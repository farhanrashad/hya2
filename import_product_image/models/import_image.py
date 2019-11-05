# -*- coding: utf-8 -*-

import csv
import urllib.request as urllib2
import base64
import io
import sys
from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.tools import pycompat


class ProductImageImportWizard(models.TransientModel):
    _name = 'import.product_image'

    product_model = fields.Selection([('1', 'Product Template'), ('2', 'Product Variants')], string="Product Model")
    pdt_operation = fields.Selection([('1', 'Product Creation'), ('2', 'Product Updation')], string="Product Operation")
    file = fields.Binary('File to import', required=True)

    @api.multi
    def import_file(self):
        content = base64.decodestring(self.file)
        reader = pycompat.csv_reader(io.BytesIO(content), quotechar='"', delimiter=',')
        fields = next(reader)
        for row in reader:
            product = row[0]
            image_path = row[1]
            if "http://" in image_path or "https://" in image_path:
                try:
                    link = urllib2.urlopen(image_path).read()
                    image_base64 = base64.encodestring(link)
                    if self.product_model == '1':
                        product_obj = self.env['product.template']
                    else:
                        product_obj = self.env['product.product']
                    product_id = product_obj.search([('name', '=', product)])

                    vals = {
                        'image_medium': image_base64,
                        'name': product,
                    }

                    if self.pdt_operation == '1' and not product_id:
                        import pdb; pdb.set_trace()
                        product_obj.create(vals)
                    elif self.pdt_operation == '1' and product_id:
                        product_id.write(vals)
                    elif self.pdt_operation == '2' and product_id:
                        product_id.write(vals)
                    elif not product_id and self.pdt_operation == '2':
                        raise Warning("Could not find the product '%s'" % product)
                except:
                    raise Warning("Please provide correct URL for product '%s' or check your image size.!" % product)
            else:
                try:
                    with open(image_path, 'rb') as image:
                        image_base64 = image.read().encode("base64")
                        if self.product_model == '1':
                            product_obj = self.env['product.template']
                        else:
                            product_obj = self.env['product.product']
                        product_id = product_obj.search([('name', '=', product)])
                        vals = {
                            'image_medium': image_base64,
                            'name': product,
                        }
                        if self.pdt_operation == '1' and not product_id:
                            product_obj.create(vals)
                        elif self.pdt_operation == '1' and product_id:
                            product_id.write(vals)
                        elif self.pdt_operation == '2' and product_id:
                            product_id.write(vals)
                        elif not product_id and self.pdt_operation == '2':
                            raise Warning("Could not find the product '%s'" % product)
                except IOError:
                    raise Warning("Could not find the image '%s' - please make sure it is accessible to this script" %
                                  product)
