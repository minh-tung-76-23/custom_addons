from odoo import models, fields, api

class AssignInternWizard(models.TransientModel):
    _name = 'assign.intern.wizard'
    _description = 'Chọn thực tập sinh'

    intern_ids = fields.Many2many(
        comodel_name='intern.management',
        string='Sinh viên'
    )

    def action_confirm(self):
        active_id = self.env.context.get('active_id')
        request = self.env['company.request'].browse(active_id)

        # Gán sinh viên vào request
        request.write({
            'intern_ids': [(4, intern.id) for intern in self.intern_ids],
            'request_state': 'in_progress'
        })

        # Cập nhật trạng thái sinh viên
        for intern in self.intern_ids:
            intern.intern_status = 'active'

    @api.model
    def default_get(self, fields):
        res = super(AssignInternWizard, self).default_get(fields)
        intern_pending = self.env['intern.management'].search([('intern_status', '=', 'pending')])
        
        if intern_pending:
            res['intern_ids'] = [(6, 0, intern_pending.ids)]

        return res
