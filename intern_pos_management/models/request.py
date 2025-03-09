from odoo import models, fields, api

class Request(models.Model):
    _name = 'company.request'
    _description = 'Yêu cầu của doanh nghiệp'

    name = fields.Char(string='Vị trí', required=True)
    quantity_intern = fields.Integer("Số lượng thực tập sinh")
    sent_quantity = fields.Integer("Số lượng đã gửi", default=0)  
    request_skills = fields.Text(string='Kĩ năng')
    request_details = fields.Text(string='Yêu cầu công việc')
    job_description = fields.Text(string='Mô tả công việc')
    interest = fields.Text(string='Quyền lợi')
    work_time = fields.Text(string='Thời gian làm việc')
    contact_email = fields.Char(string='Địa chỉ email liên hệ')
    note = fields.Text(string='Ghi chú')
    request_state = fields.Selection(
        [
            ('insufficient', 'Chưa đủ yêu cầu'),
            ('submitted', 'Đã nộp'),
            ('approved', 'Đã phê duyệt'),
            ('rejected', 'Bị từ chối')
        ],
        string='Trạng thái yêu cầu',
        default='insufficient'
    )
    company_id = fields.Many2one(
        comodel_name='company.management',
        string='Company'
    )

    @api.constrains('sent_quantity', 'quantity_intern')
    def _check_sent_quantity(self):
        for record in self:
            if record.sent_quantity == record.quantity_intern:
                record.request_state = 'submitted'

    # Phương thức xử lý khi click nút "Gửi thực tập sinh"
    def action_send_interns(self):
        # Mở view hiển thị tên yêu cầu và danh sách sinh viên
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,  # Tên yêu cầu
            'res_model': 'intern.management',  # Model hiển thị
            'view_mode': 'tree,form',  # Chế độ hiển thị
            'domain': [('intern_status', '=', 'pending')],  # Lọc dữ liệu nếu cần
            'context': {
                'default_request_id': self.id,  # Truyền ID của yêu cầu
            },
            'target': 'new',  # Mở trong cửa sổ mới
        }