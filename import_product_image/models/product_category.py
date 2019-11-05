# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import csv
import urllib.request as urllib2
import base64

import io
import sys
from odoo.exceptions import Warning
from odoo.tools import pycompat


class ProductCategImageImportWizard(models.TransientModel):
    _name = 'import.product_categ_image'

    function = fields.Selection(
        [('create', 'Create'), ('update', 'Update')], string="Product Category Operation", default='create')
    data_file = fields.Binary('Data File', required=True)

    @api.multi
    def import_csv_data(self):
        content = base64.decodestring(self.data_file)
        reader = pycompat.csv_reader(io.BytesIO(
            content), quotechar='"', delimiter=',')
        # First Row of the csv as a header or fields.
        fields = next(reader)
        # Read Data from second row.
        product_obj = self.env['product.public.category']
        for row in reader:
            product_name = row[0]
            image_path = row[1]
            if "http://" in image_path or "https://" in image_path:
                try:
                    link = urllib2.urlopen(image_path).read()
                    image_base64 = base64.encodestring(link)
                    product_id = product_obj.search(
                        [('name', '=', product_name)])

                    vals = {
                        'image_medium': image_base64,
                        'name': product_name,
                    }

                    if self.function == 'create' and not product_id:
                        product_obj.create(vals)
                    elif self.function == 'create' and product_id:
                        product_id.write(vals)
                    elif self.function == 'update' and product_id:
                        product_id.write(vals)
                    elif not product_id and self.function == 'update':
                        raise Warning(
                            "Could not find the product '%s'" % product_name)
                except:
                    raise Warning(
                        "Please provide correct URL for product '%s' or check your image size.!" % product_name)
            else:
                try:
                    with open(image_path, 'rb') as image:
                        image_base64 = base64.b64encode(image.read())
                        product_id = product_obj.search(
                            [('name', '=', product_name)])
                        vals = {
                            'image_medium': image_base64,
                            'name': product_name,
                        }
                        if self.function == 'create' and not product_id:
                            product_obj.create(vals)
                        elif self.function == 'create' and product_id:
                            product_id.write(vals)
                        elif self.function == 'update' and product_id:
                            product_id.write(vals)
                        elif not product_id and self.function == 'update':
                            raise Warning(
                                "Could not find the product '%s'" % product_name)
                except IOError:
                    raise Warning("Could not find the image '%s' - please make sure it is accessible to this script" %
                                  product_name)
