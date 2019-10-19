# -*- coding: utf-8 -*-
from odoo import http

# class ECommerceExt(http.Controller):
#     @http.route('/e_commerce_ext/e_commerce_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/e_commerce_ext/e_commerce_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('e_commerce_ext.listing', {
#             'root': '/e_commerce_ext/e_commerce_ext',
#             'objects': http.request.env['e_commerce_ext.e_commerce_ext'].search([]),
#         })

#     @http.route('/e_commerce_ext/e_commerce_ext/objects/<model("e_commerce_ext.e_commerce_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('e_commerce_ext.object', {
#             'object': obj
#         })