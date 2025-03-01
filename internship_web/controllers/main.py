from odoo import http
from odoo.http import request


class InternWebController(http.Controller):
    
    @http.route('/intern-portal', type='http', auth='public', website=True)
    def intern_portal_home(self, **kw):
        return request.render('internship_web.portal_home', {})
    
    @http.route('/intern-portal/universities', type='http', auth='public', website=True)
    def university_list(self, **kw):
        universities = request.env['university.university'].sudo().search([])
        return request.render('internship_web.university_list', {
            'universities': universities
        })
    
    @http.route('/intern-portal/companies', type='http', auth='public', website=True)
    def company_list(self, **kw):
        companies = request.env['company.management'].sudo().search([])
        return request.render('internship_web.company_list', {
            'companies': companies
        })
    
    @http.route('/intern-portal/interns', type='http', auth='public', website=True)
    def intern_list(self, **kw):
        interns = request.env['intern.management'].sudo().search([])
        return request.render('internship_web.intern_list', {
            'interns': interns
        })
    
    @http.route('/intern-portal/university/<model("university.university"):university>', type='http', auth='public', website=True)
    def university_detail(self, university, **kw):
        return request.render('internship_web.university_detail', {
            'university': university
        })
    
    @http.route('/intern-portal/intern/<model("intern.management"):intern>', type='http', auth='public', website=True)
    def intern_detail(self, intern, **kw):
        return request.render('internship_web.intern_detail', {
            'intern': intern
        })
    
