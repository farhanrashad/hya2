# -*- coding: utf-8 -*-
from odoo import http

# class DeThemeModification(http.Controller):
#     @http.route('/de_theme_modification/de_theme_modification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_theme_modification/de_theme_modification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_theme_modification.listing', {
#             'root': '/de_theme_modification/de_theme_modification',
#             'objects': http.request.env['de_theme_modification.de_theme_modification'].search([]),
#         })

#     @http.route('/de_theme_modification/de_theme_modification/objects/<model("de_theme_modification.de_theme_modification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_theme_modification.object', {
#             'object': obj
#         })