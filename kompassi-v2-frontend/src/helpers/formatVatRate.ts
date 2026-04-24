export default function formatVatRate(value: string, locale: string = "en") {
  const num = parseFloat(value);
  const formatted = num.toString();
  if (locale === "fi" || locale === "sv") {
    return formatted.replace(".", ",");
  }
  return formatted;
}
