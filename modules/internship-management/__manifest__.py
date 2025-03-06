{
    'name': 'Internship Management',
    'version': '1.0',
    'summary': 'Quản lý lịch trình thực tập sinh',
    'description': 'Hỗ trợ tạo lịch trình, theo dõi tiến độ thực tập, và gửi thông báo nhắc nhở.',
    'category': 'Human Resources',
    'author': 'Mai Thanh Binh',
    'depends': ['base', 'intern-management', 'company_management'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/internship_view.xml',
    ],
    'installable': True,
    'application': True,
}
