# -*- coding: utf-8 -*-
{
    'name': "Theme Modifiction",

    'summary': """
    Modify Default Theme
        """,

    'description': """
        Modify Default Theme Look & Feel
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'website',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website','website_sale','product_tiered_pricing'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}