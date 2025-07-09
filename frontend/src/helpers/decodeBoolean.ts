export const falsyValues = ["false", "0", "no", "off", ""];

export function decodeBoolean(strBool: string): boolean {
  return !falsyValues.includes(strBool.toLowerCase());
}
