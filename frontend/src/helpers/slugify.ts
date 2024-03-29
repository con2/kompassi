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

export default function slugify(ustr: string) {
  ustr = ustr.toLowerCase();
  ustr = Array.prototype.map.call(ustr, (c) => charMap[c] || c).join("");
  return ustr.replace(/[^a-z0-9-]/g, "").replace(/-+/g, "-");
}
