# Backend data holder.
# The data can be set via constructor or with individual setters.
class BackendData
  constructor: (filterDefs=null, titleMap=null) ->
    @setFilterDefs(filterDefs) if filterDefs?
    @setTitleMap(titleMap) if titleMap?

  # @param filterDefs [Object] Dictionary of id:def.
  setFilterDefs: (filterDefs) ->
    @_filterDefs = filterDefs

  # @param titleMap [Array] List of tuples containing id, title.
  setTitleMap: (titleMap) ->
    @_titleMap = {}
    @_order = []
    for tuple in titleMap
      key = tuple[0]
      title = tuple[1]
      @_titleMap[key] = title
      @_order.push(key)

  getTitleById: (id) ->
    return @_titleMap[id]

  getTitleByIndex: (index) ->
    return @_titleMap[@_order[index]]

  getTitleIdByIndex: (index) ->
    return @_order[index]

  getFilterCount: ->
    return @_filterDefs.length

  getTitleCount: ->
    return @_order.length

  getFilterDefById: (id) ->
    return @_filterDefs[id]

  getTitleOrder: ->
    return @_order
window.BackendData = BackendData


# Widget factory producing jquery elements.
class DefaultWidget
  id: (id) ->
    return if id? then "id=\"#{ id }\"" else ""

  hidden: (name) ->
    return $("""<input type="hidden" name="#{ name }">""")

  label: (forId) ->
    return $("""<label for="#{ forId }">""")

  button: (id=null) ->
    return $("""<button type="button" #{ @id(id) }>""")

  select: (id=null) ->
    return $("""<select #{ @id(id) }>""")

  checkbox: (id=null) ->
    return $("""<input type="checkbox" #{ @id(id) }>""")

  radio: (id=null) ->
    return $("""<input type="radio" #{ @id(id) }>""")

  text: (id=null) ->
    return $("""<input type="text" #{ @id(id) }>""")


# Bootstrap-specialized widget factory.
class BootstrapWidget extends DefaultWidget
  button: (id=null, type=null) ->
    btn = super.button(id).addClass("btn")
    return if type? then btn.addClass("btn-" + type) else btn

window.Widget = new BootstrapWidget()


# Query filter nanager.
# Filters can be registered with {QFilterManager.registerFilter registerFilter},
# and later found with {QFilterManager#findFilter findFilter}.
# @example Registering filter
#   QFilterManager.registerFilter("bool", BooleanFilter)
#   QFilterManager.registerFilter("fancyText", StringFilter, (def) -> def is "str")
class QFilterManager
  # Singleton instance.
  # @noDoc
  @_instance = null

  # Get singleton instance of this class.
  #
  # @return [QFilterManager] Manager instance.
  @instance: ->
    if @_instance is null
      @_instance = new QFilterManager()
    return @_instance

  constructor: ->
    @filters = {}
    @matchers = {}

  # Register a new filter type.
  # This is only a convenience function for calling the actual instance version of this.
  #
  # @see QFilterManager#registerFilter
  @registerFilter: (args...) ->
    QFilterManager.instance().registerFilter(args...)

  # Register a new filter type.
  #
  # @param typeName [String] Filter type name used for simple matching and identification.
  # @param filterClass [QueryFilter] Filter class being registered.
  # @param matcher [function, optional] Optional matcher function, that will be given the
  #   filter definition when called.
  registerFilter: (typeName, filterClass, matcher=null) ->
    @filters[typeName] = filterClass
    @matchers[typeName] = matcher unless matcher is null

  # Find name of suitable filter for filter definition.
  #
  # @param filterPart [Object | String] Type name of the filter, or the filter definition object.
  # @return [String] Name of the filter, or null if no matches were found.
  findFilterName: (filterPart) ->
    # String name of filter
    return filterPart unless filterPart instanceof Object or filterPart of @matchers

    # Object -> match by matcher
    for key, matcher of @matchers
      result = matcher(filterPart)
      if result is true
        return key
    return null

  # Find suitable filter for filter definition.
  #
  # @param filterPart [Object | String] Type name of the filter, or the filter definition object.
  # @return [QueryFilter] Filter class, or null if no matches were found.
  findFilter: (filterPart) ->
    key = @findFilterName(filterPart)
    return @filters[key] if key?
    return null

