 # -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductPublicCategoryExt(models.Model):
    _inherit = 'product.public.category'

    pnc_number = fields.Char('PNC Number')
    product_public_category_lines = fields.One2many('product.public.category.line', 'product_public_category_id')
    no_of_products = fields.Integer(compute='_no_of_products')

    @api.one
    def _no_of_products(self):
        product_count = 0
        for rec in self.product_public_category_lines:
            product_count += len(
                self.env['product.template'].search(
                    [('pnc_number', '!=', 'False'), ('pnc_number', '=', rec.pnc_number)]).mapped('id'))
        self.no_of_products = product_count

    @api.multi
    def open_products(self):
        domain = []
        for rec in self.product_public_category_lines:
            domain.append(rec.pnc_number)
        return {
            'name': _('Products'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('pnc_number', 'in', domain), ('pnc_number', '!=', 'False')],
        }

    

    @api.multi
    def write(self, vals):
        rec = super(ProductPublicCategoryExt, self).write(vals)
        lines = self.env['product.public.category.line'].search(
            [('product_public_category_id', '=', self.id), ('is_linked', '!=', True)])
        for line in lines:
            for product in self.env['product.template'].search([('pnc_number', '=', line.pnc_number)]):
                product.public_categ_ids = [(4, self.id)]
            line.is_linked = True
        return rec


class ProductPublicCategoryLineExt(models.Model):
    _name = 'product.public.category.line'
    _descripttion = "Product Public Category Line"

    name = fields.Char("Name")
    pnc_number = fields.Char("PNC Number")
    product_id = fields.Many2one('product.template', 'Product', store=True)
    is_linked = fields.Boolean(string="Category attached", default=False)
    product_public_category_id = fields.Many2one('product.public.category')
