{
    "name": "InternShip Position Management",
    "sumary": "InternShip Position Management",
    "version": "1.0",
    "description": "Sử dụng để quản lý quá trình chuyển thực tập sinh đến doanh nghiệp",
    "author": "My Company",
    # "website": "http://www.mycompany.com",
    "category": "Tools",
    "depend": ['base', 
               'company_management', 
               'intern_management'
    ],
    
    "data": [
        # 'security/company_security.xml',
        # 'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/intern_pos_views.xml',
        'views/intern_order_views.xml',
        'views/appointment_form_template.xml',
        'views/reject_order_template.xml',
        'views/list_intern_views.xml',
        # 'views/request_views.xml',
    ],
    'license': 'LGPL-3', 
    # 'demo': [],
    # 'images': [],
    'installable': True,
    'application': True,
    # 'auto_install': False,

}