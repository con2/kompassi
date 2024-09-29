import { Field, Value, Values } from "./models";

/// Implements subset of forms/utils/process_form_data.py:process_form_data
/// just enough to do what we need to do with forms client-side.
export default function formDataToValues(
  fields: Field[],
  formData: FormData,
): Values {
  const byFieldName = Object.fromEntries(formData.entries());
  const values: Values = {};

  for (const field of fields) {
    switch (field.type) {
      case "Spacer":
      case "Divider":
      case "StaticText":
        break;

      case "SingleLineText":
      case "MultiLineText":
        values[field.slug] = byFieldName[field.slug] as string;
        break;

      case "NumberField":
        values[field.slug] = parseFloat(byFieldName[field.slug] as string);
        break;

      case "SingleCheckbox":
        values[field.slug] = Boolean(byFieldName[field.slug]);
        break;

      default:
        throw new Error(`Unsupported field type: ${field}`);
    }
  }

  return values;
}
