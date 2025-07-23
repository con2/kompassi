(function ($) {
  $('input[name="signup-job_categories"]').each(function (index, elem) {
    var pk = $(elem).attr("value");
    $(this)
      .parent("label")
      .after('<p class="help-block">' + labourJobDescriptions[pk] + "</p>");
  });
})(jQuery);
