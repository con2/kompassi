import { Choice, Field } from "./models";

export default function makeInputId(
  idPrefix: string,
  field: Field,
  choice?: Choice,
) {
  const parts = [];

  if (idPrefix) {
    parts.push(idPrefix);
  }
  parts.push(field.slug);
  if (choice) {
    parts.push(choice.slug);
  }

  return parts.join("-");
}
