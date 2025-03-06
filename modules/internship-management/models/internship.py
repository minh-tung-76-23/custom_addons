import logging
from odoo import models, fields, api
from datetime import timedelta

class Internship(models.Model):
    _name = 'internship.management'
    _description = 'Internship Management'

    position = fields.Char(string='Vị trí', required=True)
    intern_id = fields.Many2one('intern.management', string='Intern', required=True, domain=[('intern_status', '=', 'active')])
    intern_name = fields.Char(string='Họ và Tên', related='intern_id.name', store=True)
    business_id = fields.Many2one('company.management', string='Business', required=True)
    business_name = fields.Char(string='Tên doanh nghiệp', related='business_id.name', store=True)
    intern_status = fields.Selection(related='intern_id.intern_status', string='Trạng thái thực tập', store=True)
    start_date = fields.Date(string='Ngày bắt đầu', required=True)
    end_date = fields.Date(string='Ngày kết thúc', required=True)
    duration = fields.Integer(string='Thời hạn (ngày)', compute='_compute_duration', store=True)
    intern_report = fields.Binary(string='Báo cáo thực tập')
    business_report = fields.Binary(string='Báo cáo doanh nghiệp')
    
    @api.onchange('intern_status')
    def _onchange_state(self):
        if self.intern_status == 'active' and not self.start_date:
            self.start_date = fields.Date.today()

    @api.model
    def cron_update_internship_status(self):
        today = fields.Date.today()
        internships = self.search([('end_date', '<', today), ('intern_status', '!=', 'completed'), ('intern_status', '!=', 'canceled')])
        for internship in internships:
            internship.intern_status = 'completed'
    
    @api.model
    def cron_update_duration(self):
        internships = self.search([])
        for internship in internships:
            if internship.start_date and internship.end_date:
                delta = internship.end_date - internship.start_date
                internship.duration = delta.days
            else:
                internship.duration = 0

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration = delta.days
            else:
                record.duration = 0

_logger = logging.getLogger(__name__)
_logger.info(">>> MODEL ĐÃ LOAD: internship")
