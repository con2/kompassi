import { T } from "../../translations";
import { Field } from "./models";

const tEditor = T((r) => r.FormEditor.EditFieldForm);

const nameField: Field = {
  type: "SingleLineText",
  name: "name",
  title: tEditor((r) => r.name.title),
  helpText: tEditor((r) => r.name.helpText),
  required: true,
};

const baseFieldEditorFields: Field[] = [
  nameField,
  {
    type: "SingleLineText",
    name: "title",
    title: tEditor((r) => r.title.title),
    helpText: tEditor((r) => r.title.helpText),
    required: false,
  },
  {
    type: "MultiLineText",
    name: "helpText",
    title: tEditor((r) => r.helpText.title),
    helpText: tEditor((r) => r.helpText.helpText),
    required: false,
  },
  {
    type: "SingleCheckbox",
    name: "required",
    title: tEditor((r) => r.required.title),
    required: false,
  },
];

export const fieldEditorMapping = {
  SingleLineText: baseFieldEditorFields,
  MultiLineText: baseFieldEditorFields,
  Divider: [nameField],
  StaticText: baseFieldEditorFields,
  SingleCheckbox: baseFieldEditorFields,
  Spacer: [nameField],
};
