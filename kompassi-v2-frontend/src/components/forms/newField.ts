import { generateUniqueIdentifier } from "@con2/components/helpers";
import type { FormEditorContext } from "./editFieldForm";
import { Field, FieldType } from "./models";

export default function newField(
  type: FieldType,
  usedIdentifiers: string[],
  formContext: FormEditorContext,
): Field {
  const slug = generateUniqueIdentifier(type, usedIdentifiers);
  // survey responses have nothing to pass dimension values forward to
  const propagation =
    formContext === "survey"
      ? {}
      : { propagateDimensionOnCreate: true, propagateDimensionOnEdit: true };
  switch (type) {
    case "Divider":
    case "Spacer":
    case "StaticText":
    case "SingleLineText":
    case "MultiLineText":
    case "MarkdownText":
    case "NumberField":
    case "DecimalField":
    case "SingleCheckbox":
    case "Tristate":
    case "FileUpload":
    case "DateField":
    case "DateTimeField":
    case "TimeField":
      return { type, slug, title: "" };
    case "SingleSelect":
    case "MultiSelect":
      return { type, slug, title: "", choices: [] };
    case "DimensionSingleSelect":
    case "DimensionMultiSelect":
      return {
        type,
        slug,
        title: "",
        choices: [],
        dimension: "",
        ...propagation,
      };
    case "DimensionSingleCheckbox":
      return { type, slug, title: "", dimension: "", ...propagation };
    case "RadioMatrix":
      return { type, slug, title: "", choices: [], questions: [] };
    case "MultiItemField":
      return { type, slug, title: "", fields: [] };
    default:
      const exhaustiveCheck: never = type;
      throw new Error(`Unknown field type ${exhaustiveCheck}`);
  }
}
