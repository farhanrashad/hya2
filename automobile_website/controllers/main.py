from addons.http_routing.models.ir_http import slug
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import UserError


class Website(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        public_category = request.env['product.public.category'].sudo()
        row_category_data = request.env['row.category.data'].sudo()
        categories = public_category.search([('parent_id', '=', False)])

        row_ids = row_category_data.search([])
        # Model No List
        model_code = filter(None, list(
            set([x.model_code for x in row_ids])))

        # Get all producut
        product_template_ids = request.env['product.template'].sudo().search([])
        product_ids = product_template_ids.filtered(lambda r: r.pnc_no != False)

        # Grade List
        grade_list = filter(None, list(
            set([x.grade for x in product_template_ids])))

        # Engine List
        engine_list = filter(None, list(
            set([x.engine_no for x in product_template_ids])))

        # Model List
        model_list = filter(None, list(
            set([x.model.strip() for x in product_template_ids if x.model])))

        # Product List
        pnc_no, product_rec = [], []
        for rec in product_ids:
            if rec.pnc_no not in pnc_no:
                product_rec.append(rec.id)
                pnc_no.append(rec.pnc_no)
        product_list = product_ids.filtered(lambda x: x.id in product_rec)
        values = {
            'categories': categories,
            'grade_list': grade_list,
            'engine_list': engine_list,
            'product_list': product_list,
            'model_list': model_list,
            'model_code': model_code,
        }
        return request.render("automobile_website.automobile_home_page1", values)


class WebsiteAutomobile(http.Controller):

    @http.route(['/shop/row', '/shop/row/<model("product.public.category"):category>'], type='http', auth="public", website=True)
    def shop_page_row(self, category=False, search='', search_frame='', parent_category=0, **post):
        values = {}
        if category.child_id:
            categories = category.child_id
            values = {
                'categories': categories,
                'parent_category': category
            }
        return request.render("automobile_website.automobile_shop_page", values)

    @http.route(['/shop', '/shop/<model("product.public.category"):category>'], type='http', auth="public", website=True)
    def shop_page(self, category=False, search='', search_frame='', parent_category=0, **post):
        public_category = request.env['product.public.category'].sudo()
        if search_frame:
            categories = public_category.search(
                [('name', 'ilike', search_frame)])
            values = {
                'categories': categories
            }
        elif search and not parent_category:
            categories = public_category.search(
                [('name', 'ilike', search), ('parent_id', '=', False)])
            values = {
                'categories': categories
            }
        elif parent_category and search:
            categories = public_category.search(
                [('name', 'ilike', search), ('parent_id', '=', int(parent_category))])
            parent_category = public_category.search(
                [('id', '=', int(parent_category))])
            values = {
                'categories': categories,
                'parent_category': parent_category
            }
        elif category and not search:
            if category.display_mode == 'row':
                values = {'category': category,
                          'row_categories': category.row_categ_lines}
                return request.render("automobile_website.automobile_row_categ_page", values)
            if category.child_id:
                categories = category.child_id
                values = {
                    'categories': categories,
                    'parent_category': category
                }
            elif category.display_mode == 'img_mapping':
                return request.redirect("/category/%s" % slug(category))
            else:
                return request.redirect("/shop/category/%s" % slug(category))
        else:
            categories = public_category.search([('is_car', '=', True)])
            values = {
                'categories': categories
            }
        return request.render("automobile_website.automobile_shop_page", values)

    @http.route(['/category/<model("product.public.category"):category>'], type='http', auth="public",
                website=True)
    def product_page(self, category=False, **post):
        products = request.env['product.template'].sudo().search(
            [('public_categ_ids', '=', category.id)])
        values = {
            'category': category,
            'products': products
        }
        request.session['category'] = category.id
        return request.render("automobile_website.product_details", values)

    @http.route(['/create_new_image/<model("product.public.category"):category>'], type='http', auth="public",
                website=True)
    def create_image(self, category=False, **post):
        if category:
            products = request.env['product.template'].sudo().search(
                [('public_categ_ids', '=', category.id)])
            values = {
                'category': category,
                'products': products
            }
            categ_image = request.env['category.image.html'].sudo().search(
                [('category_id', '=', category.id)])
            if categ_image:
                values['image_id'] = categ_image
        return request.render("automobile_website.automobile_create_image_page", values)

    @http.route(['/create_product_image'], type='json', auth="public", website=True)
    def create_category_image(self, category_id=0, image_html=False, **kw):
        if category_id and image_html and kw.get('product_list'):
            category_image_html_obj = request.env['category.image.html'].sudo()
            category_image_html_id = category_image_html_obj.search(
                [('category_id', '=', int(category_id))])
            if category_image_html_id:
                category_image_html_id.sudo().write({
                    'html_data': image_html
                })
            else:
                category_image_html_id = request.env['category.image.html'].sudo().create({
                    'category_id': int(category_id),
                    'html_data': image_html
                })
            for each in kw.get('product_list'):
                product = request.env['product.image.create'].sudo().search([('product_id', '=', each),
                                                                             ('category_image_id', '=',
                                                                              category_image_html_id.id)])
                if not product:
                    request.env['product.image.create'].sudo().create({
                        'product_id': each,
                        'category_image_id': category_image_html_id.id
                    })

            return True

    @http.route(['/update/cart/new'], type='json', auth="public", website=True)
    def add_product_cart(self, product_id=0, qty=1, **kw):
        if product_id:
            request.website.sale_get_order(force_create=1)._cart_update(
                product_id=int(product_id),
                add_qty=int(qty),
                set_qty=0,
            )
        return True

    @http.route(['/shop/category/product/<model("product.template"):product>'], type='http', auth="public",
                website=True)
    def product(self, product, **kwargs):
        category = request.env['product.public.category'].sudo().search(
            [('id', '=', request.session.get('category'))])
        values = {
            'product': product,
            'category': category,
        }
        return request.render("automobile_website.automobile_product_page", values)

    @http.route(['/get_grade_list'], type='json', auth="public", website=True)
    def get_grade_list(self, car=False, grade_id=0, **kw):
        if car:
            grade_list = []
            product_list = []
            year_list = []
            engine_list = []

            # # Row Data
            # row_category_data = request.env['row.category.data'].sudo().search([])
            # # Grade List
            # grade_list = filter(None, list(
            #     set([x.grade for x in row_category_data])))
            # # Engine List
            # engine_list = filter(None, list(
            #     set([x.engine for x in row_category_data])))
            # # Model List
            # model_list = filter(None, list(
            #     set([x.model_code for x in row_category_data])))

            # product_template = request.env['product.template'].sudo()
            # product_ids = product_template.search([('pnc_no', '!=', False)])
            # # Product List
            # pnc_no, product_rec = [], []
            # for rec in product_ids:
            #     if rec.pnc_no not in pnc_no:
            #         product_rec.append(rec.id)
            #         pnc_no.append(rec.pnc_no)
            # product_list = product_ids.filtered(lambda x: x.id in product_rec)
            # return request.render("automobile_website.automobile_home_page1", values)
            products = request.env['product.template'].sudo().search([('model', '=', car)])

            # Product List
            pnc_no, product_list = [], []

            for rec in products:
                if rec.pnc_no not in pnc_no:
                    product_list.append({
                        'value': rec.id,
                        'name': rec.name
                    })
                    pnc_no.append(rec.pnc_no)
            # Grade List
            grade_list = filter(None, list(
                set([x.grade for x in products])))

            grade_list = [x for x in grade_list]
            # Engine List
            engine_list = filter(None, list(
                set([x.engine_no for x in products])))
            engine_list = [x for x in engine_list]

            # Model List
            model_list = filter(None, list(
                set([x.model for x in products])))
            model_list = [x for x in model_list]
            # Year List
            year_list = filter(None, list(
                set([x.model_year for x in products])))
            year_list = [x for x in year_list]

            # category = request.env['product.public.category'].sudo().search([
            #     ('id', '=', int(id))])
            # products = request.env['product.template'].sudo().search([])
            # for product in products:
            #     for categ in product.public_categ_ids:
            #         if category.name in categ.display_name:
            #             product_list.append({
            #                 'value': product.id,
            #                 'name': product.name
            #             })
            #             if product.model:
            #                 grade_list.append(product.model)
            #             if product.model_year:
            #                 year_list.append(product.model_year)
            #             if product.engine_no:
            #                 engine_list.append(product.engine_no)
            # engine_list = set(engine_list)
            # engine_list = list(engine_list)
            # grade_list = set(grade_list)
            # grade_list = list(grade_list)
            # year_list = set(year_list)
            # year_list = list(year_list)
            return {'grade_list': grade_list, 'product_list': product_list, 'year_list': year_list, 'engine_list': engine_list}

        if grade_id:
            product_list = []
            category = request.env['product.public.category'].sudo().search(
                [('id', '=', int(grade_id))])
            products = request.env['product.template'].sudo().search([])
            for product in products:
                for categ in product.public_categ_ids:
                    if category.name in categ.display_name:
                        product_list.append({
                            'value': product.id,
                            'name': product.name
                        })

            return {'product_list': product_list}

    @http.route(['/search'], type='http', auth="public", website=True)
    def search_page(self, **post):
        product_template = request.env['product.template'].sudo()
        domain = []
        category = False
        values = {}
        # Search with frame model 2nd type search
        if post.get('search_frame'):
            frame_detail_data = request.env['frame.detail.data'].sudo().search([])
            frame_model_code = post.get('search_frame')
            if frame_model_code:
                content = frame_model_code.split('-')
                frame_model_code = content[0]
                try:
                    from_frame_no = int(content[1])
                except:
                    values['error'] = 'Invalid Frame Number'
                    return request.render('automobile_website.automobile_search_page', values)
                frame_detail_data = frame_detail_data.filtered(
                    lambda r: r.frame_model == frame_model_code and r.from_frame_no <= from_frame_no and r.to_frame_no > from_frame_no)
            if frame_detail_data and len(frame_detail_data) == 1:
                category = frame_detail_data.e_categ_id
                if category:
                    lines = category.frame_data_ids.filtered(
                        lambda r: r.id == frame_detail_data.id)
                    values = {
                        'category': category,
                        'frame_data_lines': lines,
                        'search_frame': post.get('search_frame', ''),
                        'search_result': True
                    }
                    return request.render("automobile_website.automobile_row_categ_page", values)
            return request.render('automobile_website.automobile_search_page', False)

        # Search with partnumber
        if post.get('part_number'):
            products = product_template.search(
                [('display_code', 'ilike', post.get('part_number'))])
            value = {
                'products': products
            }
            return request.render('automobile_website.automobile_search_page', value)

        # Search With Car/Grade/Year/Engine and Product
        if post.get('car_selection'):
            # category = request.env['product.public.category'].sudo().search(
            #     [('id', '=', int(post.get('car_selection')))])

            products = product_template.search(
                [('model', '=', post.get('car_selection'))])
            product_list = []
            # for product in products:
            #     for categ in product.public_categ_ids:
            #         if category.name in categ.display_name:
            #             product_list.append(product.id)
            domain.append(('model', '=', post.get('car_selection')))
        if post.get('grade_selection'):
            domain.append(('grade', 'ilike', str(post.get('grade_selection'))))
        if post.get('year_selection'):
            domain.append(
                ('model_year', 'ilike', str(post.get('year_selection'))))
        if post.get('engine_selection'):
            domain.append(('engine_no', '=', post.get('engine_selection')))
        if post.get('product_selection'):
            product_pnc = product_template.browse(
                int(post.get('product_selection')))
            domain.append(('pnc_no', 'ilike', product_pnc.pnc_no))
        products = product_template.search(domain)
        if len(products) == 1:
            values = {
                'product': products,
                'category': products.public_categ_ids,
            }
            return request.render("automobile_website.automobile_product_page", values)
        else:
            value = {
                'products': products
            }
            return request.render('automobile_website.automobile_search_page', value)

    @http.route(['/reset_image'], type='json', auth="public", website=True)
    def reset_image(self, id=0, **kw):
        if id:
            image_id = request.env['category.image.html'].sudo().search(
                [('category_id', '=', int(id))])
            if image_id:
                for each in image_id:
                    each.unlink()
        return True
