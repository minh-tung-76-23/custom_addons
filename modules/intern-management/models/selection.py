from odoo import models, fields

class UniversitySelection(models.Model):
    _name = 'university.selection'
    _description = 'University Selection'

    name = fields.Char(string="Tên trường", required=True)
    university_selection = fields.One2many(comodel_name='intern.management', inverse_name='university_selection', string="Danh sách trường")

class MajorSelection(models.Model):
    _name = 'major.selection'
    _description = 'Major Selection'

    name = fields.Char(string="Tên ngành", required=True)
    major_selection = fields.One2many(comodel_name='intern.management', inverse_name='major_selection', string="Danh sách ngành")
