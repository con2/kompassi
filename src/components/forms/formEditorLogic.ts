import { Field } from "./models";

export function canMoveUp(fields: Field[], fieldName: string): boolean {
  return fieldName !== fields[0].name;
}

export function moveUp(fields: Field[], fieldName: string): Field[] {
  const index = fields.findIndex((field) => field.name === fieldName);
  return swapWithNextField(fields, index - 1);
}

export function canMoveDown(fields: Field[], fieldName: string): boolean {
  return fieldName !== fields[fields.length - 1].name;
}

export function moveDown(fields: Field[], fieldName: string): Field[] {
  const index = fields.findIndex((field) => field.name === fieldName);
  return swapWithNextField(fields, index);
}

function swapWithNextField(fields: Field[], index: number): Field[] {
  return fields
    .slice(0, index)
    .concat([fields[index + 1], fields[index]])
    .concat(fields.slice(index + 2));
}

export function removeField(fields: Field[], fieldName: string): Field[] {
  const index = fields.findIndex((field) => field.name === fieldName);

  if (index < 0) {
    throw new Error(`asked to remove nonexistent ${fieldName}`);
  }

  return fields.slice(0, index).concat(fields.slice(index + 1));
}
