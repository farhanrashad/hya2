odoo.define('pos_pro_pack.pos_pro_pack', function (require) {
"use strict";

var models = require('point_of_sale.models');
var chrome = require('point_of_sale.chrome');
var core = require('web.core');
var PosPopWidget = require('point_of_sale.popups');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var gui = require('point_of_sale.gui');
var screens = require('point_of_sale.screens');
var _t = core._t;

models.load_fields('product.product',['is_pack','is_fix_pack','is_selective_pack','fixed_selective_pack','item_limit','fix_pack_id','selective_pack_id']);

models.load_models([{
        model: 'fix.product.pack',
        condition: function(self){ return self.config.allow_product_pack; },
        fields: ['product_id','qty'],
        loaded: function(self,result){
            if(result.length){
                self.wv_fix_pack_list = result;
            }
            else{
                self.wv_fix_pack_list = [];
            }
        },
    },{
        model: 'selective.product.pack',
        condition: function(self){ return self.config.allow_product_pack; },
        fields: ['product_id','default_selected','qty'],
        loaded: function(self,result){
            if(result.length){
                self.wv_selective_pack_list = result;
            }
            else{
                self.wv_selective_pack_list = [];
            }
        },
    },
    ],{'after': 'product.product'});

    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr,options){
            var self = this;
            OrderlineSuper.prototype.initialize.apply(this, arguments);
            
            var fix_products = false;
            if(options.product && options.product.is_pack && options.product.is_fix_pack){
                fix_products = options.product.fix_pack_id || false;
            }
            this.fix_product_ids = fix_products;

           
        },
        fixed_product_pack: function(pack_id,qty,unit){
            var self = this;
            var fixed_product = self.pos.wv_fix_pack_list;
            for(var i=0;i<fixed_product.length;i++){
                if(fixed_product[i].id == pack_id){
                    return "<em>"+fixed_product[i].qty * qty+"</em> "+fixed_product[i].product_id[1];
                }
            }
        },

        selected_product_pack: function(pack_id,qty,unit){
            var self = this;
            var selected_pack = self.pos.wv_selective_pack_list;
            for(var i=0;i<selected_pack.length;i++){
                if(selected_pack[i].id == pack_id){
                    return "<em>"+selected_pack[i].qty * qty+"</em> "+selected_pack[i].product_id[1];
                }
            }
        },
        fixed_product_pack_json: function(pack_id){
            var self = this;
            var fixed_product = self.pos.wv_fix_pack_list;
            for(var i=0;i<fixed_product.length;i++){
                if(fixed_product[i].id == pack_id){
                    return "<em>"+fixed_product[i].qty * qty+"</em> "+fixed_product[i].product_id[1];
                }
            }
        },
        selected_product_pack_json: function(pack_id){
            var self = this;
            var selected_pack = self.pos.wv_selective_pack_list;
            for(var i=0;i<selected_pack.length;i++){
                if(selected_pack[i].id == pack_id){
                    return {quantity:selected_pack[i].qty * this.quantity,product_id:selected_pack[i].product_id[0],discount:0,price_unit:0};
                }
            }
        },
        fixed_product_pack_json: function(pack_id){
            var self = this;
            var fixed_product = self.pos.wv_fix_pack_list;
            for(var i=0;i<fixed_product.length;i++){
                if(fixed_product[i].id == pack_id){
                    return {quantity:fixed_product[i].qty * this.quantity,product_id:fixed_product[i].product_id[0],discount:0,price_unit:0};
                }
            }
        },
        export_as_JSON: function(){
            var fixed_product_list = [];
            if(this.fix_product_ids){
                for(var i=0;i<this.fix_product_ids.length;i++){
                    fixed_product_list.push([0, 0, this.fixed_product_pack_json(this.fix_product_ids[i])]);
                }
            }
            var selected_product_list = [];
            if(this.selective_product_ids){
                for(var i=0;i<this.selective_product_ids.length;i++){
                    selected_product_list.push([0, 0, this.selected_product_pack_json(this.selective_product_ids[i])]);
                }
            }
            var data = OrderlineSuper.prototype.export_as_JSON.apply(this, arguments);
            data.fixed_product_list = fixed_product_list;
            data.selected_product_list = selected_product_list;
            return data;
        }
    });

    var SelectiveProductWidget = PosPopWidget.extend({
        template: 'SelectiveProductWidget',

        renderElement: function(options){
            var self = this;
            this._super();
            this.$(".add_modifiers").click(function(){
                var selected_product_list = [];
                $(".wv_product").each(function() {
                    if($(this).hasClass('dark-border')){
                        var product_id = $(this).data('product-id');
                        // var amount = $(this).data('product-amount');
                        selected_product_list.push(product_id);
                    }
                });
                var p_id = $('.base_product').data('product-id');
                if(p_id){
                    if(! options.edit_pack){
                        self.pos.get_order().add_product(self.pos.db.get_product_by_id(p_id));
                    }
                    self.pos.get_order().selected_orderline.selective_product_ids = selected_product_list;
                    self.pos.get_order().selected_orderline.trigger('change',self.pos.get_order().selected_orderline);
                }
                self.gui.show_screen('products');
            });
            $(".wv_product").click(function() {
                if($(this).hasClass('dark-border')){
                    $(this).removeClass('dark-border');
                }
                else{
                    var count = 0;
                    var total = $('.base_product').data('count');
                    $(".wv_product").each(function() {
                        if($(this).hasClass('dark-border')){
                           count = count + 1;
                        }
                    });
                    if(count < total){
                        $(this).addClass('dark-border');
                    }
                    else{
                        alert("Sorry you can add only "+total+" products")
                    }
                }
            });
        },
        show: function(options){
            var self = this;
            this.options = options || {};
            var product_pack_list = [];
            var fixed_product_list= [];
            var fixed_product = this.pos.wv_fix_pack_list;
            var wv_selective_pack = this.pos.wv_selective_pack_list;
            if(options.product.is_fix_pack){
                var pack_ids = options.product.fix_pack_id;
                for(var i=0;i<fixed_product.length;i++){
                    if(pack_ids.indexOf(fixed_product[i].id)>=0){
                        fixed_product_list.push(fixed_product[i]);
                    }
                }
                options.fixed_product_list = fixed_product_list;
            }
            var pack_ids = options.product.selective_pack_id;
            for(var i=0;i<wv_selective_pack.length;i++){
                if(pack_ids.indexOf(wv_selective_pack[i].id)>=0){
                    product_pack_list.push(wv_selective_pack[i]);
                }
            }
            options.product_pack_list = product_pack_list;
            this._super(options); 
            this.renderElement(options);
        },
    });

    gui.define_popup({
        'name': 'selective-product-widget', 
        'widget': SelectiveProductWidget,
    });
    var OrderlineEditPackButton = screens.ActionButtonWidget.extend({
        template: 'OrderlineEditPackButton',
        button_click: function(){
            var line = this.pos.get_order().get_selected_orderline();
            if(line){
                if(line.product.is_pack && line.product.is_selective_pack){
                    this.gui.show_popup('selective-product-widget',{'product':line.product,'edit_pack':true});
                }
            }
        },
    });

    screens.define_action_button({
        'name': 'order_line_edit_pack',
        'widget': OrderlineEditPackButton,
        'condition': function(){
            return this.pos.config.allow_product_pack;
        },
    });
    screens.ProductScreenWidget.include({
        click_product: function(product) {
           if(product.to_weight && this.pos.config.iface_electronic_scale){
               this.gui.show_screen('scale',{product: product});
           }else{
                if(this.pos.config.allow_product_pack && product.is_pack && product.is_selective_pack){
                    this.gui.show_popup('selective-product-widget',{'product':product,'edit_pack':false});
                }
                else{
                    this.pos.get_order().add_product(product);
                }
            }
        },

    });
});

