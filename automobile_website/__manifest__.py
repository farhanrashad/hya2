{
    'name': 'Automobile Website',
    'summary': 'Automobile Website',
    'version': '1.6',
    'description': """Automobile Website""",
    'author': '',
    'category': 'Website',
    'website': "",
    'depends': ['base', 'website_sale', 'sale', 'website'],
    'data': [
        'views/template.xml',
        'views/product.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}
