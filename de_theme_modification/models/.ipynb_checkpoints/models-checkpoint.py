# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Company(models.Model):
    _inherit = 'res.company'

    secondary_logo = fields.Binary("Secondary Logo", attachment=True, help="This field holds the secondary logo used in website",)

class Website(models.Model):
    _inherit = 'website'

    msg = fields.Char(string='Message', help='Display message at top header on website.')