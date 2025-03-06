from odoo import models, fields

class Request(models.Model):
    _name = 'company.request'
    _description = 'Yêu cầu của doanh nghiệp'

    name = fields.Char(string='Vị trí', required=True)
    quantity_intern = fields.Integer("Số lượng thực tập sinh")
    request_skills = fields.Text(string='Kĩ năng')
    request_details = fields.Text(string='Yêu cầu công việc')
    job_description = fields.Text(string='Mô tả công việc')
    interest = fields.Text(string='Quyền lợi')
    work_time = fields.Text(string='Thời gian làm việc')
    note = fields.Text(string='Ghi chú') 
    request_state = fields.Selection(  
    [
        ('draft', 'Nháp'), 
        ('in-progress', 'Đang xử lý'), 
        ('approved', 'Đã phê duyệt'), 
        ('rejected', 'Bị từ chối')
    ],
    string='Trạng thái yêu cầu', 
    default='draft'
)
    company_id = fields.Many2one(
        comodel_name='company.management',  # Liên kết với mô hình `company.management`
        string='Company'
    )

    def action_assign_intern(self):
        return {
            'name': 'Giao thực tập sinh',
            'type': 'ir.actions.act_window',
            'res_model': 'assign.intern.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_intern_id': False}
        }