# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re

class intern_model(models.Model):
    _name = 'intern.management'
    _description = 'Intern Management'

    name = fields.Char(string="Họ và Tên", required=True)
    age = fields.Integer(string="Tuổi", required=True)
    email = fields.Char(string="Email", required=True)
    address = fields.Char(string="Địa chỉ")
    phone = fields.Char(string="Số điện thoại", required=True)
    gender = fields.Selection([("male", "Nam"), ("female", "Nữ")], string="Giới tính", required=True, default="Male")
    major = fields.Char(string="Ngành học", required=True)
    skills = fields.Char(string="Kỹ năng", required=True)
    university = fields.Char(string="Trường", required=True)
    cv = fields.Binary(string="CV", required=True)
    avatar = fields.Binary(string="Chân dung")
    intern_status = fields.Selection([
        ('pending', 'Đang chờ'),
        ('active', 'Đang thực tập'),
        ('completed', 'Hoàn thành'),
    ], string="Trạng thái thực tập", default='pending', required=True)

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email không được trùng lặp!'),
        ('unique_phone', 'UNIQUE(phone)', 'Số điện thoại không được trùng lặp!'),
        ('check_age', 'CHECK(age >= 18 AND age <= 60)', 'Tuổi phải nằm trong khoảng từ 18 đến 60!')
        ]

    @api.model
    def create(self, vals):
        # required_fields = {
        #     'name': "Họ và Tên",
        #     'age': "Tuổi",
        #     'email': "Email",
        #     'phone': "Số điện thoại",
        #     'gender': "Giới tính",
        #     'major': "Ngành học",
        #     'skills': "Kỹ năng",
        #     'university': "Trường",
        #     'cv': "CV"
        # }
    
        # for field, field_string in required_fields.items():
        #     if field not in vals or vals[field] in [False, '', None]:
        #         raise ValueError(f"Trường '{field_string}' không được bỏ trống.")

        if not re.match(r'^[a-zA-Z\s]+$', vals['name']):
            raise ValueError("Trường 'Họ và Tên' phải chứa chỉ chữ cái và khoảng trắng.")
        # if not 18 <= vals['age'] <= 60:
        #     raise ValueError("Trường 'Tuổi' phải nằm trong khoảng từ 18 đến 60.")
        if not re.match(r'^\S+@\S+\.\S+$', vals['email']):
            raise ValueError("Trường 'Email' phải là một địa chỉ email hợp lệ.")
        if not re.match(r'^0\d{9,10}$', vals['phone']):
            raise ValueError("Trường 'Số điện thoại' phải là một số điện thoại hợp lệ bắt đầu bằng 0 và có 10 hoặc 11 chữ số.")
        return super(intern_model, self).create(vals)
    def write(self, vals):  
        if 'name' in vals and not re.match(r'^[a-zA-Z\s]+$', vals['name']):
            raise ValueError("Trường 'Họ và Tên' phải chứa chỉ chữ cái và khoảng trắng.")
        # if 'age' in vals and not 18 <= vals['age'] <= 60:
        #     raise ValueError("Trường 'Tuổi' phải nằm trong khoảng từ 18 đến 60.")
        if 'email' in vals and not re.match(r'^\S+@\S+\.\S+$', vals['email']):
            raise ValueError("Trường 'Email' phải là một địa chỉ email hợp lệ.")
        if 'phone' in vals and not re.match(r'^0\d{9,10}$', vals['phone']):
            raise ValueError("Trường 'Số điện thoại' phải là một số điện thoại hợp lệ bắt đầu bằng 0 và có 10 hoặc 11 chữ số.")
        return super(intern_model, self).write(vals)
    
