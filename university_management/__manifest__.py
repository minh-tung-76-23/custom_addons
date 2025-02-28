{
    "name": "University Management",
    "version": "1.0",
    "description": "This is a university management system",
    "author": "Minh Tung",
    # "website": "http://www.mycompany.com",
    "category": "Education",
    "depend": ['base', 'intern_management',],
    "data": [
        # 'security/ir.models.access.csv',
        'views/university_views.xml',
        'views/students_views.xml',
        'views/menu_views.xml',
    ],
    'license': 'LGPL-3', 
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}