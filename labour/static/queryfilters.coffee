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
QFilterManager.registerFilter("bool", BoolFilter)


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
QFilterManager.registerFilter("str", StringFilter)
QFilterManager.registerFilter("text", StringFilter)


# EnumFilter aka OR-Object.
class EnumFilter extends QueryFilter
  _createMode: (id) ->
    """
    <select id="#{ id }" #{ @createDebugAttr() }>
      <option value="in" selected="selected">On joukossa</option>
      <option value="!in">Ei ole joukossa</option>
    </select>
    """

  _createOne: (id, key, value_title) ->
    """
    <input type="checkbox" id="#{ id }" name="#{ id }" data-key="#{ key }" #{ @createDebugAttr() } />
    <label for="#{ id }">#{ value_title }</label>
    """

  _createValues: ->
    order = @filterDef["order"]
    titles = @filterDef["values"]

    @valueIds = []
    output = ""

    for key in order
      title = titles[key]
      id = @id("v" + key)
      output += @_createOne(id, key, title)
      @valueIds.push(id)

    return output

  createUi: ->
    # Create span#id>(select#v>option*2)+(input#m$+label)*3
    group_id = @id("g")
    output = """<span id=#{ group_id }>"""
    mode_id = @id("m")
    output += @_createMode(mode_id)
    output += @_createValues()
    output += "</span>"
    return output

  createFilter: ->
    # Get the selection mode.
    mode = $("#" + @id("m")).val()
    negate = false
    if mode[0] == "!"
      negate = true

    # Find out selected enum values.
    group = $("#" + @id("g"))
    keys = []
    for valueId in @valueIds
      enumInput = $("#" + valueId + ":checked", group)
      if enumInput.length == 1
        keys.push(enumInput.data("key"))

    if keys.length == 0
      # "Empty" list (only mode and name in the list). No filter, then.
      return []

    if keys.length == 1
      # Special case for single selection: equal
      return @applyNOT(negate, ["eq", @idName, keys[0]])

    return @applyNOT(negate, ["in", @idName, keys])
QFilterManager.registerFilter("object_or", EnumFilter, (filterDef) ->
  return "multiple" of filterDef and filterDef.multiple is "or"
)

