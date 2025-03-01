from odoo import http
from odoo.http import request


class InternWebController(http.Controller):
    
    @http.route('/intern-portal', type='http', auth='public', website=True)
    def intern_portal_home(self, **kw):
        return request.render('internship_web.portal_home', {})
    

    # ----------------------Trường đại học
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
    
    # ---------------------Doanh Nghiệp
    @http.route('/intern-portal/companies', type='http', auth='public', website=True)
    def company_list(self, **kw):
        companies = request.env['company.management'].sudo().search([])
        return request.render('internship_web.company_list', {
            'companies': companies
        })

    # --------------Thực tập sinh
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
    
