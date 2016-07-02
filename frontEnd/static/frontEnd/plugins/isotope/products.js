(function ($) {
    "use strict";

    jQuery(window).load(function () {
        if ($().isotope && ($('.ct-product-gallery').length > 0)) {

            var $container = $('.ct-product-gallery'), // object that will keep track of options
                isotopeOptions = {}, // defaults, used if not explicitly set in hash
                defaultOptions = {
                    filter: '*', itemSelector: '.ct-product', // set columnWidth to a percentage of container width
                    masonry: {
                    },
                    transformsEnabled: false
                };
            // set up Isotope
            $container.isotope(defaultOptions);

            $container.imagesLoaded().progress(function (instance, image) {
                if (!image.isLoaded) {
                    return;
                }

                var p = $(image.img).closest('.hidden');
                p.removeClass('hidden');
                $container.addClass('is-loaded');

                $container.isotope('layout');
            });

            // Range Slider // ----------------------------------------------------------------

            var $filtering = $('.ct-sliderAmount');

            jQuery.each($filtering, function(){
                var $this = $(this);
                var $filterslider = $(this).find('.sliderAmount');
                var $productattr = $(this).attr('id');

                $filterslider.on('slide', function(){
                    var $min = $this.find('.slider_min').val().replace( /^\D+/g, '');
                    var $max = $this.find('.slider_max').val().replace( /^\D+/g, '');

                    $container.isotope('layout');

                    $('[' + $productattr + ']').each(function(){
                        if ($(this).attr($productattr) < $min){
                            $(this).addClass('hidden');
                        }
                        else if ($(this).attr($productattr) > $max){
                            $(this).addClass('hidden');
                        }
                        else{
                            $(this).removeClass('hidden');
                        }
                    });
                });
            });


            // bind filter on select change
            $('.ct-js-selectDriver').on( 'change', function() {
                // get filter value from option value
                var filterValue = this.value;
                // use filterFn if matches value
                $container.isotope({ filter: filterValue });
            });

            $('.ct-js-carType').on( 'change', function() {
                // get filter value from option value
                var filterValue = this.value;
                // use filterFn if matches value
                $container.isotope({ filter: filterValue });
            });



        }

    });


}(jQuery));