from odoo import http
from odoo.http import request
import base64
import logging
from odoo.exceptions import UserError
import tempfile

_logger = logging.getLogger(__name__)
class InternWebController(http.Controller):
    
    @http.route('/intern-portal', type='http', auth='public', website=True)
    def intern_portal_home(self, **kw):
        return request.render('internship_web.portal_home', {})
    

    # -------------------------------------Trường đại học--------------------------------------------------------------------------------------
    @http.route('/intern-portal/universities', type='http', auth='public', website=True)
    def university_list(self, **kw):
        universities = request.env['university.university'].sudo().search([])
        return request.render('internship_web.university_list', {
            'universities': universities
        })
    
    @http.route('/intern-portal/university/<model("university.university"):university>', type='http', auth='public', website=True)
    def university_detail(self, university, **kw):
        return request.render('internship_web.university_detail', {
            'university': university
        })

    @http.route('/intern-portal/university/new', type='http', auth='public', website=True)
    def university_new(self, **kw):
        # Hiển thị form thêm trường đại học mới
        return request.render('internship_web.university_new_template', {})

    @http.route('/intern-portal/university/create', type='http', auth='public', website=True, methods=['POST'])
    def university_create(self, **kw):
        # Xử lý file upload
        student_list_file = kw.get('student_list')
        student_list_data = base64.b64encode(student_list_file.read()) if student_list_file else False

        # Tạo trường đại học mới từ dữ liệu form
        university = request.env['university.university'].sudo().create({
            'name': kw.get('name'),
            'address': kw.get('address'),
            'student_list': student_list_data,  # Lưu file danh sách sinh viên dưới dạng base64
            'student_filename': student_list_file.filename if student_list_file else False,
            'state': kw.get('state'),  # Lưu trạng thái
        })

        # Nếu trạng thái là "confirmed", thực hiện import sinh viên từ file Excel
        if university.state == 'confirmed':
            try:
                university.action_confirm()  # Gọi phương thức import sinh viên
            except Exception as e:
                # Xử lý lỗi nếu có
                _logger.error(f"Lỗi khi import sinh viên: {str(e)}")
                raise UserError(_('Lỗi khi import sinh viên: %s') % str(e))

        # Chuyển hướng về danh sách trường đại học
        return request.redirect('/intern-portal/universities')
    
    @http.route('/intern-portal/university/edit/<int:university_id>', type='http', auth='public', website=True)
    def university_edit(self, university_id, **kw):
        # Lấy thông tin trường đại học từ database
        university = request.env['university.university'].sudo().browse(university_id)
        # Trả về template và truyền dữ liệu
        return request.render('internship_web.university_edit_template', {
            'university': university
        })

    @http.route('/intern-portal/university/update/<int:university_id>', type='http', auth='public', website=True, methods=['POST'])
    def university_update(self, university_id, **kw):
        # Lấy thông tin trường đại học từ database
        university = request.env['university.university'].sudo().browse(university_id)
        
        # Xử lý file upload
        student_list_file = kw.get('student_list')
        student_list_data = base64.b64encode(student_list_file.read()) if student_list_file else university.student_list

        # Cập nhật thông tin trường đại học
        university.write({
            'name': kw.get('name'),
            'address': kw.get('address'),
            'student_list': student_list_data,  # Lưu file danh sách sinh viên dưới dạng base64
            'student_filename': student_list_file.filename if student_list_file else university.student_filename,
            'state': kw.get('state'),  # Lưu trạng thái
        })

        # Chuyển hướng về danh sách trường đại học
        return request.redirect('/intern-portal/universities')
    
    @http.route('/intern-portal/university/delete/<int:university_id>', type='http', auth='public', website=True)
    def university_delete(self, university_id, **kw):
        # Lấy thông tin trường đại học từ database
        university = request.env['university.university'].sudo().browse(university_id)
        
        # Xóa tất cả sinh viên liên quan
        university.student_ids.unlink()
        
        # Xóa trường đại học
        university.unlink()

        # Chuyển hướng về danh sách trường đại học
        return request.redirect('/intern-portal/universities')

    # -------------------------------------Doanh Nghiệp-----------------------------------------------------------------------------------
    @http.route('/intern-portal/companies', type='http', auth='public', website=True)
    def company_list(self, **kw):
        companies = request.env['company.management'].sudo().search([])
        return request.render('internship_web.company_list', {
            'companies': companies
        })

    # -----------------------------------Thực tập sinh--------------------------------------------------------------------------------------
    @http.route('/intern-portal/interns', type='http', auth='public', website=True)
    def intern_list(self, **kw):
        interns = request.env['intern.management'].sudo().search([])
        return request.render('internship_web.intern_list', {
            'interns': interns
        })
    
    @http.route('/intern-portal/intern/<model("intern.management"):intern>', type='http', auth='public', website=True)
    def intern_detail(self, intern, **kw):
        return request.render('internship_web.intern_detail', {
            'intern': intern
        })
    
    @http.route('/intern-portal/intern/new', type='http', auth='public', website=True)
    def intern_new(self, **kw):
        # Hiển thị form thêm thực tập sinh mới
        return request.render('internship_web.intern_new_template', {})
    
    @http.route('/intern-portal/intern/create', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def intern_create(self, **kw):
        # Xử lý file upload
        avatar_file = kw.get('avatar')
        cv_file = kw.get('cv')

        # Chuyển đổi file thành base64
        avatar_data = base64.b64encode(avatar_file.read()) if avatar_file else False
        cv_data = base64.b64encode(cv_file.read()) if cv_file else False

        # Tạo thực tập sinh mới từ dữ liệu form
        request.env['intern.management'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'phone': kw.get('phone'),
            'birth_date': kw.get('birth_date'),
            'address': kw.get('address'),
            'gender': kw.get('gender'),
            'major': kw.get('major'),
            'skills': kw.get('skills'),
            'intern_status': kw.get('intern_status'),
            'university_id': int(kw.get('university_id')),
            'avatar': avatar_data,  # Lưu ảnh đại diện dưới dạng base64
            'cv': cv_data,  # Lưu CV dưới dạng base64
        })
        # Chuyển hướng về danh sách thực tập sinh
        return request.redirect('/intern-portal/interns')
    @http.route('/intern-portal/intern/<int:intern_id>', type='http', auth='public', website=True)
    def intern_detail(self, intern_id, **kwargs):
        intern = request.env['intern.management'].sudo().browse(intern_id)
        if not intern.exists():
            return request.not_found()
        return request.render('internship_web.intern_detail_template', {
            'intern': intern
        })
    
    @http.route('/intern-portal/intern/update/<int:intern_id>', type='http', auth="user", website=True, csrf=False)
    def update_intern(self, intern_id, **post):
        # Lấy bản ghi thực tập sinh từ database
        intern = request.env['intern.management'].browse(intern_id)
        if intern:
            # Cập nhật dữ liệu từ form
            intern.write({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'birth_date': post.get('birth_date'),
                'address': post.get('address'),
                'gender': post.get('gender'),
                'major': post.get('major'),
                'skills': post.get('skills'),
                'intern_status': post.get('intern_status'),
                'university_id': int(post.get('university_id')),
            })
            # Xử lý tải lên ảnh đại diện và CV
            if post.get('avatar'):
                intern.avatar = post.get('avatar').read()
            if post.get('cv'):
                intern.cv = post.get('cv').read()
        # Chuyển hướng về trang chi tiết
        return request.redirect(f'/intern-portal/intern/{intern_id}')
    
    @http.route('/intern-portal/intern/delete/<int:intern_id>', type='http', auth="user", website=True, csrf=True)
    def delete_intern(self, intern_id, **kw):
        # Lấy bản ghi sinh viên từ database
        intern = request.env['intern.management'].browse(intern_id)
        id_university = intern.university_id.id
        if intern:
            # Xóa bản ghi
            intern.unlink()
        # Chuyển hướng về trang chi tiết trường đại học
        return request.redirect(f'/intern-portal/university/{id_university}')