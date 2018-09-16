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

  setViewGroups: (groupConfig) ->
    @_groupConfig = groupConfig

  getViewGroups: ->
    @_groupConfig

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
    if type instanceof Array
      btn.addClass("btn-" + one) for one in type
      return btn
    else
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


# Filter select renderer. This is attached to existing <select> element.
# If group information is present, option groups are rendered too and their group order is used. Otherwise, plain
# backend order is used.
class FilterSelector

  # @param container [$] The <select> element to be rendered.
  constructor: (container) ->
    @container = container

  # @param backendData [BackendData] Existing backend data container.
  setBackendData: (backendData) ->
    @backendData = backendData

  # Clear and render the select contents.
  render: ->
    # Clear and add the default item.
    @container.empty()
    @container.append($("<option>").text("---"))

    # Determine whether to use grouped render, or plain render.
    groups = @backendData.getViewGroups()
    if not groups? or groups.length == 0
      @_renderPlain()
    else
      @_renderGroups()

  # Plain option list render.
  # @private
  _renderPlain: ->

    # Over whole title order, add titles that are also filters.
    for i in [0...@backendData.getTitleCount()]
      titleId = @backendData.getTitleIdByIndex(i)
      continue unless @backendData.getFilterDefById(titleId)?

      # A filter. Add its option.
      title = @backendData.getTitleById(titleId)
      item = $("<option>").text(title).prop("value", titleId)
      @container.append(item)
    return

  # Grouped option list render.
  # @private
  _renderGroups: ->

    # Over groups, add group if group contains any items, and the items itself if they are also filters.
    for groupConfig in @backendData.getViewGroups()
      groupTitle = groupConfig[0]
      columns = if groupConfig[1] instanceof Array then groupConfig[1] else groupConfig[1..]
      group = $("<optgroup>").prop("label", groupTitle)
      anyItem = false

      for column in columns
        continue unless @backendData.getFilterDefById(column)?

        # Item in group. Add the item and update flag so the whole group will be added to the select.
        anyItem = true
        item = $("<option>")
        item.text(@backendData.getTitleById(column))
        item.prop("value", column)
        group.append(item)

      # Add the group only if it is not empty.
      @container.append(group) if anyItem
    return



# Class for view selection generation and parsing.
# Selected views are displayed in the result set.
class ViewSelector

  # Dom class name for the inputs created by this.
  @inputClass: "query_builder_view_select"

  # Dom class name for use with hidden view list.
  # The class must specify display:none attribute.
  @hiddenClass: "hidden"

  # Static input id generator.
  # @param i [String | Integer, optional] Index or identifier for certain input.
  # @return [String] Id string.
  @idGen: (i=null) ->
    return "query_view_#{ i }" unless i is null
    return "query_view"

  # Constructor.
  # @param container [JQuery-object] Root object that will contain the view selectors.
  constructor: (container) ->
    @container = container
    @keyToId = {}

  # @param backendData [BackendData] Data from backend.
  setViews: (backendData) ->
    @_data = backendData

  # Render one view selector.
  # @private
  # @param title [String] View name / title.
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
      @keyToId[key] = id

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

  setEnabled: (viewKey, enabled=true) ->
    if viewKey not of @keyToId
      console.error("Key " + viewKey + " is not in key list.")
      return
    id = @keyToId[viewKey]
    $("#" + id).prop("checked", enabled)


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
    @_showID = false

    @backendUrl = null

  # Attach add-control to the controller.
  #
  # @param uiAddId [String] jQuery query for the control.
  attachAdd: (@uiAddId) ->
    @uiAdd = $(uiAddId)
    @uiAdd.change(() => @onSelect())
    selector = new FilterSelector(@uiAdd)
    selector.setBackendData(@_data)
    selector.render()

  # Attach form to the controller.
  # This is used for destination for the filter ui.
  #
  # @param uiFormId [String] jQuery query for the form.
  attachForm: (@uiFormId) ->
    @uiForm = $(uiFormId)

    # Disable submission with enter, like if the form was a regular div.
    @uiForm.on("submit", () -> false)

  attachDebug: (@uiDebugId) ->
    @uiDebug = $(uiDebugId)

  attachViewSelect: (@uiViewSelectId) ->
    @uiViewSelect = $(uiViewSelectId)
    @viewSelector = new ViewSelector(@uiViewSelect)
    @viewSelector.setViews(@_data)
    @viewSelector.render()

  attachResults: (@uiResultsId) ->
    @uiResults = $(uiResultsId)

  attachNumResults: (@uiNumResultsId) ->
    @uiNumResults = $(uiNumResultsId)

  attachExportResultsLink: (@uiExportResultsLinkId) ->
    @uiExportResultsLink = $(uiExportResultsLinkId)

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
    flt = null

    flt_type = QFilterManager.instance().findFilter(type)
    if flt_type?
      flt = @newFilter(flt_type, selected_id, type)

    container = $("<div>")
    if flt == null
      container.text("Data type '#{type}' is currently not supported.")
    else
      if @uiDebug?
        # Attach debug handler if debug place is defined.
        flt.setDebug("window.query_builder.onUpdateDebug();")

      # Remove-button for the container.
      containerId = flt.id()
      rmButton = Widget.button(null, ["default", "sm", "remove"]).text("-")
      rmButton.click(() => @onRmFilter(containerId))
      container.attr("id", "container_" + containerId)
      container.append(rmButton)

      # The actual UI.
      container.append(flt.title(), flt.createUi())
      @filterList.push(flt)

    @uiForm.append(container)

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

  onRmFilter: (containerId) ->
    # Remove given container from the form.
    @uiForm.find("#container_" + containerId).remove()

    # Find the same id from filter list and remove it.
    for flt, i in @filterList
      if flt.id() == containerId
        @filterList.splice(i, 1)
        return
    console.error("ID '" + containerId + "' not found in filters.")

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
    @uiForm.attr("method", "post")

    # Allow submitting now.
    @uiForm.off("submit")
    @uiForm.submit()

  onDataResult: (data, status, xhdr) ->
    view = new ResultView(@uiResults, @_data, @queriedViews, data)
    view.showID = @_showID
    view.render()

    @uiNumResults.text(data.length)
    @uiExportResultsLink.attr 'href', do =>
      paramStart = 'signup_ids='
      oldHref = @uiExportResultsLink.attr('href')
      replaceIdsAt = oldHref.indexOf(paramStart) + paramStart.length

      oldHref.slice(0, replaceIdsAt) + (row.pk for row in data).join(',')

  onToggleIDVisibility: (selfID) ->
    @_showID = not @_showID
    return unless selfID?
    self = $("#" + selfID)
    if @_showID
      self.addClass("btn-success")
      self.removeClass("btn-default")
    else
      self.addClass("btn-default")
      self.removeClass("btn-success")


