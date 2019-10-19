# -*- coding: utf-8 -*-


from odoo import fields, models,tools,api
import logging

class product_template(models.Model):
    _inherit = 'product.template'

    alternative_products_id = fields.Many2many(comodel_name='product.product',relation='product_temp_product',column1='product_temp_id',column2='product_id', string="Alternative Products")


    