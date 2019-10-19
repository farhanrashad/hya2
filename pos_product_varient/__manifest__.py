# -*- coding: utf-8 -*-

{
    'name': 'POS Product template/variant',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Webveer',
    'summary': 'Product template manage multiple variants of single products in POS screen easily and manage Alternative/Suggestion Products',
    'description': """

=======================

Product template manage multiple variants of single products in POS screen easily and manage Alternative/Suggestion Products.

""",
    'depends': ['point_of_sale'],
    'data': [
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/product_v.png',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 15,
    'currency': 'EUR',
}
