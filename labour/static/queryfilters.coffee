# Base class for various query filter implementations.
# A subclass must implement {QueryFilter#createUi} and {QueryFilter#createFilter}.
class QueryFilter
  constructor: (selectedId, filterDef) ->
    @debugHandler = null  # Handler script to execute on element change.
    @idName = selectedId  # Backend-related name of the filter.
    @idNumber = null  # Index number of added filter (of type @idName).
    @filterDef = filterDef  # Filter definition from backend. A string or object.

  # Set display name of the property/filterable.
  setTitle: (uiTitle) ->
    @uiTitle = uiTitle

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

  setDebugAttr: (target, attr = "onchange") ->
    target.attr(attr, @debugHandler) if @debugHandler?

  # Yield label-tag for given name using default display name.
  labelFor: (id, title = @uiTitle) ->
    return Widget.label(id).text(title)

  # Yield id-name for this filter with optional suffix.
  id: (suff = null) ->
    return @idName + "_" + @idNumber if suff == null
    return @idName + "_" + suff + "_" + @idNumber

  # Yield display name -element.
  title: ->
    return $("<span class=\"title\">").text(@uiTitle)

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
  createRadio: (id, name, value) ->
    return @setDebugAttr(Widget.radio(id).attr("name", name).val(value))

  createUi: ->
    name = @id()
    id_true = @id("true")
    id_false = @id("false")
    output = $("<span id=\"#{ name }\">")
    output.append(@labelFor(id_true, "Kyllä"), @createRadio(id_true, name, "true").attr("checked", "checked"))
    output.append(@labelFor(id_false, "Ei"), @createRadio(id_false, name, "false"))
    return output

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
      <option value="exact">On</option>
      <option value="!exact">Ei ole</option>
      <option value="regex">Regex</option>
      <option value="!regex">Ei regex</option>
    </select>
    """

  # Yield input text input.
  #
  # @private
  # @param id [String] Unique id for the input.
  createInput: (id) ->
    return @setDebugAttr(Widget.text(id).attr("name", id))

  createCase: (id) ->
    return [
      @setDebugAttr(Widget.checkbox(id).attr("name", id)),
      Widget.label(id).text("Sama kirjainkoko")
    ]

  createUi: ->
    # Title [MatchMethod] [StringInput] [Case sensitive]
    output = $("<span>")
    output.append(@createMode(@id("mode")))
    output.append(@createInput(@id()))
    output.append(@createCase(@id("case")))

  createFilter: ->
    mode = $("#" + @id("mode")).val()
    value = $("#" + @id()).val()
    if not mode? or mode == ""
      throw "Invalid select value for string mode."

    negate = false
    if mode[0] == "!"
      mode = mode.substr(1)
      negate = true

    value = "" if not value?
    if mode == "contains" and value == ""
      return null

    icase = $("#" + @id("case") + ":checked")
    if icase.size() != 1
      mode = "i" + mode

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

  _createOne: (output, id, key, value_title) ->
    input = Widget.checkbox(id)
    input.data("key", key)
    @setDebugAttr(input)

    label = Widget.label(id)
    label.text(value_title)

    output.append(input)
    output.append(label)

  _createValues: (output) ->
    order = @filterDef["order"]
    titles = @filterDef["values"]
    @valueIds = []

    for key in order
      title = titles[key]
      id = @id("v" + key)
      @_createOne(output, id, key, title)
      @valueIds.push(id)

  createUi: ->
    # Create span#id>(select#v>option*2)+(input#m$+label)*3
    group_id = @id("g")
    output = $("""<span id="#{ group_id }">""")

    mode_id = @id("m")
    output.html(@_createMode(mode_id))
    @_createValues(output)
    return output

  createFilter: ->
    # Get the selection mode.
    mode = $("#" + @id("m")).val()
    negate = mode[0] == "!"

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


# M2M Filter aka AND-Object.
class M2MFilter extends QueryFilter
  _createMode: (id) ->
     """
    <select id="#{ id }" #{ @createDebugAttr() }>
      <option value="eq" selected="selected">On</option>
      <option value="!eq">Ei ole</option>
    </select>
    """

  _createOne: (key, title) ->
    one = $("<option>")
    if key?
      one.data("key", key)
      one.val(key)
    else
      one.attr("disabled", "disabled")
      one.attr("selected", "selected")
    one.text(title)
    return one

  createUi: ->
    output = $("<span>")
    output.append(@_createMode(@id("m")))

    sel = $("""<select id="#{ @id("s") }" #{ @createDebugAttr() }>""")
    sel.append(@_createOne(null, "---"))

    order = @filterDef["order"]
    titles = @filterDef["values"]
    for key in order
      title = titles[key]
      one = @_createOne(key, title)
      sel.append(one)

    output.append(sel)
    return output

  createFilter: ->
    value_key = $("#" + @id("s") + ">:selected")
    if value_key.attr("disabled")?
      return []

    value_key = value_key.data("key")

    mode = $("#" + @id("m")).val()
    negate = mode[0] == "!"

    return @applyNOT(negate, ["eq", @idName, value_key])