# Class repsonsible of rendering query results to result table.
class ResultView
  constructor: (element, backendData, views, data) ->
    @rootElement = element  # <table> jquery element.
    @_data = backendData
    @views = views  # list[str] of selected view_names
    @resultData = data  # list[dict[str,?]] of result list with dict of view_names:values
    @formatter = new ValueFormatter(backendData)
    @showID = false

  # Generate colgroup and th entries.
  #
  # @param root [$] Table container where colgroup is added.
  # @param groups [$] THead container where th is added.
  # @param itemCount [Integer] Number of columns in the group.
  # @param title [String, optional] Title for the group.
  _genGroup: (root, groups, itemCount, title=null) ->
    root.append($("<colgroup>").prop("span", itemCount))
    th = $("<th>").prop("colspan", itemCount)
    th.text(title) if title?
    groups.append(th)

  # Generate table header.
  #
  # @param to [$] Table container where thead and colgroups are added.
  genHeader: (to) ->
    # Create table header element.
    # thead>tr>th*N  where N is count(selected views) (+ optional ID column)
    output = $("<thead>")

    # Headings for column groups.
    groups = $("<tr>")

    # Headings for individual columns
    titles = $("<tr>")

    # Key order defined in backend containing only keys that were selected for the query.
    _order = []

    if @showID
      # Optional ID column.
      titles.append($("<th>").text("ID"))
      @_genGroup(to, groups, 1)

    # Iterate through backend group order and find out which groups are visible in the result, and in which
    # order the items should be presented in the table.
    for groupConfig in @_data.getViewGroups()
      groupTitle = groupConfig[0]
      itemCount = 0

      # Either use given array, or the rest of the list.
      # [title, [item, item..]]  or  [title, item, item..]
      columns = if groupConfig[1] instanceof Array then groupConfig[1] else groupConfig[1..]
      for item in columns

        # If the backend column is in the result set, add relevant contents to results.
        if item in @views
          _order.push(item)
          itemCount++

          # Single column title.
          title = @_data.getTitleById(item)
          content = $("<th>").text(title)
          titles.append(content)

      if itemCount > 0
        # Column group heading generation.
        @_genGroup(to, groups, itemCount, groupTitle)

    # Add both rows of headings to thead container.
    output.append(groups)
    output.append(titles)
    to.append(output)
    return _order

  # Render the results to table.
  render: ->
    # Empty the result element.
    # table>tbody+thead
    @rootElement.empty()
    _order = @genHeader(@rootElement.append())

    # tbody>tr>td*N
    data = $("<tbody>")
    for element in @resultData
      row = $("<tr>")

      # The ID entry.
      if "__url" of element
        link = element["__url"]
        linkFn = (container, text) ->
          container.append($("<a>").attr("href", link).text(text))
      else
        linkFn = (container, text) ->
          container.text(text)

      if @showID
        row.append(linkFn($("<td>"), element["pk"]))

      # Selected views values.
      for field in _order
        value = element[field]  # TODO: Process special values from filter table.
        content = $("<td>")
        formatted = @formatter.format(field, value)
        linkFn(content, formatted)
        row.append(content)
      data.append(row)

    @rootElement.append(data)


# Result value formatter class.
# A result value can be formatted by calling {ValueFormatter#format}.
# Date locale and time zone should be set to respective class members before constructing instances.
class ValueFormatter

  # Name of the time zone used in formatting of times / timestamps.
  # (Not currently used.)
  @timeZone = null

  # Locale name used to format dates, times and timestamps.
  @locales = null

  # ValueFormatter constructor.
  # @param backendData [BackendData] Backend data object.
  constructor: (backendData) ->
    @backendData = backendData
    @dateOptions = null
    moment.locale(@locales)

  # Format a value to human readable format.
  # @param field [String] Name of the field on which the value is.
  # @param value [?] Value in the field.
  # @return [String] Formatted value.
  format: (field, value) ->
    type = @backendData.getFilterDefById(field)
    name = QFilterManager.instance().findFilterName(type)
    return value unless name?

    # Call _fmt_TYPE function, if such exists in this class.
    fn_name = "_fmt_" + name
    if fn_name of this
      return this[fn_name](value, type)

  # Format a date to string.
  # @private
  _fmt_date: (value) ->
    moment(value).format("L")

  # Format a time to string.
  # @private
  _fmt_time: (value) ->
    moment(value).format("LTS")

  # Format a time stamp to string.
  # @private
  _fmt_datetime: (value) ->
    moment(value).format("L LTS")

  # Format a nullable time stamp to string.
  # @private
  _fmt_datetimenull: (value) ->
    if value?
      return @_fmt_datetime(value)
    "-"

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
