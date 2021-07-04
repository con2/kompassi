import * as yup from "yup";
import { Field, FormSchema, nonValueFieldTypes } from "./models";

function fieldToYup(field: Field) {
  let validator: yup.AnySchema = yup.string();

  switch (field.type) {
    case "SingleCheckbox":
      validator = yup.boolean();
      if (field.required) {
        validator = validator.oneOf([true]);
      }
  }

  if (field.required) {
    validator = validator.required();
  }

  return validator;
}

export function fieldsToYup(fields: Field[]) {
  let validator = yup.object();

  for (const field of fields) {
    if (nonValueFieldTypes.includes(field.type)) {
      continue;
    }

    validator = validator.shape({ [field.name]: fieldToYup(field) });
  }

  return validator.noUnknown(true).required().strict();
}
