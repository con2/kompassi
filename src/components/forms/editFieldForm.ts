import { T } from "../../translations";
import { Field } from "./models";

const t = T((r) => r.FormEditor.EditFieldForm);

const nameField: Field = {
  type: "SingleLineText",
  name: "name",
  title: t((r) => r.name.title),
  helpText: t((r) => r.name.helpText),
  required: true,
};

const baseFieldEditorFields: Field[] = [
  nameField,
  {
    type: "SingleLineText",
    name: "title",
    title: t((r) => r.title.title),
    helpText: t((r) => r.title.helpText),
    required: false,
  },
  {
    type: "MultiLineText",
    name: "helpText",
    title: t((r) => r.helpText.title),
    helpText: t((r) => r.helpText.helpText),
    required: false,
  },
  {
    type: "SingleCheckbox",
    name: "required",
    title: t((r) => r.required.title),
    required: false,
  },
];

const optionsField: Field = {
  type: "MultiLineText",
  name: "options",
  title: t((r) => r.options.title),
  helpText: t((r) => r.options.helpText),
  required: true,
};

export const fieldEditorMapping = {
  SingleLineText: baseFieldEditorFields,
  MultiLineText: baseFieldEditorFields,
  Divider: [nameField],
  StaticText: baseFieldEditorFields,
  SingleCheckbox: baseFieldEditorFields,
  SingleSelect: baseFieldEditorFields.concat([optionsField]),
  Spacer: [nameField],
};
