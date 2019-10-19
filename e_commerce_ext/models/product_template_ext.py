# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplateExt(models.Model):
    _inherit = 'product.template'


    pnc_number = fields.Char('PNC Number')