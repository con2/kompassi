import { FormsFormLayoutChoices } from "@/__generated__/graphql";

export type FieldType =
  | "SingleLineText"
  | "MultiLineText"
  | "Divider"
  | "StaticText"
  | "Spacer"
  | "SingleCheckbox"
  | "SingleSelect"
  | "MultiSelect"
  | "RadioMatrix";

export const fieldTypes: FieldType[] = [
  "SingleLineText",
  "MultiLineText",
  "SingleCheckbox",
  "StaticText",
  "Divider",
  "Spacer",
  "SingleSelect",
  "MultiSelect",
  "RadioMatrix",
];

/** These field types represent static elements on the form and don't have values. */
export const nonValueFieldTypes: FieldType[] = [
  "StaticText",
  "Divider",
  "Spacer",
];

export type HtmlType =
  | "text"
  | "number"
  | "email"
  | "password"
  | "datetime-local";

interface BaseField {
  type: FieldType;
  slug: string;
  title?: string;
  helpText?: string;
  required?: boolean;
  readOnly?: boolean;
  htmlType?: string;
}

export interface Divider extends BaseField {
  type: "Divider";
}

export interface Spacer extends BaseField {
  type: "Spacer";
}

export interface StaticText extends BaseField {
  type: "StaticText";
}

export interface SingleLineText extends BaseField {
  type: "SingleLineText";
}

export interface MultiLineText extends BaseField {
  type: "MultiLineText";
  rows?: number;
}

export interface SingleLineText extends BaseField {
  type: "SingleLineText";
}

export interface SingleCheckbox extends BaseField {
  type: "SingleCheckbox";
}

export interface Choice {
  slug: string;
  title: string;
}

export type SingleSelectPresentation = "dropdown" | "radio";

export interface SingleSelect extends BaseField {
  type: "SingleSelect";
  choices: Choice[];
  presentation: SingleSelectPresentation;
}

export interface MultiSelect extends BaseField {
  type: "MultiSelect";
  choices: Choice[];
}

/**
 * choices are columns, questions are rows
 */
interface RadioMatrix extends BaseField {
  type: "RadioMatrix";
  questions: Choice[];
  choices: Choice[];
}

export type Layout = FormsFormLayoutChoices;
export const Layout = FormsFormLayoutChoices;

export const defaultLayout = Layout.Horizontal;

export type Field =
  | SingleLineText
  | MultiLineText
  | Divider
  | Spacer
  | StaticText
  | SingleCheckbox
  | SingleSelect
  | MultiSelect
  | RadioMatrix;

export interface FormSchema {
  title: string;
  slug: string;
  fields: Field[];
  layout: Layout;
}

export const dummyForm: FormSchema = {
  title: "Dummy form",
  slug: "dummy-form",
  layout: Layout.Horizontal,
  fields: [
    {
      type: "SingleLineText",
      title: "Required text field",
      helpText:
        "This is the help text for the required text field which is required.",
      slug: "requiredField",
      required: true,
    },
    {
      type: "SingleLineText",
      title: "Optional text field",
      slug: "optionalField",
    },
    {
      type: "Spacer",
      slug: "spacer-1",
    },
    {
      type: "SingleCheckbox",
      title: "Required checkbox",
      slug: "requiredCheckbox",
      helpText: "This checkbox is required. You need to check it.",
      required: true,
    },
    {
      type: "SingleCheckbox",
      title: "Optional checkbox",
      slug: "optionalCheckbox",
      helpText: "This checkbox is not required. You don't need to check it.",
      required: false,
    },
  ],
};

export const emptyField: Field = {
  type: "SingleLineText",
  title: "",
  slug: "",
};
