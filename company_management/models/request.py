from odoo import api, models, fields

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
