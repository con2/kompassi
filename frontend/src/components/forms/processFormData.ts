import { Field, Value, Values } from "./models";

/// Implements subset of forms/utils/process_form_data.py:process_form_data
/// just enough to do what we need to do with forms client-side.
export default function processFormData(
  fields: Field[],
  formData: FormData,
  prefix: string = "",
): Values {
  const byFieldName = Object.fromEntries(formData.entries());
  const values: Values = {};

  for (const field of fields) {
    const slug = prefix ? `${prefix}.${field.slug}` : field.slug;

    switch (field.type) {
      case "Spacer":
      case "Divider":
      case "StaticText":
        break;

      case "SingleLineText":
      case "MultiLineText":
      case "SingleSelect":
      case "DateTimeField":
      case "DateField":
        values[field.slug] = byFieldName[slug] as string;
        break;

      case "NumberField":
      case "DecimalField":
        values[field.slug] = parseFloat(byFieldName[slug] as string);
        break;

      case "SingleCheckbox":
        values[field.slug] = Boolean(byFieldName[slug]);
        break;

      case "MultiItemField":
        values[field.slug] = processFormData(field.fields, formData, slug);
        break;

      default:
        // NOTE: Not exhaustive by design.
        // We don't need to implement this for all field types in the frontend.
        // const exhaustiveCheck: never = field.type;
        throw new Error(`Unsupported field type ${field.type}`);
    }
  }

  return values;
}
