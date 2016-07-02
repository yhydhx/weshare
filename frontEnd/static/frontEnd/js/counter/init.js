(function ($) {
    "use strict";

    $(document).ready(function () {
        /* ================== */
        /* ==== COUNT TO ==== */

        var $ctjscounter = $('.ct-js-counter');

        if (($().countTo) && ($().appear) && ($("body").hasClass("cssAnimate"))) {
            $ctjscounter.data('countToOptions', {
                formatter: function (value, options) {
                    return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ' ');
                }
            }).appear(function () {
                $(this).each(function (options) {
                    var $this = $(this);
                    var $speed = validatedata($this.attr('data-speed'), 700);
                    options = $.extend({}, options || {
                        speed: $speed
                    }, $this.data('countToOptions') || {});
                    $this.countTo(options);
                });
            });
        } else if(($().countTo)){
            $ctjscounter.data('countToOptions', {
                formatter: function (value, options) {
                    return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ' ');
                }
            });
            $ctjscounter.each(function (options) {
                var $this = $(this);
                var $speed = validatedata($this.attr('speed'), 1200);
                options = $.extend({}, options || {
                    speed: $speed
                }, $this.data('countToOptions') || {});
                $this.countTo(options);
            });
        }

        jQuery.each($ctjscounter, function(){
            var $parent = $(this).parent();
            var $datacolor = $parent.attr('data-color');

            $parent.find('.ct-counterBox-number').css('color', $datacolor);
            $parent.find('.ct-counterBox-icon').css('color', $datacolor);
            $parent.css('box-shadow', ' 0 1px 0 0 ' + $datacolor);
        })

    })
}(jQuery));