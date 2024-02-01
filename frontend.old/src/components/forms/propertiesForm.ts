import { T } from "../../translations";
import { Field } from "./models";

const t = T((r) => r.FormEditor.FormPropertiesForm);

export const propertiesFormFields: Field[] = [
  {
    name: "title",
    type: "SingleLineText",
    title: t((r) => r.title.title),
    helpText: t((r) => r.title.helpText),
  },
  {
    name: "layout",
    type: "SingleSelect",
    title: t((r) => r.layout.title),
    helpText: t((r) => r.layout.helpText),
    choices: [
      {
        value: "vertical",
        label: t((r) => r.layout.choices.vertical),
      },
      {
        value: "horizontal",
        label: t((r) => r.layout.choices.horizontal),
      },
    ],
  },
];
