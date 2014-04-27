getCookie = (name) ->
  if document.cookie and document.cookie != ''
    cookies = document.cookie.split(';')
    for cookie in cookies
      cookie = jQuery.trim(cookie)
      # Does this cookie string begin with the name we want?
      if cookie.substring(0, name.length + 1) == (name + '=')
        return decodeURIComponent(cookie.substring(name.length + 1))
  return null

getCsrf = ->
  return getCookie('csrftoken')

csrfSafeMethod = (method) ->
  # these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)

setupAjax = ->
  csrftoken = getCsrf()
  $.ajaxSetup(
    crossDomain: false,
    beforeSend: (xhr, settings) ->
      if not csrfSafeMethod(settings.type)
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
  )

window.setupAjax = setupAjax
