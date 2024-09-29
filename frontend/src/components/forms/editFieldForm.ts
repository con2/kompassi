import formDataToValues from "./formDataToValues";
import { Choice, Field, FieldType, SelectField, Value } from "./models";
import type { Translations } from "@/translations/en";

export function getFieldEditorFields(
  fieldType: FieldType,
  messages: Translations["FormEditor"]["editFieldForm"],
): Field[] {
  const t = messages;
  const slugField: Field = {
    type: "SingleLineText",
    slug: "slug",
    required: true,
    ...t.slug,
  };

  const baseFieldEditorFields: Field[] = [
    slugField,
    {
      type: "SingleLineText",
      slug: "title",
      required: false,
      ...t.title,
    },
    {
      type: "MultiLineText",
      slug: "helpText",
      required: false,
      ...t.helpText,
    },
    {
      type: "SingleCheckbox",
      slug: "required",
      required: false,
      ...t.required,
    },
  ];

  const choicesField: Field = {
    type: "MultiLineText",
    slug: "choices",
    required: true,
    ...t.choices,
  };

  const questionsField: Field = {
    type: "MultiLineText",
    slug: "questions",
    required: true,
    ...t.questions,
  };

  switch (fieldType) {
    case "SingleSelect":
    case "MultiSelect":
      return baseFieldEditorFields.concat([choicesField]);
    case "RadioMatrix":
      return baseFieldEditorFields.concat([questionsField, choicesField]);
    case "Divider":
    case "Spacer":
      return [slugField];
    default:
      return baseFieldEditorFields;
  }
}

function formatChoices(choices: Choice[]): string {
  return choices.map((choice) => `${choice.slug}: ${choice.title}`).join("\n");
}

export function fieldToValues(field: Field): Record<string, any> {
  let choices: string | undefined = undefined;
  let questions: string | undefined = undefined;

  switch (field.type) {
    case "SingleSelect":
    case "MultiSelect":
      choices = formatChoices(field.choices);
      break;
    case "RadioMatrix":
      choices = formatChoices(field.choices);
      questions = formatChoices(field.questions);
      break;
  }

  return { ...field, choices, questions };
}

function parseChoices(choices: string): Choice[] {
  return choices
    .split("\n")
    .map((line) => {
      const [slug, ...titleParts] = line.split(": ");
      const title = titleParts.join(": ");
      return { slug, title };
    })
    .filter((choice) => choice.slug && choice.title);
}

export function formDataToField(
  fields: Field[],
  initialValues: Field,
  formData: FormData,
): Field {
  const values = formDataToValues(fields, formData);

  switch (initialValues.type) {
    case "SingleSelect":
    case "MultiSelect":
      return {
        ...initialValues,
        ...values,
        choices: parseChoices(values.choices as string),
      };
    case "RadioMatrix":
      return {
        ...initialValues,
        ...values,
        choices: parseChoices(values.choices as string),
        questions: parseChoices(values.questions as string),
      };
    default:
      return { ...initialValues, ...values };
  }
}
