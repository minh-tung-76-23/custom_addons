# models/intern_order.py
from odoo import models, fields

class InternOrder(models.Model):
    _name = 'intern.order'
    _description = 'Đơn thực tập'

    request_id = fields.Many2one('company.request', string='Yêu cầu', required=True)
    intern_id = fields.Many2one('intern.management', string='Thực tập sinh', required=True)
    appointment_schedule = fields.Text(string='Lịch hẹn')
    status = fields.Selection([
        ('pending', 'Chờ xác nhận'),
        ('approved', 'Đồng ý'),
        ('rejected', 'Từ chối'),
    ], string='Trạng thái', default='pending')

