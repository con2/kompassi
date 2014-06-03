$('button[type="submit"]').each(function(index, element) {
    var input = $('<input type="submit">'),
        $elem = $(element);

    input.attr('name', $elem.attr('name') || 'submit');
    input.attr('value', $elem.text());
    input.attr('class', $elem.attr('class'));

    $(element).replaceWith(input);
});