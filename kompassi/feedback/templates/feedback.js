// {% load i18n %}
function sendKompassiFeedback(event) {
  event.preventDefault();

  var $form = $("#kompassi-feedback-widget-form");

  $.ajax({
    type: "POST",
    url: '{% url "feedback_view" %}',
    data: $form.serialize(),
  }).then(function () {
    alert("{% trans 'Thank you for your feedback!' %}");
    $form[0].reset();
    $("#kompassi-feedback-widget-collapse").collapse("hide");
  });
}
