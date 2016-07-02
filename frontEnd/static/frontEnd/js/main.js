/**
 * createIT main javascript file.
 */

// Variables // -----
var $devicewidth = (window.innerWidth > 0) ? window.innerWidth : screen.width;
var $deviceheight = (window.innerHeight > 0) ? window.innerHeight : screen.height;
var $bodyel = jQuery("body");
var $navbarel = jQuery("nav.navbar");
var $currency = validatedata($('[data-currency]').attr("data-currency"), '$');
var $topbar = $('.ct-topBar');

// Helper Functions // -----
function validatedata($attr, $defaultValue) {"use strict"; if ($attr !== undefined) { return $attr } return $defaultValue; }
function parseBoolean(str, $defaultValue) {"use strict";if (str == 'true') {return true;} else if (str == "false") {return false;}return $defaultValue;}


(function ($) {
    "use strict";


    if(document.getElementById('ct-js-wrapper')){
        var snapper = new Snap({element: document.getElementById('ct-js-wrapper')}); // snap.js init
        snapper.settings({disable: "right", easing: 'ease', addBodyClasses: true, slideIntent: 25}); // snapper settings
    }

    $(document).ready(function () { // Project Backbone

        // Mobile Menu // -----------------------------------------
        var $mobileEl = $('.ct-menuMobile .ct-menuMobile-navbar .dropdown > a');
        $mobileEl.click(function() {return false;}); // iOS SUCKS
        $mobileEl.click(function(){
            var $this = $(this);
            if($this.parent().hasClass('open')){$(this).parent().removeClass('open');} // Remove Class Open
            else{$('.ct-menuMobile .ct-menuMobile-navbar .dropdown.open').toggleClass('open');$(this).parent().addClass('open');} // Add Class Open
        });
        $('.ct-menuMobile .ct-menuMobile-navbar .onepage > a').click(function() {snapper.close();});

        $(".navbar-toggle").click(function () { // Menu Button
            if($bodyel.hasClass('snapjs-left')){snapper.close();}
            else{snapper.open('left');}
        });
        $('.ct-js-slick').attr('data-snap-ignore', 'true'); // Ignore Slick

        // Placeholder Fallback // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if ($().placeholder) {$("input[placeholder],textarea[placeholder]").placeholder();}

        // Add Color // -----------------------------------------------
        $(".ct-js-color").each(function(){$(this).css("color", '#' + $(this).attr("data-color"))});

        // Animations Init // -----------------------------------------

        if ($().appear) {
            if (device.mobile() || device.tablet() || $devicewidth < 767) {
                $("body").removeClass("cssAnimate");
            } else {
                $('.cssAnimate .animated').appear(function () {
                    var $this = $(this);

                    $this.each(function () {
                        if ($this.data('time') != undefined) {
                            setTimeout(function () {
                                $this.addClass('activate');
                                $this.addClass($this.data('fx'));
                            }, $this.data('time'));
                        } else {
                            $this.addClass('activate');
                            $this.addClass($this.data('fx'));
                        }
                    });
                }, {accX: 50, accY: -350});
            }
        }

        // Tooltips and Popovers // -------------------------------------------------
        $("[data-toggle='tooltip']").tooltip({animation: false});
        $("[data-toggle='popover']").popover({trigger: "hover", html: true});

        // Link Scroll to Section // ------------------------------------------------
        $('.ct-js-btnScroll[href^="#"]').click(function (e) {
            e.preventDefault();
            var target = this.hash, $target = $(target);
            $('html, body').stop().animate({
                'scrollTop': $target.offset().top - 0
            }, 900, 'swing', function () {
                window.location.hash = target;
            });
        });
        $('.ct-js-btnScrollUp').click(function (e) {
            e.preventDefault();
            $("body,html").animate({scrollTop: 0}, 1200);
            console.log($navbarel);
            $navbarel.find('.onepage').removeClass('active');
            $navbarel.find('.onepage:first-child').addClass('active');
            return false;
        });

        // Navbar Search // ---------------------------------------------------------------
        var $searchform = $(".ct-navbar-search");
        $('.ct-js-navSearch').click(function(e){
            e.preventDefault();
            $(this).toggleClass('is-active');
            $searchform.fadeToggle(250, function () {
                if (($searchform).is(":visible")) {$searchform.find("[type=text]").focus();}
            });return false;
        });

        // Placeholder Fallback // --------------------------------------------------------
        if ($().placeholder) {$("input[placeholder],textarea[placeholder]").placeholder();}

        // Range Slider // ----------------------------------------------------------------
        var $sliderAmount = $('.ct-sliderAmount');
        jQuery.each($sliderAmount, function(){
            var $this = $(this);

            var $slidermin = $this.find('.slider_min');
            var $slidermax = $this.find('.slider_max');
            var $sliderrange = $this.find('.sliderAmount');

            $sliderrange.on('slide', function(){
                var newvalue = $sliderrange.data('slider').getValue();

                if ($sliderrange.attr('data-currency')){
                    $slidermin.val($currency + newvalue[0]);  //Add value on inputs
                    $slidermax.val($currency + newvalue[1]);
                }
                else{
                    $slidermin.val(newvalue[0]);  //Add value on inputs
                    $slidermax.val(newvalue[1]);
                }

            });
        });

        if (!($('html').is('.ie8'))){
            // Selectize.js // ----------------------------------------------------------------
            var $selectize = $('.ct-js-selectize');
            if ($selectize.length > 0){
                $selectize.each(function(){$(this).selectize();})
            }
        }

        $('#billingInfo').on('change', function(){
            var $billing = $('.ct-js-billing');
            jQuery.each($billing, function(){
                console.log($billing);
                if ($billing.attr('disabled')){
                    $billing.removeAttr('disabled');
                    $billing.siblings().removeClass('disabled');
                }
                else{
                    $billing.attr('disabled', 'disabled');
                    $billing.siblings().addClass('disabled');
                }
            })
        });

        // Video Embet Click // -----------------------------------------------------------

        $('.ct-embed').each(function(){
            var $this = $(this);
            $this.find('i').on('click', function(){
                $(this).addClass('hide');
                $this.find('img').addClass('hide');
                $this.find('.ct-embed-content').addClass('hide');
                $this.find('video').get(0).play();
            })
        });

        // h5Validate // -----------------------------------------------------------------

        if ($().h5Validate){

            $('.validateIt').h5Validate({
                errorClass: 'form-error'
            }).on('validate', function(){
                jQuery.each($('.validateIt [required]'), function(){
                    var $errormessage = validatedata($(this).attr("data-error-message"), 'This field is required');
                    $(this).attr('placeholder', $errormessage);
                })
            });

            $.h5Validate.addPatterns({
                phone: /([\+][0-9]{1,3}([ \.\-])?)?([\(]{1}[0-9]{3}[\)])?([0-9A-Z \.\-]{1,32})((x|ext|extension)?[0-9]{1,4}?)/
            });
        }
    });

        // Navbar Search // ---------------------------------------------------------------

    $(document).mouseup(function (e) {
        var $searchform = $(".ct-navbar-search");
        var $ctnavsearch = $('.ct-js-navSearch');
        if(!$ctnavsearch.is(e.target)){
            if (!$searchform.is(e.target) // if the target of the click isn't the container...
                && $searchform.has(e.target).length === 0) // ... nor a descendant of the container
            {$searchform.hide();$ctnavsearch.removeClass('is-active');}
        }});

    // -----------------------------------------------------------------------------------------------------------

    $(window).on('load resize', function(){

        // Dropdown Toggle on Mobile
        var $dropdown = $('.navbar-nav li.dropdown a, li.ct-subDropdown a');
        if ($(window).width() < 479) {$dropdown.attr('data-toggle', 'dropdown');}
        else{$dropdown.removeAttr('data-toggle');}


        // Preloader // --------------------------------------

        var $preloader = $('.ct-preloader-container');
        var $content = $('.ct-preloader');

        setTimeout(function(){
            $($preloader).addClass('animated').addClass('fadeOut');
            $($content).addClass('animated').addClass('fadeOut');
        }, 0);
        setTimeout(function(){
            $($preloader).css('display', 'none').css('z-index', '-9999');
        }, 500);


        // Sync slider // ----------------------------------------
        setTimeout(function(){
            var $slickSynced = $('.ct-slick--synced');
            if ($slickSynced.length > 0){
                var $sliderheight = $slickSynced.find('.ct-js-slick-for').find('img').first().height();

                var $slickPrev = $slickSynced.find('.slick-prev');
                var $slickNext = $slickSynced.find('.slick-next');

                $slickPrev.css('top', $sliderheight/2 + 'px');
                $slickNext.css('top', $sliderheight/2 + 'px');
            }
        }, 10);


        // Elements padding with TopBar // --------------------------------------------
        if ($topbar.length > 0){
            $navbarel.css('margin-top', $topbar.height() + 12 + 'px');
        }

        // Snapper // -------------------------------------------
        if ($("#ct-js-wrapper").length > 0) {
            if ($(window).width() < 768){
                snapper.enable();
            } else {
                snapper.disable();
            }
        }

    });


    $(window).scroll(function(){
        var scroll = $(window).scrollTop();

        // Scroll Up Button // --------------------------------------------------------
        if (scroll > 400) {jQuery('.ct-js-btnScrollUp').addClass('is-active');
        } else {jQuery('.ct-js-btnScrollUp').removeClass('is-active');}


        // Navbar states // ---------------------------------------------------------
        if (scroll > 50){
            if ($bodyel.hasClass('ct-navbar--toFixed')){
                $navbarel.addClass('ct-navbar--fixed');
            }
            if ($bodyel.hasClass('ct-navbar--toMotive')){
                $navbarel.attr('id', 'navbar-motive')
            }
            if ($bodyel.hasClass('ct-navbar--toInverse')){
                $navbarel.attr('id', 'navbar-inverse')
            }
            if ($bodyel.hasClass('ct-navbar--toDefault')){
                $navbarel.attr('id', 'navbar-default')
            }
        }
        else{
           $navbarel.removeClass('ct-navbar--fixed');
           $navbarel.removeAttr('id');
        }

    });

    if ($topbar.length > 0){
        $(window).on('load resize scroll', function(){
            var scroll = $(window).scrollTop();
            if (scroll < 100){
                $('.ct-menuMobile').css('padding-top', $topbar.height() + 12 + 'px');
            }
            else{
                $('.ct-menuMobile').css('padding-top', 0);
            }
        })
    }


})(jQuery);