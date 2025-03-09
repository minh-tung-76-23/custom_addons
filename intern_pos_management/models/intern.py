# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re

from odoo.exceptions import UserError

class intern_model(models.Model):
    _name = 'intern.management'
    _description = 'Quản lý thực tập sinh'

    name = fields.Char('Tên', required=True)
    birth_date = fields.Date('Ngày sinh', default=lambda self: fields.Date.today())
    email = fields.Char('Email', required=True)
    phone = fields.Char('Số điện thoại', required=True)
    address = fields.Text('Địa chỉ')
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ], string='Giới tính', default='male')
    major = fields.Char('Ngành học', required=True)
    skills = fields.Text('Kỹ năng', required=True)
    intern_status = fields.Selection([
        ('pending', 'Đang chờ'),
        ('active', 'Đang thực tập'),
        ('completed', 'Hoàn thành'),
    ], string="Trạng thái thực tập", default='pending', required=True)
    cv = fields.Binary('CV')
    avatar = fields.Binary('Ảnh đại diện')
    university_id = fields.Many2one('university.university', string='Trường đại học', ondelete='cascade')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email không được trùng lặp!'),
        ('unique_phone', 'UNIQUE(phone)', 'Số điện thoại không được trùng lặp!'),
    ]
    selected = fields.Boolean(string="Chọn", default=False)

    # order_intern_ids = fields.One2many(
    #     comodel_name='intern.order', 
    #     inverse_name='intern_id',  
    #     string='Orders'
    # )

 # -*- coding: utf-8 -*-

    def action_send_interns(self):
    # Lấy context để lấy ID của yêu cầu
        request_id = self.env.context.get('default_request_id')
        if not request_id:
            raise UserError("Không tìm thấy yêu cầu.")

        # Lấy thông tin yêu cầu
        request = self.env['company.request'].browse(request_id)
        if not request:
            raise UserError("Không tìm thấy yêu cầu.")

        # Lấy thông tin công ty
        company = request.company_id
        if not company:
            raise UserError("Không tìm thấy thông tin công ty.")

        # Kiểm tra xem thực tập sinh đã được gán vào yêu cầu này chưa
        existing_order = self.env['intern.order'].search([
            ('request_id', '=', request_id),
            ('intern_id', '=', self.id),
        ])
        if existing_order:
            raise UserError(f'Thực tập sinh {self.name} đã được gán vào yêu cầu này.')

        # Tạo bản ghi trong intern.order
        self.env['intern.order'].create({
            'request_id': request_id,
            'intern_id': self.id,
            'status': 'pending',  # Trạng thái mặc định
        })

        # Gửi email
        self._send_email_to_company(request, company)

        # Hiển thị thông báo thành công
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã gửi thực tập sinh {self.name} và email đến công ty.',
                'type': 'success',
                'sticky': False,
            }
        }

    def _send_email_to_company(self, request, company):
        """Gửi email đến công ty với thông tin yêu cầu và sinh viên."""
        # Lấy thông tin cần thiết
        company_name = company.name
        company_email = request.contact_email  # Địa chỉ email liên hệ của công ty
        request_name = request.name
        intern_name = self.name
        intern_cv = self.cv  # CV của sinh viên

        # Kiểm tra địa chỉ email
        if not company_email:
            raise UserError("Không tìm thấy địa chỉ email liên hệ của công ty.")

        # Tạo nội dung email
        email_body = f"""
        <p>Xin chào {company_name},</p>
        <p>Bạn đã nhận được một ứng viên thực tập sinh cho yêu cầu <strong>{request_name}</strong>.</p>
        <p>Thông tin ứng viên:</p>
        <ul>
            <li><strong>Tên:</strong> {intern_name}</li>
            <li><strong>Email:</strong> {self.email}</li>
            <li><strong>Số điện thoại:</strong> {self.phone}</li>
            <li><strong>Kỹ năng:</strong> {self.skills}</li>
            <li><strong>Địa chỉ:</strong> {self.address}</li>

        </ul>
        <p>Vui lòng xem CV của ứng viên trong tệp đính kèm.</p>
        <p>Trân trọng,</p>
        <p>Hệ thống quản lý thực tập sinh</p>
        """

        # Tạo email
        email_values = {
            'subject': f'Ứng viên thực tập sinh cho yêu cầu {request_name}',
            'body_html': email_body,
            'email_to': company_email,
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

        return True

