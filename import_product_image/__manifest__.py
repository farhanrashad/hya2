# -*- coding: utf-8 -*-

{
    'name': "Import Product Image",
    'version': '11.0.1.0.0',
    'summary': """Import Product Image from CSV File""",
    'description': """Import Product Image and ecommerce product category from CSV File(Web URL/File Path) """,
    'category': 'Sales',
    'depends': ['sale', 'website_sale'],
    'data': [
        'views/import_product_image_view.xml',
       'views/import_product_categ_image_view.xml',
        ],
    'images': ['static/description/banner.jpg'],
    'application': False,
    'installable': True,
    'auto_install': False,
}
