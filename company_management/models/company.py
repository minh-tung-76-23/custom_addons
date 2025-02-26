from odoo import models, fields

class Company(models.Model):
    _name = 'company.management'
    _description = 'Company management'

    name = fields.Char(string='Tên doanh nghiệp', required=True)
    manager = fields.Char(string='Giám đốc')  
    address = fields.Text(string='Địa chỉ')
    business_info = fields.Text(string='Thông tin doanh nghiệp') 
    employer = fields.Char(string='Người tuyển dụng')  
    contact = fields.Char(string='Thông tin liên hệ')
    request_ids = fields.One2many('company.request', 'company_id', string='Requests')
