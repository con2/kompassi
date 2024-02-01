export type FieldType =
  | "SingleLineText"
  | "MultiLineText"
  | "Divider"
  | "StaticText"
  | "Spacer"
  | "SingleCheckbox"
  | "SingleSelect";

export const fieldTypes: FieldType[] = [
  "SingleLineText",
  "MultiLineText",
  "SingleCheckbox",
  "StaticText",
  "Divider",
  "Spacer",
  "SingleSelect",
];

/** These field types represent static elements on the form and don't have values. */
export const nonValueFieldTypes: FieldType[] = [
  "StaticText",
  "Divider",
  "Spacer",
];

interface BaseField {
  type: FieldType;
  name: string;
  title?: string;
  helpText?: string;
  required?: boolean;
  readOnly?: boolean;
}

export interface SingleLineText extends BaseField {
  type: "SingleLineText";
}

export interface MultiLineText extends BaseField {
  type: "MultiLineText";
  rows?: number;
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

export interface SingleCheckbox extends BaseField {
  type: "SingleCheckbox";
}

export interface Choice {
  value: string;
  label: string;
}

export interface SingleSelect extends BaseField {
  type: "SingleSelect";
  choices?: Choice[];
}

export type Field =
  | SingleLineText
  | MultiLineText
  | Divider
  | Spacer
  | StaticText
  | SingleCheckbox
  | SingleSelect;

export type Layout = "horizontal" | "vertical";
export const defaultLayout: Layout = "vertical";

export interface FormSchema {
  title: string;
  slug: string;
  fields: Field[];
  layout: Layout;
  loginRequired: boolean;
  active: boolean;
  standalone: boolean;
}

export const dummyForm: FormSchema = {
  title: "Dummy form",
  slug: "dummy-form",
  layout: "vertical",
  loginRequired: false,
  active: true,
  standalone: true,
  fields: [
    {
      type: "SingleLineText",
      title: "Required text field",
      helpText:
        "This is the help text for the required text field which is required.",
      name: "requiredField",
      required: true,
    },
    {
      type: "SingleLineText",
      title: "Optional text field",
      name: "optionalField",
    },
    {
      type: "Spacer",
      name: "spacer1",
    },
    {
      type: "SingleCheckbox",
      title: "Required checkbox",
      name: "requiredCheckbox",
      helpText: "This checkbox is required. You need to check it.",
      required: true,
    },
    {
      type: "SingleCheckbox",
      title: "Optional checkbox",
      name: "optionalCheckbox",
      helpText: "This checkbox is not required. You don't need to check it.",
      required: false,
    },
  ],
};

export const emptyField: Field = {
  type: "SingleLineText",
  title: "",
  name: "",
};
