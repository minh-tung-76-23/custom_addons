# -*- coding: utf-8 -*-

from odoo import models, fields, api

class intern_model(models.Model):
    _name = 'intern.management'
    _description = 'Quản lý thực tập sinh'

    name = fields.Char('Tên', required=True)
    age = fields.Integer('Tuổi', default=20)
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
        ('check_age', 'CHECK(age >= 18 AND age <= 60)', 'Tuổi phải nằm trong khoảng từ 18 đến 60!')
    ]