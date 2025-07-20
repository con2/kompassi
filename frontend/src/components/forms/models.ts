import { ReactNode } from "react";

export type FieldType =
  | "SingleLineText"
  | "MultiLineText"
  | "Divider"
  | "StaticText"
  | "Spacer"
  | "SingleCheckbox"
  | "Tristate"
  | "SingleSelect"
  | "MultiSelect"
  | "RadioMatrix"
  | "FileUpload"
  | "NumberField"
  | "DecimalField"
  | "DateField"
  | "TimeField"
  | "DateTimeField"
  | "DimensionSingleSelect"
  | "DimensionMultiSelect"
  | "DimensionSingleCheckbox"
  | "MultiItemField";

export const fieldTypes: FieldType[] = [
  "SingleLineText",
  "MultiLineText",
  "SingleCheckbox",
  "Tristate",
  "DimensionSingleCheckbox",
  "StaticText",
  "Divider",
  "Spacer",
  "SingleSelect",
  "DimensionSingleSelect",
  "MultiSelect",
  "DimensionMultiSelect",
  "RadioMatrix",
  "FileUpload",
  "NumberField",
  "DecimalField",
  "DateField",
  "TimeField",
  "DateTimeField",
  "MultiItemField",
];

export const fieldTypesConvertibleToDimension: FieldType[] = [
  "SingleSelect",
  "MultiSelect",
  "SingleCheckbox",
];

/** These field types represent static elements on the form and don't have values. */
export const nonValueFieldTypes: FieldType[] = [
  "StaticText",
  "Divider",
  "Spacer",
];

export type HtmlType =
  | "text"
  | "email"
  | "password"
  | "datetime-local"
  | "number";

interface BaseField {
  type: FieldType;
  slug: string;
  title?: ReactNode;
  summaryTitle?: string;
  helpText?: ReactNode;
  required?: boolean;
  readOnly?: boolean;
  htmlType?: HtmlType;
  encryptTo?: string[];
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

export interface NumberField extends BaseField {
  type: "NumberField";
  decimalPlaces?: number;
  minValue?: number;
  maxValue?: number;
}

export interface DecimalField extends BaseField {
  type: "DecimalField";
  decimalPlaces?: number;
  minValue?: number;
  maxValue?: number;
}

export interface DateField extends BaseField {
  type: "DateField";
}

export interface TimeField extends BaseField {
  type: "TimeField";
}

export interface DateTimeField extends BaseField {
  type: "DateTimeField";
}

export interface SingleCheckbox extends BaseField {
  type: "SingleCheckbox";
}

export interface Tristate extends BaseField {
  type: "Tristate";
}

export interface DimensionSingleCheckbox extends BaseField {
  type: "DimensionSingleCheckbox";
  dimension: string;
}

export interface Choice {
  slug: string;
  title: string;
  disabled?: boolean; /// Only makes sense for SingleSelect with presentation="radio"
}

export type SingleSelectPresentation = "dropdown" | "radio";

export interface SingleSelect extends BaseField {
  type: "SingleSelect";
  choices: Choice[];
  presentation?: SingleSelectPresentation;
}

export interface MultiSelect extends BaseField {
  type: "MultiSelect";
  choices: Choice[];
}

export interface DimensionSingleSelect extends BaseField {
  type: "DimensionSingleSelect";
  dimension: string;
  subsetValues?: string[];
  choices: Choice[];
  presentation?: SingleSelectPresentation;
}

export interface DimensionMultiSelect extends BaseField {
  type: "DimensionMultiSelect";
  dimension: string;
  subsetValues?: string[];
  choices: Choice[];
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

interface FileUpload extends BaseField {
  type: "FileUpload";
  multiple?: boolean;
}

export interface MultiItemField extends BaseField {
  type: "MultiItemField";
  fields: Field[];
}

/// Value of a single field (without knowing its type)
export type Value =
  | string
  | number
  | boolean
  | string[]
  | Record<string, string>
  | Record<string, unknown>; /// MultiItemField
/// Values of all fields in a form
export type Values = Record<string, Value>;

export type Field =
  | SingleLineText
  | MultiLineText
  | Divider
  | Spacer
  | StaticText
  | SingleCheckbox
  | Tristate
  | SingleSelect
  | MultiSelect
  | RadioMatrix
  | FileUpload
  | NumberField
  | DecimalField
  | DateField
  | TimeField
  | DateTimeField
  | DimensionSingleSelect
  | DimensionMultiSelect
  | DimensionSingleCheckbox
  | MultiItemField;

export interface FormSchema {
  title: string;
  slug: string;
  fields: Field[];
}

export const dummyForm: FormSchema = {
  title: "Dummy form",
  slug: "dummy-form",
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

export function validateFields(fields: unknown): asserts fields is Field[] {
  // TODO
}

export type FieldSummaryType =
  | "Text"
  | "SingleCheckbox"
  | "Select"
  | "Matrix"
  | "FileUpload";

// NOTE: Keep in sync with backend/forms/utils/summarize_responses.py
export interface BaseFieldSummary {
  countResponses: number;
  countMissingResponses: number;
}

export interface TextFieldSummary extends BaseFieldSummary {
  type: "Text";
  summary: string[];
}

export interface SingleCheckboxSummary extends BaseFieldSummary {
  type: "SingleCheckbox";
}

export interface SelectFieldSummary extends BaseFieldSummary {
  type: "Select";
  summary: Record<string, number>;
}

export interface MatrixFieldSummary extends BaseFieldSummary {
  type: "Matrix";
  summary: Record<string, Record<string, number>>;
}

export interface FileUploadFieldSummary extends BaseFieldSummary {
  type: "FileUpload";
  summary: string[];
}

export type FieldSummary =
  | TextFieldSummary
  | SingleCheckboxSummary
  | SelectFieldSummary
  | MatrixFieldSummary
  | FileUploadFieldSummary;

export type Summary = Record<string, FieldSummary>;

export function validateSummary(summary: unknown): asserts summary is Summary {
  // TODO
}
