from addons.http_routing.models.ir_http import slug
from odoo import fields, models, api
from odoo import http

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urlparse import urlparse, parse_qsl, urlunparse, urljoin

except ImportError:
    from urllib.parse import urlparse, parse_qsl, urlunparse, urljoin
import urllib.request
import logging
import base64
import string

_logger = logging.getLogger(__name__)


class CategoryImageHtml(models.Model):
    _name = 'category.image.html'

    category_id = fields.Many2one('product.public.category', string="Category")
    html_data = fields.Text(string='HTML Data')
    product_image_ids = fields.One2many(
        'product.image.create', 'category_image_id', string="Products")


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    is_last_category = fields.Boolean(string="Last Category")
    categ_url_image = fields.Char(string="Category Image Url")
    display_mode = fields.Selection([
        ('normal', 'Normal'),
        ('without_img', 'Without Image'),
        ('conversion', 'Conversion'),
        ('img_mapping', 'Image Mapping'),
        ('row', 'Row'),
    ], string="Display Mode")
    mapping_image = fields.Binary(string="Mapping Image")
    map_image_url = fields.Char(string="Mapping Image Url")
    url_image = fields.Char(string="Url")
    is_frame_no = fields.Boolean(string="Frame Number")
    reference_urls = fields.One2many(
        'reference.url', 'category_id', string="Reference URL")
    is_have_chart = fields.Boolean(string="Search Frame")
    image2 = fields.Binary(string="Image2")
    row_categ_lines = fields.One2many(
        'row.category.data', 'categ_id', string="Category")
    frame_data_ids = fields.One2many('frame.detail.data', 'e_categ_id', string='Frame Details')
    is_car = fields.Boolean(string="Car Brand")
    is_a_car = fields.Boolean(string="Is a Car")

    @api.multi
    def create_image(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/create_new_image/%s' % slug(self),
            'target': 'self',
            'res_id': self.id,
        }

    @api.multi
    def write(self, vals):
        res = super(ProductPublicCategory, self).write(vals)
        if 'categ_url_image' in vals and vals['categ_url_image'] != '':
            temp_file, temp_header = urllib.request.urlretrieve(
                vals['categ_url_image'])
            fo = open(temp_file, "rb")
            bindata = base64.b64encode(fo.read())
            self.image = bindata
        if 'map_image_url' in vals and vals['map_image_url'] != '':
            temp_file, temp_header = urllib.request.urlretrieve(
                vals['map_image_url'])
            fo = open(temp_file, "rb")
            bindata = base64.b64encode(fo.read())
            self.mapping_image = bindata
        return res

    @api.model
    def create(self, vals):
        res = super(ProductPublicCategory, self).create(vals)
        if 'categ_url_image' in vals and vals['categ_url_image'] != '':
            temp_file, temp_header = urllib.request.urlretrieve(
                vals['categ_url_image'])
            fo = open(temp_file, "rb")
            bindata = base64.b64encode(fo.read())
            self.image = bindata
        if 'map_image_url' in vals and vals['map_image_url'] != '':
            temp_file, temp_header = urllib.request.urlretrieve(
                vals['map_image_url'])
            fo = open(temp_file, "rb")
            bindata = base64.b64encode(fo.read())
            self.mapping_image = bindata
        return res

    def get_year_list(self):
        year_list = []
        data = self.env['product.template'].sudo().search(
            [('model_year', '!=', '')])
        for each in data:
            year_list.append(each.model_year)
        new_list = set(year_list)
        year_list = list(new_list)
        return sorted(year_list)

    def get_engine_list(self):
        engine_list = []
        data = self.env['product.template'].sudo().search(
            [('chases_no', '!=', '')])
        for each in data:
            engine_list.append(each.chases_no)
        new_list = set(engine_list)
        engine_list = list(new_list)
        return sorted(engine_list)

    def get_part_list(self):
        part_list = []
        data = self.env['product.template'].sudo().search(
            [('display_code', '!=', '')])
        for each in data:
            part_list.append(each.display_code)
        new_list = set(part_list)
        part_list = list(new_list)
        return sorted(part_list)


class ReferenceUrl(models.Model):
    _name = 'reference.url'

    label = fields.Char(string="Label")
    url = fields.Char(string="URL")
    category_id = fields.Many2one('product.public.category', string="Category")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    display_code = fields.Char(string="Part No.")
    pnc_no = fields.Char(string="PNC No.")
    chases_no = fields.Char(string="Chases No.")
    model = fields.Char(string="Model")
    model_year = fields.Char(string="Model Year")
    model_desc = fields.Char(string="Model Description")
    subs = fields.Char(string="SUBS")
    part_qty = fields.Integer(string="Part Quantity")
    grade = fields.Char(string="Grade")


class ProductImage(models.Model):
    _name = 'product.image.create'

    category_image_id = fields.Many2one(
        'category.image.html', string="Category Image")
    product_id = fields.Many2one('product.template', string="Product")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    description = fields.Text(string="Description")


class row_category_data(models.Model):
    _name = 'row.category.data'

    categ_id = fields.Many2one(
        'product.public.category', string="Public Category")
    # frame_no = fields.Many2one(
    #     'product.public.category', string="Ecommerce Category")
    category_frame = fields.Char(string='Frame No.')
    model_code = fields.Char(string="MODEL CODE")
    car_name = fields.Char(string="CAR NAME")
    production_from = fields.Char(string="PRODUCTION FROM")
    production_to = fields.Char(string="PRODUCTION TO")
    destination = fields.Char(string="DESTINATION")
    driver_position = fields.Char(string="DRIVER POSITION")
    grade = fields.Char(string="GRADE")
    engine = fields.Char(string="ENGINE")
    transmission = fields.Char(string="TRANSMISSION")
    gear_shift_type = fields.Char(string="GEAR SHIFT TYPE")
    color_code = fields.Char(string="COLOR CODE")
    trim_code = fields.Char(string="TRIM CODE")


class frame_detail_data(models.Model):
    _name = 'frame.detail.data'

    e_categ_id = fields.Many2one('product.public.category', string="Public Category")
    frame_model = fields.Char(string="Frame Model")
    model_year = fields.Char(string='Year')
    from_frame_no = fields.Integer(string='From Frame No')
    to_frame_no = fields.Integer(string='To Frame No')
    production_date = fields.Char(string='Production Date')
    engine = fields.Char(string='Engine')
    month_range = fields.Selection([(x, x) for x in range(13) if x], string='Month', store=True)
    field1 = fields.Char()
    field2 = fields.Char()
