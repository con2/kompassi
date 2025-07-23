import slugify from "./slugify";

// TODO camelCase3 would be better than snake-case-3
export default function generateUniqueIdentifier(
  base: string,
  usedIdentifiers: string[],
): string {
  base = slugify(base) || "field";
  let result = base;
  let counter = 1;

  while (usedIdentifiers.includes(result)) {
    counter += 1;
    result = `${base}-${counter}`;
  }

  return result;
}
