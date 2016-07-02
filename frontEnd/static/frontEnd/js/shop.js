var $checkoutFunction = function(){
    var $checkoutList = $('#ct-js-checkout-list');
    var $checkoutBox = $('#ct-js-checkoutBox');

    var $checkoutError = $checkoutBox.find('.ct-checkout-error');
    var $checkoutFooter = $checkoutBox.find('.ct-widget--footer');
    var $checkoutPrice = $checkoutList.find('span');
    var $checkoutPriceResult = 0;

    jQuery.each($checkoutPrice, function(){
        $checkoutPriceResult += parseInt($(this).text().replace( /^\D+/g, ''));

        var $nonEmpty = $(this).text().replace( /^\D+/g, '');

        if ($nonEmpty==0){$(this).parent().css('display', 'none');}
        else{$(this).parent().css('display', 'block');}
    });

    if ($checkoutList.find('[data-itemPrice] span').text().replace( /^\D+/g, '')==0){
        $checkoutList.css('display', 'none');
        $checkoutFooter.css('display', 'none');
        $checkoutError.css('display', 'block');
        $('#ct-js-checkout-price').html($currency + '0');
    }
    else{
        $checkoutList.css('display', 'block');
        $checkoutFooter.css('display', 'block');
        $checkoutError.css('display', 'none');
        $('#ct-js-checkout-price').html($currency + $checkoutPriceResult);
    }
};

(function ($) {
    "use strict";

    $('.input-daterange').on('hide', function () {

        var $datefrom = $('.input-daterange [title="from"]').val();
        var $dateto = $('.input-daterange [title="to"]').val();

        var $getDate = function(date){

            var $dateSplit = date.split('/');
            var $dateConverted;

            var year = $dateSplit[2];
            var month = $dateSplit[0];
            var day = $dateSplit[1];

            return $dateConverted = year + '/' + month + '/' + day;
        };
        var datefromConverted = $getDate($datefrom);
        var datetoConverted = $getDate($dateto);

        var $dateinputfrom = new Date (datefromConverted);
        var $dateinputto = new Date (datetoConverted);

        var $dateTimeOutput = $dateinputto.getTime() - $dateinputfrom.getTime();
        $dateTimeOutput = $dateTimeOutput/1000/60/60/24;

        $dateTimeOutput = Math.ceil($dateTimeOutput);

        $('#datepickerOutput').html($dateTimeOutput + ' days');

        var $datacarPrice = $('[data-itemPrice]');
        var $price =  $datacarPrice.attr('data-itemPrice');

        var $priceCalculated = $price * $dateTimeOutput;

        $datacarPrice.find('span').html($currency + $priceCalculated);

        $checkoutFunction();
    });

    var $ctcheckboxgroup = $('.ct-js-checkbox-group [data-price]');
    jQuery.each($ctcheckboxgroup, function(){
        var $inputname =  $(this).attr('name');
        var $inputprice = $(this).attr('data-price');

        $(this).on('change', function(){
            if ($(this).attr('checked') == 'checked'){
                $(this).removeAttr('checked');
                $('[data-name=' + $inputname + ']').find('span').html($currency + 0);
            }
            else{
                $(this).attr('checked', 'checked');
                $('[data-name=' + $inputname + ']').find('span').html($currency + $inputprice);
            }

            $checkoutFunction();
        });
    });

    var $ctradiogroup = $('.ct-js-radio-group');
    jQuery.each($ctradiogroup, function(){
        var $radioid = $(this).attr('id');
        var $radiooutput = $('[data-name=' + $radioid + ']').find('span');

        $(this).on('change', function(){
            var $inputprice = $(this).find('[data-price]:checked').attr('data-price');
            $radiooutput.html($currency + $inputprice);

            $checkoutFunction();
        });
    });

    $(window).on('load', function(){

        jQuery.each($ctradiogroup, function(){
            var $inputprice = $(this).find('[data-price]:checked').attr('data-price');
            $('[data-name=' + $(this).attr('id') + ']').find('span').html($currency + $inputprice);
        });


        jQuery.each($ctcheckboxgroup, function(){

            var $inputname =  $(this).attr('name');
            var $inputprice = $(this).attr('data-price');

            if ($(this).attr('checked') == 'checked'){
                $('[data-name=' + $inputname + ']').find('span').html($currency + $inputprice);
            }
            else{
                $('[data-name=' + $inputname + ']').find('span').html($currency + 0);
            }
        });
        $checkoutFunction();
    });


})(jQuery);