QFilterManager.instance()
window.QFilterManager = QFilterManager


# Class for view selection generation and parsing.
# Selected views are displayed in the result set.
class ViewSelector

  # Dom class name for the inputs created by this.
  @inputClass: "query_builder_view_select"

  # Dom class name for use with hidden view list.
  # The class must specify display:none attribute.
  @hiddenClass: "view-hidden"

  # Static input id generator.
  # @param i [String | Integer, optional] Index or identifier for certain input.
  # @return [String] Id string.
  @idGen: (i=null) ->
    return "query_view_#{ i }" unless i is null
    return "query_view"

  # Constructor.
  # @param container [JQuery-object] Root object that will contain the view selectors.
  constructor: (container) ->
    @container = container

  # @param backendData [BackendData] Data from backend.
  setViews: (backendData) ->
    @_data = backendData

  # Render one view selector.
  # @private
  # @param title [String] View name / title.
  # @param id [String] View identifier.
  # @param key [String] Backend view key value.
  # @return [$] Generated selector view.
  _renderOne: (title, id, key) ->
    container = $("<div>")

    input = Widget.checkbox(id)
    input.addClass(@constructor.inputClass)
    input.data("key", key)

    label = Widget.label(id)
    label.text(title)

    container.append(input, label)
    return container

  # Renders the selectors in to a string.
  #
  # @return [String] Rendered selectors.
  renderStr: ->
    container = $("<div>")

    toggle = Widget.button(null, "default")
    toggle.text("Toggle views")
    toggle.click(() => @onToggleViews())
    container.append(toggle)

    views = $("<div>")
    views.attr("id", @constructor.idGen())
    views.addClass(@constructor.hiddenClass)

    for key, i in @_data.getTitleOrder()
      title = @_data.getTitleById(key)
      id = @constructor.idGen(i)
      views.append(@_renderOne(title, id, key))

    container.append(views)
    return container

  # Renders the selectors directly in the supplied container.
  render: ->
    @container.html(@renderStr())

  # Get current selections of views.
  #
  # @return [Array] A list of selected (backend) keys.
  getSelections: ->
    inputs = @container.find("." + @constructor.inputClass + ":checked")
    ids = []
    for element in inputs
      ids.push($(element).data("key"))
    return ids

  # Toggle views visibility.
  onToggleViews: ->
    container = $("#" + @constructor.idGen())
    container.toggleClass(@constructor.hiddenClass)


