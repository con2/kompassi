const charMap: Record<string, string> = {
  " ": "-",
  ".": "-",
  _: "-",
  à: "a",
  á: "a",
  ä: "a",
  å: "a",
  è: "e",
  é: "e",
  ë: "e",
  ö: "o",
  ü: "u",
};

export function slugifyDash(ustr: string) {
  ustr = ustr.toLowerCase();
  ustr = Array.prototype.map.call(ustr, (c) => charMap[c] || c).join("");
  return ustr
    .replace(/[^a-z0-9-]/g, "")
    .replace(/-+/g, "-") // collapse multiple dashes
    .replace(/-$/, "") // remove trailing dash
    .replace(/^-/, ""); // remove leading dash
}

export function slugifyUnderscore(ustr: string) {
  return slugifyDash(ustr).replace(/-/g, "_");
}

export default slugifyDash;
