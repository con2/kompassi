import { Field, nonValueFieldTypes } from "./models";

export function canMoveUp(fields: Field[], slug: string): boolean {
  return slug !== fields[0].slug;
}

export function moveUp(fields: Field[], slug: string): Field[] {
  const index = fields.findIndex((field) => field.slug === slug);
  return swapWithNextField(fields, index - 1);
}

export function canMoveDown(fields: Field[], slug: string): boolean {
  return slug !== fields[fields.length - 1].slug;
}

export function moveDown(fields: Field[], slug: string): Field[] {
  const index = fields.findIndex((field) => field.slug === slug);
  return swapWithNextField(fields, index);
}

function swapWithNextField(fields: Field[], index: number): Field[] {
  return fields
    .slice(0, index)
    .concat([fields[index + 1], fields[index]])
    .concat(fields.slice(index + 2));
}

export function removeField(fields: Field[], slug: string): Field[] {
  const index = fields.findIndex((field) => field.slug === slug);

  if (index < 0) {
    throw new Error(`asked to remove nonexistent ${slug}`);
  }

  return fields.slice(0, index).concat(fields.slice(index + 1));
}

export function replaceField(fields: Field[], slug: string, newField: Field) {
  const index = fields.findIndex((field) => field.slug === slug);

  if (index < 0) {
    throw new Error(`asked to edit nonexistent ${slug}`);
  }

  return fields
    .slice(0, index)
    .concat([newField])
    .concat(fields.slice(index + 1));
}

export function addField(fields: Field[], newField: Field, aboveslug?: string) {
  if (aboveslug) {
    const index = fields.findIndex((field) => field.slug === aboveslug);

    if (index < 0) {
      throw new Error(`asked to addFieldAbove nonexistent ${aboveslug}`);
    }

    return fields
      .slice(0, index)
      .concat([newField])
      .concat(fields.slice(index));
  } else {
    return fields.concat([newField]);
  }
}
