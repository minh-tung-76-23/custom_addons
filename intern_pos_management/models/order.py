from odoo import models, fields, api
from odoo.exceptions import UserError

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
        ('completed', 'Hoàn thành'),
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
        request.write({'request_state': 'insufficient'})

    def get_approval_link(self):
        """Tạo đường link để chấp nhận đơn thực tập"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/intern/order/approve/{self.id}"

    def get_reject_link(self):
        """Tạo đường link để từ chối đơn thực tập"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/intern/order/reject/{self.id}"

    def get_approval_link_confirm(self):
        """Tạo đường link để chấp nhận đơn thực tập"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/intern/order/confirm/approve/{self.id}"

    def send_email(self):
        """Gửi email đến công ty với thông tin thực tập sinh và liên kết chấp nhận/từ chối."""
        # Lấy thông tin yêu cầu và công ty
        request = self.request_id
        company = request.company_id

        # Kiểm tra xem có thông tin công ty và email liên hệ không
        if not company:
            raise UserError("Không tìm thấy thông tin công ty.")
        if not request.contact_email:
            raise UserError("Không tìm thấy địa chỉ email liên hệ của công ty.")

        # Tạo đường link để chấp nhận và từ chối đơn thực tập
        approval_link = self.get_approval_link_confirm()
        reject_link = self.get_reject_link()

        # Lấy thông tin thực tập sinh
        intern = self.intern_id
        intern_name = intern.name
        intern_email = intern.email
        intern_phone = intern.phone
        intern_skills = intern.skills
        intern_address = intern.address
        intern_cv = intern.cv  # CV của thực tập sinh

        # Tạo nội dung email
        email_body = f"""
        <p>Xin chào {company.name},</p>
        <p>Kết quả buổi phỏng vấn cho vị trí <strong>{request.name}</strong>.</p>
        <p>Thông tin ứng viên:</p>
        <ul>
            <li><strong>Tên:</strong> {intern_name}</li>
            <li><strong>Email:</strong> {intern_email}</li>
            <li><strong>Số điện thoại:</strong> {intern_phone}</li>
            <li><strong>Kỹ năng:</strong> {intern_skills}</li>
            <li><strong>Địa chỉ:</strong> {intern_address}</li>
        </ul>
        <p>Chúng tôi thấy ứng viên đã tham gia lịch hẹn phỏng vấn cho vị trí tại công ty.</p>
        <p>Nếu thấy ứng viên phù hợp, vui lòng: <a href="{approval_link}">Chấp nhận ứng viên</a></p>
        <p>Nếu ứng viên không phù hợp, <a href="{reject_link}">Vui lòng click vào đây!</a></p>
        <p>Trân trọng,</p>
        <p>Hệ thống quản lý thực tập sinh</p>
        """

        # Tạo email
        email_values = {
            'subject': f'Ứng viên thực tập sinh cho yêu cầu {request.name}',
            'body_html': email_body,
            'email_to': request.contact_email,
            'email_from': self.env.user.email or 'no-reply@example.com',
        }

        # Đính kèm CV nếu có
        if intern_cv:
            email_values['attachment_ids'] = [
                (0, 0, {
                    'name': f'CV_{intern_name}.pdf',
                    'type': 'binary',
                    'datas': intern_cv,
                })
            ]

        # Gửi email
        self.env['mail.mail'].create(email_values).send()

        # Hiển thị thông báo thành công
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã gửi email đến công ty {company.name} với thông tin thực tập sinh {intern_name}.',
                'type': 'success',
                'sticky': False,
            }
        }