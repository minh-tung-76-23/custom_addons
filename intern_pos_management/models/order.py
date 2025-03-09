# models/intern_order.py
from odoo import models, fields

class InternOrder(models.Model):
    _name = 'intern.order'
    _description = 'Đơn thực tập'

    request_id = fields.Many2one('company.request', string='Yêu cầu', required=True)
    intern_id = fields.Many2one('intern.management', string='Thực tập sinh', required=True)
    company_name = fields.Char(string='Tên công ty', related='request_id.company_id.name', readonly=True)
    appointment_schedule = fields.Text(string='Lịch hẹn')
    status = fields.Selection([
        ('pending', 'Chờ xác nhận'),
        ('approved', 'Đồng ý'),
        ('rejected', 'Từ chối'),
    ], string='Trạng thái', default='pending')

    def approve_order_convert(self):
        """Cập nhật trạng thái thành 'Đồng ý'"""
        self.write({'status': 'approved'})

    def reject_order_convert(self):
        """Cập nhật trạng thái thành 'Từ chối'"""
       # Lấy request_id từ trường request_id của đối tượng hiện tại
        request = self.request_id
        self.write({'status': 'rejected'})
        # Giảm số lượng đã gửi đi 1
        request.write({'sent_quantity': request.sent_quantity - 1})

    def get_approval_link(self):
            """Tạo đường link để chấp nhận đơn thực tập"""
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            return f"{base_url}/intern/order/approve/{self.id}"
    
    def get_reject_link(self):
            """Tạo đường link để chấp nhận đơn thực tập"""
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            return f"{base_url}/intern/order/reject/{self.id}"