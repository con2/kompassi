import { Field, Values } from "./models";

const falsyValues = new Set(["false", "0", "off", "no"]);

/// Implements subset of forms/utils/process_form_data.py:process_form_data
/// just enough to do what we need to do with forms client-side.
export default function processFormData(
  fields: Field[],
  formData: FormData,
  slugPrefix: string = "",
): Values {
  const byFieldName = Object.fromEntries(formData.entries());
  const values: Values = {};

  for (const field of fields) {
    const slug = slugPrefix ? `${slugPrefix}.${field.slug}` : field.slug;
    const type = field.type;

    switch (type) {
      case "Spacer":
      case "Divider":
      case "StaticText":
        break;

      case "SingleLineText":
      case "MultiLineText":
      case "SingleSelect":
      case "DimensionSingleSelect":
      case "DateTimeField":
      case "DateField":
      case "TimeField":
        values[field.slug] = byFieldName[slug] as string;
        break;

      case "MultiSelect":
      case "DimensionMultiSelect":
        const choicesPrefix = `${slug}.`;
        for (const [key, value] of Object.entries(byFieldName)) {
          if (key.startsWith(choicesPrefix)) {
            const choiceSlug = key.slice(choicesPrefix.length);
            if (
              typeof byFieldName[key] === "string" &&
              !falsyValues.has(byFieldName[key])
            ) {
              const chosen = (values[choiceSlug] ??= []) as string[];
              chosen.push(value as string);
            }
          }
        }
        break;

      case "RadioMatrix":
        const matrixValues: Record<string, string> = {};
        for (const question of field.questions) {
          const questionSlug = `${slug}.${question.slug}`;
          const value = byFieldName[questionSlug];
          if (value !== undefined) {
            matrixValues[question.slug] = value as string;
          }
        }
        break;

      case "NumberField":
      case "DecimalField":
        values[field.slug] = parseFloat(byFieldName[slug] as string);
        break;

      case "SingleCheckbox":
      case "DimensionSingleCheckbox":
        // "checked" => true
        // "" => false
        // undefined => false
        values[field.slug] = Boolean(byFieldName[slug]);
        break;

      case "Tristate":
        if (byFieldName[slug] === "true") {
          values[field.slug] = true;
        } else if (byFieldName[slug] === "false") {
          values[field.slug] = false;
        } else {
          values[field.slug] = null;
        }
        break;

      case "MultiItemField":
        values[field.slug] = processFormData(field.fields, formData, slug);
        break;

      case "FileUpload":
        console.warn(
          "processFormData: FileUpload is not supported client-side",
          field,
        );
        break;

      default:
        const exhaustiveCheck: never = type;
        throw new Error(`Unsupported field type ${exhaustiveCheck}`);
    }
  }

  return values;
}
