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
            'student_list': student_list_data, 
            'student_filename': student_list_file.filename if student_list_file else False,
            'state': kw.get('state'),  
        })

        # Nếu trạng thái là "confirmed", thực hiện import sinh viên từ file Excel
        if university.state == 'confirmed':
            try:
                university.action_confirm()  # Gọi phương thức import sinh viên
            except Exception as e:
                # Xử lý lỗi nếu có
                _logger.error(f"Lỗi khi import sinh viên: {str(e)}")
                raise UserError(('Lỗi khi import sinh viên: %s') % str(e))

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
            'student_list': student_list_data,  
            'student_filename': student_list_file.filename if student_list_file else university.student_filename,
            'state': kw.get('state'),  
        })

        # Chuyển hướng về danh sách trường đại học
        return request.redirect('/intern-portal/universities')
    
    @http.route('/intern-portal/university/delete/<int:university_id>', type='http', auth='public', website=True)
    def university_delete(self, university_id, **kw):
        university = request.env['university.university'].sudo().browse(university_id)
        university.student_ids.unlink()
        university.unlink()
        return request.redirect('/intern-portal/universities')

# -------------------------------------Doanh Nghiệp-----------------------------------------------------------------------------------
    @http.route('/intern-portal/companies', type='http', auth='public', website=True)
    def company_list(self, **kw):
        companies = request.env['company.management'].sudo().search([])
        return request.render('internship_web.company_list', {
            'companies': companies
        })
    
    @http.route('/company/<int:company_id>', type='http', auth="public", website=True)
    def company_details(self, company_id, **kwargs):
        company = request.env['company.management'].browse(company_id)
        if not company.exists():
            return request.not_found()
        
        requests = request.env['company.request'].search([('company_id', '=', company_id)])
        return request.render('internship_web.company_details_template', {
            'company': company,
            'requests': requests,
        })

    @http.route('/company/new', type='http', auth='public', website=True)
    def company_new(self, **kw):
        return request.render('internship_web.company_new_template', {})
    
    @http.route('/company/create', type='http', auth='public', website=True, csrf=False)
    def company_create(self, **post):
        # Xử lý dữ liệu form submit
        if post:
            request.env['company.management'].sudo().create({
                'name': post.get('name'),
                'manager': post.get('manager'),
                'address': post.get('address'),
                'business_info': post.get('business_info'),
                'employer': post.get('employer'),
                'contact': post.get('contact'),
            })
        return request.redirect('/intern-portal/companies')

    @http.route('/company/edit/<int:company_id>', type='http', auth='public', website=True)
    def company_edit(self, company_id, **kw):
        company = request.env['company.management'].sudo().browse(company_id)
        return request.render('internship_web.company_edit_template', {
            'company': company
        })
    
    @http.route('/company/update/<int:company_id>', type='http', auth='public', website=True, csrf=False)
    def company_update(self, company_id, **post):
        company = request.env['company.management'].sudo().browse(company_id)
        if company:
            company.write({
                'name': post.get('name'),
                'manager': post.get('manager'),
                'address': post.get('address'),
                'business_info': post.get('business_info'),
                'employer': post.get('employer'),
                'contact': post.get('contact'),
            })
            return request.redirect('/intern-portal/companies')

