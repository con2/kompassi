# Base class for various query filter implementations.
# A subclass must implement {QueryFilter#createUi} and {QueryFilter#createFilter}.
class QueryFilter
  constructor: ->
    @debugHandler = null  # Handler script to execute on element change.
    @idName = ""  # Backend-related name of the filter.
    @idNumber = null  # Index number of added filter (of type @idName).
    @uiTitle = ""  # Title/display name of the property this filter filters.

  # Set display name of the property/filterable.
  setTitle: (@uiTitle) ->

  # Set onchange debug script. null to disable.
  setDebug: (@debugHandler) ->

  # Set backend property name.
  setName: (@idName) ->

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
    return ["is", @idName, selected]


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

    if not negate
      return flt
    else
      return ["not", flt]


# The actual front end Query Builder.
# This class is made available via window.
# To use this, {QueryBuilder#attachAdd} and {QueryBuilder#attachForm} must be called to attach functions for the UI.
# Additionally, {QueryBuilder#setFilters} and {QueryBuilder#setTitles} must be called to bind backend data to the
# controller.
class QueryBuilder
  constructor: ->
    @filterIds = {}  # Map containing index numbers for added filters.
    @filterList = []  # List containing the actual filters.
    @uiDebug = null  # Debug output node.
    @disableSelect = false  # Flag to prevent recursive change-events.

    # Map of backend types to frontend classes.
    @filterTypeMap =
      "bool": BoolFilter
      "text": StringFilter
      "str": StringFilter
    @dataFilters = {}  # Filter data from backend.
    @dataTitles = {}  # Title data from backend.
    @dataOrder = []  # Ordered entries.

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

  setFilters: (@dataFilters) ->
    # dict[str, str | dict[str, str | dict | list]

  setTitles: (orderedTitles) ->
    # list[(str, str)]
    @dataTitles = {}
    @dataOrder = []
    for tuple in orderedTitles
      key = tuple[0]
      title = tuple[1]
      @dataTitles[key] = title
      @dataOrder.push(key)

  onSelect: ->
    return if @disableSelect

    selected_id = @uiAdd.val()

    # Change selection back to initial "---"
    @disableSelect = true
    @uiAdd.find("option:selected").removeAttr("selected")
    @uiAdd.children(":first").attr("selected", "selected")
    @disableSelect = false

    type = @dataFilters[selected_id]
    title = @dataTitles[selected_id]
    filterUi = null
    flt = null

    if type instanceof Object and "multiple" of type
      filterUi = "Objects not supported yet."
      # flt = @newFilter(selected_id, "object_" + type.multiple, title)

    else if type of @filterTypeMap
      flt = @newFilter(selected_id, type, title)


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

  newFilter: (selected_id, type, title) ->
    # Create new filter by typemap.
    flt = new @filterTypeMap[type]()
    flt.setTitle(title)

    # Each filter is numbered by count of added number of given type.
    if selected_id of @filterIds
      @filterIds[selected_id]++
    else
      @filterIds[selected_id] = 0

    flt.setId(@filterIds[selected_id])
    flt.setName(selected_id)

    return flt

  onUpdateDebug: ->
    result = []

    for queryPart in @filterList
      flt = queryPart.createFilter()
      if result.length == 0
        result.push("and")
      result.push(flt)

    asJson = JSON.stringify(result)
    @uiDebug.text(asJson)

# Publish the class.
window.QueryBuilder = QueryBuilder
