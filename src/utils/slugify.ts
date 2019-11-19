const charMap = {
  ' ': '-',
  '.': '-',
  _: '-',
  à: 'a',
  á: 'a',
  ä: 'a',
  å: 'a',
  è: 'e',
  é: 'e',
  ë: 'e',
  ö: 'o',
  ü: 'u',
};

export default function slugify(ustr: string) {
  ustr = ustr.toLowerCase();

  // rationale for any: property access has a default when undefined
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  ustr = Array.prototype.map.call(ustr, (c: string) => (charMap as any)[c] || c).join('');

  return ustr.replace(/[^a-z0-9-]/g, '').replace(/-+/g, '-');
}
