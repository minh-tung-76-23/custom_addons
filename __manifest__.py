# -*- coding: utf-8 -*-
{
    'name': "intern",

    'summary': """
        Module này dùng để quản lý thông tin sinh viên thực tập""",

    'description': """
        Module này dùng để quản lý thông tin thực tập sinh trong nhiều công ty khác nhau
    """,

    'author': "Funix Dev",
    'website': "https://funix.edu.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'installable': True,
    'application': True,

    'data': [
        # 'security/groups.xml',
        # 'security/ir.model.access.csv',
        # 'views/menu_views.xml',
        'views/intern_views.xml',
    ],
}
