var getProgramme = function(cell) {
  return $($(cell).find('a').attr('href'));
};

$('td.programme').popover({
  container: 'body',
  html: true,
  placement: 'bottom',
  trigger: 'hover',
  title: function() {
    return getProgramme(this).find('.title').html();
  },
  content: function(){
    return getProgramme(this).find('.programme-info').html();
  }
});

$("body").on("click", "a", function() {
  var fromTop = 60;
  var href = $(this).attr("href");
  var anchor = href.indexOf("#");

  if(href && anchor != -1 && anchor != href.length - 1) {
    href = href.substring(anchor);
    if($(href).length > 0) {
      $('html, body').animate({scrollTop: $(href).offset().top - fromTop}, 400);
      return false;
    }
  }
});
