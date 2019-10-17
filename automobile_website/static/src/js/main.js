odoo.define('automobile_website.main', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    $(document).ready(function () {
        $('a[href="/shop"]').html("Catalog Of Parts");
        $('#shop_product_image .col-md-12.draggable_class.ui-widget-content').html("");
        $('#new_image .col-md-12.draggable_class.ui-widget-content').draggable();
        $('#new_image .reference_field').draggable();
        $(document).find('#new_image .reference_field').resizable();
        if (typeof $(document).find('.carousel-inner .reference_field').html() != 'undefined') {
            $('.carousel-inner .reference_field').each(function () {
                $(this).removeClass('ui-resizable');
                $(this).html('');
            });
        }
        $('.chart_table td a').on('mouseenter', function () {
            $(this).parents('tr').find('a').css({'background':'#337ab7','color':'#fff'})
        });
        $('.chart_table td a').on('mouseleave', function () {
            $(this).parents('tr').find('a').css({'background':'#fff','color':'#000'})
        });
        $('#copy_btn').click(function () {
            var html = $(document).find('.col-md-12.draggable_class.ui-widget-content.ui-draggable.ui-draggable-handle.variant_active_click').clone();
            $('.col-md-1.product_variants').append(html.removeAttr('style').css('background', 'transparent').removeClass('variant_active_click'));

            $('#new_image .col-md-12.draggable_class.ui-widget-content').draggable();

        });
        $('#create_image').on('click', function () {
            $("#new_image").find(".col-md-1.product_variants").addClass('image_added');
            var category_id = $('#category_id').val();
            var image_html = $('#new_image').html();
            var product_list = [];
            $('#new_image').find('.product_variants').find('.draggable_class.ui-widget-content').each(function () {
                product_list.push(parseInt($(this).attr('variant_id')))
            });
            ajax.jsonRpc("/create_product_image", 'call', {
                'image_html': image_html,
                'category_id': category_id,
                'product_list': product_list
            })
                .then(function (data) {
                    var url = '/web';
                    window.location.replace(url)
                });
        });
        $('.dropdown_sorty_by').remove();
        $('.col-md-12.draggable_class.ui-widget-content').on('mouseenter', function () {
            var id = "#product_" + $(this).attr('variant_id');
            $(document).find(id).addClass('variant_active');
            $(this).addClass('variant_active');
        }).mouseleave(function () {
            var id = "#product_" + $(this).attr('variant_id');
            $(document).find(id).removeClass('variant_active');
            $(this).removeClass('variant_active');
        });
        $('.col-md-12.draggable_class.ui-widget-content').on('click', function () {
            var id = "#product_" + $(this).attr('variant_id');
            $('.col-md-12.product_variant_box').each(function () {
                $(this).removeClass('variant_active_click')
            });
            $('.col-md-12.draggable_class.ui-widget-content').each(function () {
                $(this).removeClass('variant_active_click')
            });
            $(document).find(id).addClass('variant_active_click');
            $(this).addClass('variant_active_click');
        });
        $('.col-md-12.product_variant_box').on('mouseenter', function () {
            var id = ".product_box_" + $(this).attr('data');
            $('.col-md-12 .col-md-12.draggable_class.ui-widget-content').each(function () {
                $(this).removeClass('variant_active_click');
                $(this).removeClass('variant_active')
            });
            $(document).find(id).each(function () {
                $(this).addClass('variant_active');
            });
            $(this).addClass('variant_active');
        }).mouseleave(function () {
            var id = ".product_box_" + $(this).attr('data');
            $(this).removeClass('variant_active');
        });
        $('.col-md-12.product_variant_box').on('click', function () {
            var id = ".product_box_" + $(this).attr('data');
            $('.col-md-12.draggable_class.ui-widget-content').each(function () {
                $(this).removeClass('variant_active_click')
            });
            $('.col-md-12.product_variant_box').each(function () {
                $(this).removeClass('variant_active_click')
            });
            $(document).find(id).each(function () {
                $(this).addClass('variant_active_click');
            });
            $(this).addClass('variant_active_click');
        });
        $('.add_to_cart_variant').on('click', function () {
            var product_id = $(this).attr('product-id');
            var qty = $(this).parents('.col-md-12').find('.qty').val();
            console.log(product_id, qty)
            ajax.jsonRpc("/update/cart/new", 'call', {'product_id': product_id, 'qty': qty})
                .then(function (data) {
                    window.location.reload()
                });
        });
        $('input.search_frame').on('change', function() { 
            
            // 1
            var $this = $(this);
            var input = $this.val();
            if (!/[\-]/.test(input))
            {
                // 2
                input = input.replace(/[\W\s\._]+/g, '');
                 
                // 3
                var split = 4;
                var chunk = [];
                 
                for (var i = 0, len = input.length; i < len; i += split) {
                    split = ( i >= 6 && i <= 14 ) ? 7 : 6;
                    if(chunk.length < 2){
                        chunk.push( input.substr( i, split ) ); 
                    }
                }
                 
                // 4
                $this.val(function() {
                    return chunk.join("-");
                });
            } 
        });
        $('#car_selection').on('change', function () {
            var car = $(this).val();
            ajax.jsonRpc("/get_grade_list", 'call', {'car': car})
                .then(function (data) {
                    if (data) {
                        $('#grade_selection').children('option:not(:first)').remove();
                        $('#product_selection').children('option:not(:first)').remove();
                        $('#year_selection').children('option:not(:first)').remove();
                        $('#engine_selection').children('option:not(:first)').remove();
                        for (var i = 0; i < data['grade_list'].length; i++) {
                            $('#grade_selection').append($('<option>', {
                                value: data['grade_list'][i],
                                text: data['grade_list'][i]
                            }));
                        }
                        debugger;
                        for (var i = 0; i < data['product_list'].length; i++) {
                            $('#product_selection').append($('<option>', {
                                value: data['product_list'][i].value,
                                text: data['product_list'][i].name
                            }));
                        }
                        for (var i = 0; i < data['year_list'].length; i++) {
                            $('#year_selection').append($('<option>', {
                                value: data['year_list'][i],
                                text: data['year_list'][i]
                            }));
                        }
                        for (var i = 0; i < data['engine_list'].length; i++) {
                            $('#engine_selection').append($('<option>', {
                                value: data['engine_list'][i],
                                text: data['engine_list'][i]
                            }));
                        }
                    }
                })
        });
        $('.collapse.in').prev('.panel-heading').addClass('active');
        $('#accordion, #bs-collapse')
            .on('show.bs.collapse', function (a) {
                $(a.target).prev('.panel-heading').addClass('active');
            })
            .on('hide.bs.collapse', function (a) {
                $(a.target).prev('.panel-heading').removeClass('active');
            });
        $('.minus-btn').on('click', function (e) {
            e.preventDefault();
            var $this = $(this);
            var $input = $this.closest('div').find('input');
            var value = parseInt($input.val());
            if (value > 1) {
                value = value - 1;
            }
            else {
                value = 0;
            }
            $input.val(value);
        });
        $('.plus-btn').on('click', function (e) {
            e.preventDefault();
            var $this = $(this);
            var $input = $this.closest('div').find('input');
            var value = parseInt($input.val());

            if (value < 100) {
                value = value + 1;
            }
            else {
                value = 100;
            }
            $input.val(value);
        });
        $('#reset_btn').on('click', function () {
            var id = $(this).attr('data-id')
            ajax.jsonRpc("/reset_image", 'call', {'id': id})
                .then(function (data) {
                    window.location.reload()
                });
        });
    });
});
