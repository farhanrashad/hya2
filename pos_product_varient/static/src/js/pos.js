odoo.define('pos_product_varient.pos_product_varient', function (require) {
"use strict";
	var module = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var PosPopWidget = require('point_of_sale.popups');
    var PosDB = require('point_of_sale.DB');
    var models = module.PosModel.prototype.models;
    var modelss = require('point_of_sale.models');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var QWeb = core.qweb;
    var _t = core._t;

    PosDB.include({
        init: function(options){
            this.product_template = [];
            this.template_by_id = {};
            this.product_attribute_by_id = {};
            this.product_attribute_value_by_id = {};
            this._super(options);
        },
        get_products_by_template: function(template_id){
            return this.template_by_id[template_id];     
        },

        add_templates: function(templates){
            for(var i=0 ; i < templates.length; i++){
                var attribute_value_ids = [];
                this.template_by_id[templates[i].id] = templates[i];
                for (var j = 0; j <templates[i].product_variant_ids.length; j++){
                    var product = this.product_by_id[templates[i].product_variant_ids[j]]
                    for (var k = 0; k < product.attribute_value_ids.length; k++){
                        if (attribute_value_ids.indexOf(product.attribute_value_ids[k])==-1){
                            attribute_value_ids.push(product.attribute_value_ids[k]);
                        }
                    }
                    product.product_variant_count = templates[i].product_variant_count;
                    product.is_primary_variant = (j==0);
                }
                this.template_by_id[templates[i].id].attribute_value_ids = attribute_value_ids;
            }
        },
    });

    screens.ProductListWidget.include({
        init: function(parent, options) {
            var self = this;
            this._super(parent,options);
            this.click_product_handler = function(){
                var product = self.pos.db.get_product_by_id(this.dataset.productId);
                if (product.product_variant_count == 1) {
                    options.click_product_action(product);
                }
                else{
                    var product_list = self.pos.db.get_products_by_template(product.product_tmpl_id);
                    var products_list = [];
                    var product_temp = product_list.product_variant_ids;
                    var alternative_list = []
                    for(var i=0;i<product_temp.length;i++){
                        products_list.push(self.pos.db.get_product_by_id(product_temp[i]))
                    }
                    var alternative = product_list.alternative_products_id;
                    for(var i=0;i<alternative.length;i++){
                        alternative_list.push(self.pos.db.get_product_by_id(alternative[i]))
                    }
                    self.gui.show_popup('select-variant-popup',{'products':products_list,'alternative':alternative_list,'pricelist':self.pos.get_order().pricelist});
                }
            };
        },
        set_product_list: function(product_list){
            for (var i = product_list.length - 1; i >= 0; i--){
                if (!product_list[i].is_primary_variant){
                    product_list.splice(i, 1);
                }
            }
            this._super(product_list);
        },

    });

    var SelectVariantPopupWidget = PosPopWidget.extend({
        template: 'SelectVariantPopupWidget',

        renderElement: function(){
            this._super(); 
            var self = this;
            $(".wv.product").click(function(){
                var product_id = $(this).attr('data-product-id');
                var product = self.pos.db.get_product_by_id(parseInt(product_id));
                self.pos.get_order().add_product(product);
                self.click_cancel();
            }); 
                
            },
        show: function(options){
            this.options = options || {};
            var self = this;
            this._super(options); 
            this.renderElement();
        },

        get_product_image_url: function(product){
            return window.location.origin + '/web/image?model=product.product&field=image_medium&id='+product.id;
        },
    });

    gui.define_popup({
        'name': 'select-variant-popup', 
        'widget': SelectVariantPopupWidget,
    });

    var _render_product_ = screens.ProductListWidget.prototype.render_product;
    screens.ProductListWidget.prototype.render_product = function(product){
        self = this;
        if (product.product_variant_count == 1){
            return _render_product_.call(this, product);
        }
        else{
            var cached = this.product_cache.get_node(product.id);
            if(!cached){
                var image_url = this.get_product_image_url(product);
                var product_html = QWeb.render('Template',{ 
                        widget:  this, 
                        product: product, 
                        image_url: this.get_product_image_url(product),
                    });
                var product_node = document.createElement('div');
                product_node.innerHTML = product_html;
                product_node = product_node.childNodes[1];
                this.product_cache.cache_node(product.id,product_node);
                return product_node;
            }
            return cached;
        }
    };

    for(var i=0; i<models.length; i++){
        var model=models[i];
        if(model.model === 'product.product'){
            if (model.fields.indexOf('name') == -1) {
                    model.fields.push('name');
                }
            if (model.fields.indexOf('attribute_value_ids') == -1) {
                model.fields.push('attribute_value_ids');
            }
        
        } 
    }

    modelss.load_models({
            model: 'product.template',
            fields: [
                'product_variant_ids',
                'product_variant_count',
                'alternative_products_id',
                ],
            domain:  function(self){
                return [
                    ['sale_ok','=',true],
                    ['available_in_pos','=',true],
                ];},
            context: function(self){
                return {
                    display_default_code: false,
                };},
            loaded: function(self, templates){
                 self.db.add_templates(templates);
            },
        });
});
