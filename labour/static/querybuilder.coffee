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

# Base class for various query filter implementations.
# A subclass must implement {QueryFilter#createUi} and {QueryFilter#createFilter}.
class QueryFilter
  constructor: (selectedId, filterDef) ->
    @debugHandler = null  # Handler script to execute on element change.
    @idName = selectedId  # Backend-related name of the filter.
    @idNumber = null  # Index number of added filter (of type @idName).
    @filterDef = filterDef  # Filter definition from backend. A string or object.

  # Set display name of the property/filterable.
  setTitle: (@uiTitle) ->

  # Set onchange debug script. null to disable.
  setDebug: (@debugHandler) ->

  # Set index number of added filter.
  setId: (@idNumber) ->

  # Yield UI contents of this filter.
  #
  # @abstract
  # @return [String, $] String or jQuery-tree.
  createUi: ->
    throw "Not implemented."

  # Yield filter object defined by this filter.
  # The returned filter should reflect choices user has made with the UI.
  #
  # @abstract
  # @return [Array] A list used by backend filter parser.
  createFilter: ->
    throw "Not implemented."

  # Yield debug attribute if handler code is defined.
  #
  # @param attr [String] Optional attribute name to use instead of onchange.
  createDebugAttr: (attr = "onchange") ->
    return "" if @debugHandler is null
    return "#{ attr }=\"#{ @debugHandler }\""

  # Yield label-tag for given name using default display name.
  labelFor: (id, title = @uiTitle) ->
    return "<label for=\"#{ id }\">#{ title }</label>"

  # Yield id-name for this filter with optional suffix.
  id: (suff = null) ->
    return @idName + "_" + @idNumber if suff == null
    return @idName + "_" + suff + "_" + @idNumber

  # Yield display name -element.
  title: ->
    return "<span class=\"title\">#{ @uiTitle }</span> "

  # Apply negation, if negative query is requested.
  # @param isNot [Boolean] If true, query is negated.
  # @param query [Array] Query / filter array to negate.
  # @return [Array] Query, or its negated version.
  applyNOT: (isNot, query) ->
    return query unless isNot
    return ["not", query]


# A filter for boolean variables.
# This will display just two radio buttons, "Yes" and "No" that will define the resulting filter.
class BoolFilter extends QueryFilter

  # Create radio input.
  #
  # @private
  # @param id [String] The actual unique id field name.
  # @param name [String] Name of the radio group.
  # @param value [String] Choice value.
  # @param attrs [String] Optional attributes to append to the input.
  createRadio: (id, name, value, attrs="") ->
    return """ <input type="radio" id="#{ id }" name="#{ name }" value="#{ value }" #{ @createDebugAttr() } #{ attrs }>"""

  createUi: ->
    name = @id()
    id_true = @id("true")
    id_false = @id("false")
    return "<span id=\"#{ name }\">" +
      @labelFor(id_true, "Kyllä") + @createRadio(id_true, name, "true", "checked=\"checked\"") +
      @labelFor(id_false, "Ei") + @createRadio(id_false, name, "false") +
      "</span>"

  createFilter: ->
    name = @id()
    selected = $("#" + name).find("input:checked").attr("value")

    if selected != "true" and selected != "false"
      throw "Selected value was not any valid boolean value."

    selected = "true" == selected
    return ["eq", @idName, selected]


# A filter for string variables.
# Strings can be filtered in various modes - they are presented in a drop-list to choose from.
class StringFilter extends QueryFilter

  # Yield filtering mode input.
  #
  # @private
  # @param id [String] Unique id for the input.
  createMode: (id) ->
    return """
    <select id="#{ id }" #{ @createDebugAttr() }>
      <option value="contains" selected="selected">Sisältää</option>
      <option value="!contains">Ei sisällä</option>
      <option value="startswith">Alkaa</option>
      <option value="endswith">Päättyy</option>
      <option value="is">On</option>
      <option value="!is">Ei ole</option>
      <option value="regex">Regex</option>
      <option value="!regex">Ei regex</option>
    </select>
    """

  # Yield input text input.
  #
  # @private
  # @param id [String] Unique id for the input.
  createInput: (id) ->
    return """ <input type="text" id="#{ id }" name="#{ id }" #{ @createDebugAttr() }/>"""

  createUi: ->
    # Title [MatchMethod] [StringInput]
    id = @id()
    return @createMode(id + "_mode") + @createInput(id)

  createFilter: ->
    mode = $("#" + @id() + "_mode").val()
    value = $("#" + @id()).val()
    if mode == null or mode == ""
      throw "Invalid select value for string mode."

    negate = false
    if mode[0] == "!"
      mode = mode.substr(1)
      negate = true

    flt = [mode, @idName, value]
    return @applyNOT(negate, flt)



# Class for view selection generation and parsing.
# Selected views are displayed in the result set.
class ViewSelector

  # Dom class name for the inputs created by this.
  @inputClass: "query_builder_view_select"

  # Static input id generator.
  # @param i Index or identifier for certain input.
  # @return [String] Id string.
  @idGen: (i) ->
    "query_view_#{ i }"

  # Constructor.
  # @param container [JQuery-object] Root object that will contain the view selectors.
  constructor: (container) ->
    @container = container

  # @param backendData [BackendData] Data from backend.
  setViews: (backendData) ->
    @_data = backendData

  # Renders the selectors in to a string.
  #
  # @return [String] Rendered selectors.
  renderStr: ->
    views = ""
    for key, i in @_data.getTitleOrder()
      title = @_data.getTitleById(key)
      id = @constructor.idGen(i)
      views += """<div><input type="checkbox" id="#{ id }" class="#{ @constructor.inputClass }" data-key="#{ key }" /> <label for="#{ id }">#{ title }</label></div>"""
    return views

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
    @disableSelect = false  # Flag to prevent recursive change-events.

    # Map of backend types to frontend classes.
    @filterTypeMap =
      "bool": BoolFilter
      "text": StringFilter
      "str": StringFilter
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
    return if @disableSelect

    selected_id = @uiAdd.val()

    # Change selection back to initial "---"
    @disableSelect = true
    @uiAdd.find("option:selected").removeAttr("selected")
    @uiAdd.children(":first").attr("selected", "selected")
    @disableSelect = false

    type = @_data.getFilterDefById(selected_id)
    filterUi = null
    flt = null

    if type instanceof Object and "multiple" of type
      filterUi = "Objects not supported yet."
      # flt = @newFilter(selected_id, "object_" + type.multiple, title)

    else if type of @filterTypeMap
      flt = @newFilter(selected_id, type, type)


    if flt == null
      filterUi = "Type #{type} not supported."
    else
      if @uiDebug != null
        # Attach debug handler if debug place is defined.
        flt.setDebug("window.query_builder.onUpdateDebug();")

      filterUi = flt.title() + flt.createUi()
      @filterList.push(flt)

    if filterUi != null and typeof(filterUi) is not "string"
      filterUi = filterUi.html()

    @uiForm.append("<div>#{ filterUi }</div>")

  newFilter: (selected_id, type, def) ->
    # Create new filter by typemap.
    flt = new @filterTypeMap[type](selected_id, def)
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

  onExec: ->
    postData =
      "filter": JSON.stringify(@_getFilter())
      "view": JSON.stringify(@_getViews())

    fn = (data, status, xhdr) => @onDataResult(data, status, xhdr)
    $.post(@backendUrl, postData, fn, "json")

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
        content.text(value)
        row.append(content)
      data.append(row)

    @rootElement.append(data)


# Publish the class.
window.QueryBuilder = QueryBuilder
