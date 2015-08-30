(function($) {
    var fragmentLinkClicked, fragmentReceived;

    fragmentLinkClicked = function() {
        var href =$(this).attr('href');
        $.getJSON(href, fragmentReceived);
        return false;
    };

    fragmentReceived = function(data, textStatus, jqXHR) {
        if (!data.replace || !data.content) {
            return;
        }

        $(data.replace).replaceWith(data.content);
    };

    $('a[data-fragment]').click(fragmentLinkClicked);
})(jQuery);