QFilterManager.registerFilter("object_and", EnumFilter, (filterDef) ->
  return "multiple" of filterDef and filterDef.multiple is "and"
)


class DateTimeFilter extends QueryFilter
  _join: (left, join, right, hasLeft, hasRight) ->
    ret = ""
    ret += left if hasLeft
    ret += join if hasLeft and hasRight
    ret += right if hasRight
    return ret

  _createFormat: (filterDef) ->
    hasTime = filterDef is "datetime" or filterDef is "time"
    hasDate = filterDef is "datetime" or filterDef is "date"

    # Placeholder text in the input field.
    placeholder = @_join("pp.kk.vvvv", " ", "hh:mm(:ss)", hasDate, hasTime)

    # Apparently, moment allows to replace ":" with any separator when parsing. So no need to add those.
    parse = @_join("D.M.YYYY", " ", "H:m", hasDate, hasTime)
    if hasTime
      parse = [
        parse,
        @_join("D.M.YYYY", " ", "H:m:s", hasDate, hasTime)
      ]

    # Transport format, RFC8601, or similar. Only datetime has tz info added.
    time = "HH:mm:ss"
    time += "ZZ" if hasDate
    transport = @_join("YYYY-MM-DD", "[T]", time, hasDate, hasTime)

    return placeholder: placeholder, parse: parse, transport: transport

  _createMode: (id) ->
    # For non-datetime fields, equal comparisons are allowed.
    if @filterDef isnt "datetime"
      parts = """
        <option value="eq" selected="selected">On</option>
        <option value="!eq">Ei ole</option>
        <option value="lt">Ennen</option>
        <option value="lte">Ennen (tai tasan)</option>
        <option value="gt">Jälkeen</option>
        <option value="gte">Jälkeen (tai tasan)</option>
        """
    else
      parts = """
        <option value="lt" selected="selected">Ennen</option>
        <option value="gt">Jälkeen</option>
        """
    """
    <select id="#{ id }" #{ @createDebugAttr() }>#{ parts }
    </select>
    """

  createUi: (filterDef=@filterDef) ->
    format = @_createFormat(filterDef)

    match = @_createMode(@id("m"))
    value = @setDebugAttr(Widget.text(@id("v")))
    value.attr("placeholder", format.placeholder)

    output = $("<span>")
    output.append(match, value)
    return output

  createFilter: ->
    format = @_createFormat(@filterDef)

    # The mode selector.
    mode = $("#" + @id("m")).val()
    negate = false
    if mode[0] == "!"
      mode = mode.substr(1)
      negate = true

    # The written value.
    value = $("#" + @id("v")).val()

    #noinspection JSCheckFunctionSignatures
    value_obj = moment(value, format.parse)
    if not value_obj.isValid()
      return null
    value_obj.utc() if @filterDef is "datetime"

    flt = [mode, @idName, value_obj.format(format.transport)]
    return @applyNOT(negate, flt)
QFilterManager.registerFilter("date", DateTimeFilter)
QFilterManager.registerFilter("time", DateTimeFilter)
QFilterManager.registerFilter("datetime", DateTimeFilter)