# The actual front end Query Builder.
# This class is made available via window.
# To use this, {QueryBuilder#attachAdd} and {QueryBuilder#attachForm} must be called to attach functions for the UI.
# Additionally, {QueryBuilder#setFilters} and {QueryBuilder#setTitles} must be called to bind backend data to the
# controller.
class QueryBuilder
  constructor: (backendData) ->
    @filterIds = {}  # Map containing index numbers for added filters.
    @filterList = []  # List containing the actual filters.
    @uiDebug = null  # Debug output node.
    @_disableSelect = false  # Flag to prevent recursive change-events.
    @_data = backendData
    @viewSelector = null

    @backendUrl = null

  # Attach add-control to the controller.
  #
  # @param uiAddId [String] jQuery query for the control.
  attachAdd: (@uiAddId) ->
    @uiAdd = $(uiAddId)
    @uiAdd.change(() => @onSelect())

  # Attach form to the controller.
  # This is used for destination for the filter ui.
  #
  # @param uiFormId [String] jQuery query for the form.
  attachForm: (@uiFormId) ->
    @uiForm = $(uiFormId)

  attachDebug: (@uiDebugId) ->
    @uiDebug = $(uiDebugId)

  attachViewSelect: (@uiViewSelectId) ->
    @uiViewSelect = $(uiViewSelectId)
    @viewSelector = new ViewSelector(@uiViewSelect)
    @viewSelector.setViews(@_data)
    @viewSelector.render()

  attachResults: (@uiResultsId) ->
    @uiResults = $(uiResultsId)

  setBackend: (url) ->
    @backendUrl = url

  onSelect: ->
    return if @_disableSelect

    selected_id = @uiAdd.val()

    # Change selection back to initial "---"
    @_disableSelect = true
    @uiAdd.find("option:selected").removeAttr("selected")
    @uiAdd.children(":first").attr("selected", "selected")
    @_disableSelect = false

    type = @_data.getFilterDefById(selected_id)
    filterUi = null
    flt = null

    flt_type = QFilterManager.instance().findFilter(type)
    if flt_type?
      flt = @newFilter(flt_type, selected_id, type)

    if flt == null
      filterUi = "Type #{type} not supported."
    else
      if @uiDebug?
        # Attach debug handler if debug place is defined.
        flt.setDebug("window.query_builder.onUpdateDebug();")

      filterUi = flt.createUi()
      @filterList.push(flt)

    @uiForm.append($("<div>").append(flt.title(), filterUi))

  newFilter: (flt_type, selected_id, type) ->
    # Create new filter by typemap.
    flt = new flt_type(selected_id, type)
    flt.setTitle(@_data.getTitleById(selected_id))

    # Each filter is numbered by count of added number of given type.
    if selected_id of @filterIds
      @filterIds[selected_id]++
    else
      @filterIds[selected_id] = 0

    flt.setId(@filterIds[selected_id])

    return flt

  onUpdateDebug: ->
    asJson = JSON.stringify(@_getFilter())
    asJson += "\n\n" + JSON.stringify(@_getViews())
    @uiDebug.text(asJson)

  _getFilter: ->
    result = []

    for queryPart in @filterList
      flt = queryPart.createFilter()
      if flt is null or flt.length == 0
        continue
      if result.length == 0
        result.push("and")
      result.push(flt)

    return result

  _getViews: ->
    # Cache selections so they can be used when rendering the contents.
    @queriedViews = @viewSelector.getSelections()

  _postData: ->
    postData =
      "filter": JSON.stringify(@_getFilter())
      "view": JSON.stringify(@_getViews())
    return postData

  onExec: ->
    postData = @_postData()
    fn = (data, status, xhdr) => @onDataResult(data, status, xhdr)
    $.post(@backendUrl, postData, fn, "json")

  onExecPlain: ->
    postData = @_postData()

    filter = Widget.hidden("filter")
    filter.val(postData.filter)
    @uiForm.append(filter)

    views = Widget.hidden("view")
    views.val(postData.view)
    @uiForm.append(views)

    @uiForm.attr("action", @backendUrl)
    @uiForm.submit()

  onDataResult: (data, status, xhdr) ->
    view = new ResultView(@uiResults, @_data, @queriedViews, data)
    view.render()


# Class repsonsible of rendering query results to result table.
class ResultView
  constructor: (element, backendData, views, data) ->
    @rootElement = element  # <table> jquery element.
    @_data = backendData
    @views = views  # list[str] of selected view_names
    @resultData = data  # list[dict[str,?]] of result list with dict of view_names:values
    @formatter = new ValueFormatter(backendData)

  # Generate table header.
  genHeader: ->
    # Create table header element.
    # thead>tr>th*N  where N is 1 + count(selected views)
    output = $("<thead>")

    row = $("<tr>")
    row.append($("<th>").text("ID"))

    # The selected views headings.
    for field in @views
      title = @_data.getTitleById(field)
      content = $("<th>").text(title)
      row.append(content)

    output.append(row)
    return output

  # Render the results to table.
  render: ->
    # Empty the result element.
    # table>tbody+thead
    @rootElement.empty()
    @rootElement.append(@genHeader())

    # tbody>tr>td*N
    data = $("<tbody>")
    for element in @resultData
      row = $("<tr>")

      # The ID entry.
      row.append($("<td>").text(element["pk"]))

      # Selected views values.
      for field in @views
        value = element[field]  # TODO: Process special values from filter table.
        content = $("<td>")
        formatted = @formatter.format(field, value)
        content.text(formatted)
        row.append(content)
      data.append(row)

    @rootElement.append(data)