# -----------------Vị trí trong doanh nghiệp
    @http.route('/company/<int:company_id>/add-request', type='http', auth="user", website=True)
    def add_request(self, company_id, **kwargs):
        # Lấy thông tin công ty
        company = request.env['company.management'].browse(company_id)
        if not company.exists():
            return request.not_found()

        # Hiển thị form thêm yêu cầu
        return request.render('internship_web.add_request_template', {
            'company': company,
        })

    @http.route('/company/<int:company_id>/submit-request', type='http', auth="user", website=True, csrf=False)
    def submit_request(self, company_id, **post):
        # Lấy thông tin công ty
        company = request.env['company.management'].browse(company_id)
        if not company.exists():
            return request.not_found()

        # Tạo yêu cầu mới từ dữ liệu form
        request.env['company.request'].create({
            'name': post.get('name'),
            'quantity_intern': int(post.get('quantity_intern')),
            'request_skills': post.get('request_skills'),
            'request_details': post.get('request_details'),
            'job_description': post.get('job_description'),
            'interest': post.get('interest'),
            'work_time': post.get('work_time'),
            'note': post.get('note'),
            'company_id': company.id,
        })

        # Chuyển hướng về trang chi tiết công ty
        return request.redirect(f'/company/{company.id}')
    
    # Hiển thị form sửa yêu cầu
    @http.route('/company/<int:company_id>/edit-request/<int:request_id>', type='http', auth="user", website=True)
    def edit_request(self, company_id, request_id, **kwargs):
        # Lấy thông tin công ty và yêu cầu
        company = request.env['company.management'].browse(company_id)
        request_obj = request.env['company.request'].browse(request_id)
        if not company.exists() or not request_obj.exists():
            return request.not_found()
        return request.render('internship_web.edit_request_template', {
            'company': company,
            'req': request_obj,
        })

    # Xử lý dữ liệu khi submit form sửa
    @http.route('/company/<int:company_id>/update-request/<int:request_id>', type='http', auth="user", website=True, csrf=False)
    def update_request(self, company_id, request_id, **post):
        company = request.env['company.management'].browse(company_id)
        request_obj = request.env['company.request'].browse(request_id)
        if not company.exists() or not request_obj.exists():
            return request.not_found()
        request_obj.write({
            'name': post.get('name'),
            'quantity_intern': int(post.get('quantity_intern')),
            'request_skills': post.get('request_skills'),
            'request_details': post.get('request_details'),
            'job_description': post.get('job_description'),
            'interest': post.get('interest'),
            'work_time': post.get('work_time'),
            'note': post.get('note'),
            'request_state': post.get('request_state'),  
        })
        return request.redirect(f'/company/{company.id}')

    @http.route('/company/<int:company_id>/delete-request/<int:request_id>', type='http', auth="user", website=True, csrf=False)
    def delete_request(self, company_id, request_id, **kwargs):
        company = request.env['company.management'].browse(company_id)
        request_obj = request.env['company.request'].browse(request_id)
        if not company.exists() or not request_obj.exists():
            return request.not_found()
        request_obj.unlink()
        return request.redirect(f'/company/{company.id}')
        
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
            'avatar': avatar_data,  
            'cv': cv_data,  
        })
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
    
#  ----------------------------------------------------------Quá trình duyệt TTS   

    @http.route('/intern/order/approve/<int:order_id>', type='http', auth="public", website=True)
    def show_appointment_form(self, order_id, **kwargs):
        intern_order = request.env['intern.order'].sudo().browse(order_id)
        if not intern_order.exists():
            return request.not_found()
        return request.render('internship_web.appointment_form_template', {
            'order': intern_order,
        })

    @http.route('/intern/order/approve/submit', type='http', auth="public", website=True, csrf=False)
    def submit_appointment_form(self, **post):
        order_id = int(post.get('order_id'))
        appointment_schedule = post.get('appointment_schedule')
        intern_order = request.env['intern.order'].sudo().browse(order_id)
        if intern_order.exists():
            intern_order.write({
                'appointment_schedule': appointment_schedule,
                'status': 'approved',
            })
            return request.render('internship_web.appointment_success_template', {
                'order': intern_order,
            })
        return request.not_found()
    
    @http.route('/intern/order/reject/<int:order_id>', type='http', auth="public", website=True)
    def reject_order_res(self, order_id):
        """Xử lý yêu cầu từ đường link và cập nhật trạng thái"""
        order = request.env['intern.order'].sudo().browse(order_id)
        if order.exists():
            order.reject_order_convert()  # Gọi phương thức từ đối tượng order
            # Hiển thị thông báo trên một trang web
            return request.render('internship_web.reject_order_template', {
                'message': "Cảm ơn bạn đã phản hồi. Chúng tôi sẽ tìm kiếm ứng viên khác phù hợp!",
            })
        else:
            return request.not_found("Không tìm thấy đơn thực tập.")
        
    @http.route('/intern/order/confirm/approve/<int:order_id>', type='http', auth="public", website=True)
    def show_appointment_form_confirm(self, order_id, **kwargs):
        intern_order = request.env['intern.order'].sudo().browse(order_id)
        if not intern_order.exists():
            return request.not_found()
        return request.render('internship_web.appointment_complete_form_template', {
            'order': intern_order,
        })

    @http.route('/intern/order/confirm/approve/submit', type='http', auth="public", website=True, csrf=False)
    def submit_appointment_form_confirm(self, **post):
        order_id = int(post.get('order_id'))
        appointment_schedule = post.get('appointment_schedule')
        intern_order = request.env['intern.order'].sudo().browse(order_id)
        if intern_order.exists():
            intern_order.write({
                'appointment_schedule': appointment_schedule,
                'status': 'completed',
            })
            return request.render('internship_web.appointment_complete_success_template', {
                'order': intern_order,
            })
        return request.not_found()