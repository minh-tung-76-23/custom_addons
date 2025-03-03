import base64
import tempfile
import logging
import requests
import os
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import openpyxl
from datetime import datetime, date


_logger = logging.getLogger(__name__)

class University(models.Model):
    _name = 'university.university'
    _description = 'Thông tin trường đại học'
    
    name = fields.Char('Tên trường', required=True)
    address = fields.Text('Địa chỉ', required=True)
    student_list = fields.Binary('File danh sách sinh viên', attachment=True, help='Upload file danh sách sinh viên định dạng Excel (.xls, .xlsx)')
    student_filename = fields.Char('Tên file')
    student_count = fields.Integer('Số lượng sinh viên', compute='_compute_student_count')
    
    student_ids = fields.One2many('intern.management', 'university_id', string='Danh sách sinh viên')
    
    state = fields.Selection([
        ('draft', 'Bản nháp'),
        ('confirmed', 'Đã nhận'),
        ('done', 'Hoàn thành')
    ], string='Trạng thái', default='draft', tracking=True)

    def _valid_field_parameter(self, field, name):
        # Cho phép sử dụng tham số 'tracking' trong trường 'state'
        if name == 'tracking':
            return True
        return super(University, self)._valid_field_parameter(field, name)
    
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)
    
    def _download_and_encode_file(self, file_url):
        """
        Tải file từ URL và mã hóa thành base64
        """
        try:
            # Xử lý URL Google Drive
            if 'drive.google.com' in file_url:
                # Chuyển URL Drive thành URL tải xuống trực tiếp
                file_id = None
                if '/file/d/' in file_url:
                    file_id = file_url.split('/file/d/')[1].split('/')[0]
                elif 'id=' in file_url:
                    file_id = file_url.split('id=')[1].split('&')[0]
                
                if not file_id:
                    _logger.warning(f"Không thể trích xuất ID từ URL Google Drive: {file_url}")
                    return False
                
                direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                file_url = direct_url
            
            # Tải file
            response = requests.get(file_url, timeout=10)
            if response.status_code != 200:
                _logger.warning(f"Không thể tải file từ {file_url}, mã trạng thái: {response.status_code}")
                return False
            
            # Mã hóa nội dung file thành base64
            file_content = response.content
            encoded_content = base64.b64encode(file_content)
            return encoded_content
        except Exception as e:
            _logger.error(f"Lỗi khi tải file từ {file_url}: {str(e)}")
            return False
    
    def _process_local_file(self, file_path):
        """
        Đọc file từ đường dẫn cục bộ và mã hóa thành base64
        """
        try:
            if not os.path.exists(file_path):
                _logger.warning(f"File không tồn tại: {file_path}")
                return False
            
            with open(file_path, 'rb') as file:
                file_content = file.read()
                encoded_content = base64.b64encode(file_content)
                return encoded_content
        except Exception as e:
            _logger.error(f"Lỗi khi đọc file từ {file_path}: {str(e)}")
            return False
    
    def action_confirm(self):
        self.ensure_one()
        if not self.student_list:
            raise UserError(_('Vui lòng upload file danh sách sinh viên trước khi xác nhận.'))
        
        # Xóa danh sách sinh viên cũ nếu có
        self.student_ids.unlink()
        
        # Đọc file Excel sử dụng openpyxl
        try:            
            # Lưu file tạm thời
            file_content = base64.b64decode(self.student_list)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            # Mở workbook
            workbook = openpyxl.load_workbook(temp_file_path, read_only=True, data_only=True)
            sheet = workbook.active
            
            # Xác định cấu trúc file Excel (giả định các cột theo thứ tự)
            # Mã sinh viên, Họ tên, Ngày sinh, Giới tính, Email, SĐT, Địa chỉ, Tuổi, Ngành học, Kỹ năng, CV URL
            intern_vals_list = []
            
            # Bỏ qua dòng header
            rows = list(sheet.rows)
            for row_idx, row in enumerate(rows[1:], 1):
                # Lấy giá trị các ô cho model university.student
                student_id = row[0].value
                name = row[1].value
                birth_date = row[2].value
                gender_value = row[3].value if len(row) > 3 else ''
                email = row[4].value if len(row) > 4 else ''
                phone = row[5].value if len(row) > 5 else ''
                address = row[6].value if len(row) > 6 else ''
                
                # Lấy giá trị các ô bổ sung cho model intern.management
                major = row[7].value if len(row) > 7 else ''
                skills = row[8].value if len(row) > 8 else ''
                
                # Lấy URL CV từ cột thứ 10 (index 9)
                cv_url = row[9].value if len(row) > 9 and row[9].value else False
                cv_binary = False
                
                # Kiểm tra các trường bắt buộc cho university.student
                if not student_id or not name:
                    _logger.warning(f"Bỏ qua dòng {row_idx + 1} do thiếu thông tin bắt buộc")
                    continue
                
                if birth_date and isinstance(birth_date, str):
                    try:
                        birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
                    except ValueError:
                        _logger.warning(f"Ngày sinh không hợp lệ tại dòng {row_idx + 1}: {birth_date}")
                        birth_date = None

                
                # Xử lý giới tính
                gender = 'male'
                if gender_value:
                    gender_value = str(gender_value).lower()
                    if gender_value in ['nữ', 'female', 'f']:
                        gender = 'female'
                    elif gender_value not in ['nam', 'male', 'm']:
                        gender = 'other'
                
                # Kiểm tra các trường bắt buộc cho intern.management
                if not name or not email or not phone or not major or not skills:
                    _logger.warning(f"Không tạo bản ghi intern cho dòng {row_idx + 1} do thiếu thông tin bắt buộc")
                    continue
                
                # Xử lý URL CV
                if cv_url:
                    if cv_url.startswith(('http://', 'https://')):
                        # Nếu là URL từ internet (Google Drive, etc.)
                        cv_binary = self._download_and_encode_file(cv_url)
                    elif os.path.exists(cv_url):
                        # Nếu là đường dẫn file cục bộ
                        cv_binary = self._process_local_file(cv_url)
                    
                    if not cv_binary:
                        _logger.warning(f"Không thể tải hoặc xử lý CV từ {cv_url} ở dòng {row_idx + 1}")
                        # Vẫn tiếp tục tạo record nhưng không có CV
                        
                # Tạo dữ liệu cho model intern.management
                intern_vals = {
                    'name': name,
                    'birth_date': birth_date if birth_date else date(date.today().year - 20, 1, 1),
                    'email': str(email).strip(),
                    'address': address if address else False,  
                    'phone': str(phone).strip(),
                    'gender': gender if gender in ['male', 'female'] else 'male',
                    'major': major,  
                    'skills': skills,  
                    'university_id': self.id,
                    'intern_status': 'pending',
                    'cv': cv_binary,  # Thêm CV đã tải và mã hóa
                    'avatar': False
                }
                intern_vals_list.append(intern_vals)
                     
            # Tạo bản ghi intern    
            if intern_vals_list:
                self.env['intern.management'].create(intern_vals_list)
                _logger.info(f"Đã import thành công {len(intern_vals_list)} bản ghi vào model intern.management")
                # Chỉ chuyển trạng thái khi đã tạo được ít nhất một bản ghi
                self.state = 'confirmed'
            else:
                # Không thể tạo bản ghi nào, báo lỗi và không chuyển trạng thái
                raise UserError(_('Không thể tạo bản ghi nào từ file Excel. Vui lòng kiểm tra dữ liệu và thử lại.'))
                
        except ImportError:
            raise UserError(_('Không thể import thư viện openpyxl. Vui lòng cài đặt thư viện này để đọc file Excel định dạng .xlsx'))
        except Exception as e:
            raise UserError(_('Lỗi khi đọc file Excel: %s') % str(e))

    def action_done(self):
        self.state = 'done'
    
    def action_draft(self):
        self.state = 'draft'
        self.student_ids.unlink()
        
    def action_view_students(self):
        self.ensure_one()
        return {
            'name': _('Sinh viên của %s') % self.name,
            'view_mode': 'tree,form',
            'res_model': 'intern.management',
            'domain': [('university_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_university_id': self.id}
        }