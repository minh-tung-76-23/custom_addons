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
       # One2many relationship to 'request'
    request_ids = fields.One2many(
        comodel_name='company.request',  # Trỏ đến mô hình `request`
        inverse_name='company_id',  # Tên trường Many2one trong mô hình `request`
        string='Requests'
    )
