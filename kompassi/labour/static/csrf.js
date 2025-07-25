// Generated by CoffeeScript 1.7.1
(function () {
  var csrfSafeMethod, getCookie, getCsrf, setupAjax;

  getCookie = function (name) {
    var cookie, cookies, _i, _len;
    if (document.cookie && document.cookie !== "") {
      cookies = document.cookie.split(";");
      for (_i = 0, _len = cookies.length; _i < _len; _i++) {
        cookie = cookies[_i];
        cookie = jQuery.trim(cookie);
        if (cookie.substring(0, name.length + 1) === name + "=") {
          return decodeURIComponent(cookie.substring(name.length + 1));
        }
      }
    }
    return null;
  };

  getCsrf = function () {
    return getCookie("csrftoken");
  };

  csrfSafeMethod = function (method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };

  setupAjax = function () {
    var csrftoken;
    csrftoken = getCsrf();
    return $.ajaxSetup({
      crossDomain: false,
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
          return xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
    });
  };

  window.setupAjax = setupAjax;
}).call(this);
