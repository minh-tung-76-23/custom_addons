{
    'name': 'Intern Management Web Portal',
    'version': '1.0',
    'summary': 'Website for managing interns, universities and companies',
    'description': """
        Website module integrating university_management, company_management, 
        and intern_management modules into a user-friendly web interface.
    """,
    'category': 'Website',
    'author': 'Minh Tung',
    'website': 'https://www.yourwebsite.com',
    'depends': [
        'website',
        'university_management',
        'company_management',
        'intern_management',
    ],
    'data': [
        'views/home_views.xml',
        'views/intern_views.xml',
        'views/university_views.xml',
        'views/company_views.xml',
        'views/website_menu.xml',
        # 'security/ir.model.access.csv', 
    ],
    'license': 'LGPL-3', 
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
