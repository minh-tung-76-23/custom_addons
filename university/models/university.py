from odoo import models, fields, api
import base64
import pandas as pd


class University(models.Model):
    _name = 'university'
    _description = 'University Management'

    name = fields.Char(string="University Name", required=True)
    address = fields.Char(string="Address")
    states_university = fields.Selection([
        ('received', 'Đã nhận'),
        ('interning', 'Đang thực tập'),
        ('returned', 'Hoàn thành')
    ], string="State", default='draft')

    list_info = fields.One2many('intern.management', 'university_id', string="Student Info")
    excel_file = fields.Binary(string="Upload Excel File")
    file_name = fields.Char(string="File Name")

    def import_students_from_excel(self):
        if not self.excel_file:
            raise ValueError("No file uploaded!")
        
        # Decode the file content
        file_content = base64.b64decode(self.excel_file)

        # Read the Excel file using pandas
        try:
            # Assuming the file has headers matching the field names in the `intern.management` model
            data = pd.read_excel(file_content)

            for index, row in data.iterrows():
                self.env['intern.management'].create({
                    'name': row.get('Họ và Tên'),
                    'age': row.get('Tuổi'),
                    'email': row.get('Email'),
                    'address': row.get('Địa chỉ'),
                    'phone': row.get('Số điện thoại'),
                    'gender': row.get('Giới tính'),
                    'major': row.get('Ngành học'),
                    'skills': row.get('Kỹ năng'),
                    'university': self.name,  # Link university name automatically
                    'cv': False,  # Placeholder if no CV data in Excel
                    'avatar': False,  # Placeholder if no avatar data in Excel
                    'intern_status': 'pending',
                })

        except Exception as e:
            raise ValueError(f"Failed to import Excel file: {e}")