# Result value formatter class.
# A result value can be formatted by calling {ValueFormatter#format}.
# Date locale and time zone should be set to respective class members before constructing instances.
class ValueFormatter

  # Name of the time zone used in formatting of times / timestamps.
  @timeZone = null

  # Locale name used to format dates, times and timestamps.
  @locales = null

  # Yield options passed to Date format functions.
  @createDateOptions: () ->
    return timeZone: ValueFormatter.timeZone

  # Test if given Date function supports locales.
  # @param fn [String] Function name, such as "toLocaleString".
  # @return [Boolean] True if the function supports locales, false if not.
  @dateSupportsLocales: (fn) ->
    try
      new Date()[fn]("i")
    catch e
      return e.name is "RangeError"
    return false

  @dateSupport:
    toLocaleDateString: @dateSupportsLocales("toLocaleDateString")
    toLocaleTimeString: @dateSupportsLocales("toLocaleTimeString")
    toLocaleString: @dateSupportsLocales("toLocaleString")

  # ValueFormatter constructor.
  # @param backendData [BackendData] Backend data object.
  constructor: (backendData) ->
    @backendData = backendData
    @dateOptions = null

  # Format a value to human readable format.
  # @param field [String] Name of the field on which the value is.
  # @param value [?] Value in the field.
  # @return [String] Formatted value.
  format: (field, value) ->
    type = @backendData.getFilterDefById(field)
    name = QFilterManager.instance().findFilterName(type)
    return value unless name?

    fn_name = "_fmt_" + name
    if fn_name of this
      return this[fn_name](value, type)

  # Helper function for calling locale-aware toLocale*String functions of date objects.
  # If the function does not support locales, their un-aware versions are called instead.
  #
  # @param dateObj [Date] Object to call the function on.
  # @param fn [String] Function name to call.
  # @return [String] Locale-formatted string.
  # @private
  _callDateLocale: (dateObj, fn) ->
    if ValueFormatter.dateSupport[fn]
      if @dateOptions is null
        @dateOptions = ValueFormatter.createDateOptions()
      return dateObj[fn](ValueFormatter.locales, @dateOptions)
    else
      return dateObj[fn]()

  # Format a date to string.
  # @private
  _fmt_date: (value) ->
    date = new Date(value)
    @_callDateLocale(date, "toLocaleDateString")

  # Format a time to string.
  # @private
  _fmt_time: (value) ->
    time = new Date(value)
    @_callDateLocale(time, "toLocaleTimeString")

  # Format a time stamp to string.
  # @private
  _fmt_datetime: (value) ->
    dt = new Date(value)
    @_callDateLocale(dt, "toLocaleString")

  # Format a boolean value to string.
  # @private
  _fmt_bool: (value) ->
    return if value then "Kyllä" else "Ei"

  # Format a Enum/FK value to string.
  # @private
  _fmt_object_or: (value, type) ->
    if value of type.values
      return type.values[value]
    return value

  # Format a M2M value to string.
  # @private
  _fmt_object_and: (value, type) ->
    # null -> empty string
    return "" unless value?

    # Use enum formatter to format each entry separately, and join the result array to string.
    value = [value] if not value instanceof Array
    results = (@_fmt_object_or(entry, type) for entry in value)
    return results.join(", ")


# Publish some classes.
window.QueryBuilder = QueryBuilder
window.ValueFormatter = ValueFormatter
