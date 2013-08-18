$(function() {
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
});