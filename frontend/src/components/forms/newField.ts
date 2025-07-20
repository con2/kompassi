import { Field, FieldType } from "./models";
import generateUniqueIdentifier from "@/helpers/generateUniqueIdentifier";

export default function newField(
  type: FieldType,
  usedIdentifiers: string[],
): Field {
  const slug = generateUniqueIdentifier(type, usedIdentifiers);
  switch (type) {
    case "Divider":
    case "Spacer":
    case "StaticText":
    case "SingleLineText":
    case "MultiLineText":
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
      return { type, slug, title: "", choices: [], dimension: "" };
    case "DimensionSingleCheckbox":
      return { type, slug, title: "", dimension: "" };
    case "RadioMatrix":
      return { type, slug, title: "", choices: [], questions: [] };
    case "MultiItemField":
      return { type, slug, title: "", fields: [] };
    default:
      const exhaustiveCheck: never = type;
      throw new Error(`Unknown field type ${exhaustiveCheck}`);
  }
}
