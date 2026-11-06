/// HTML `pattern` attribute values. The browser anchors them at both ends and compiles them
/// with the `v` flag, under which a literal dash inside a character class must be escaped.

/// Must accept exactly what `validate_slug` in kompassi/core/utils/model_utils.py accepts,
/// or the browser lets through slugs the backend then rejects with a generic error.
export const slugPattern = "[a-z0-9\\-]+";

/// Form field technical names are not validated by the backend. Dashes and dots stay allowed
/// because existing fields use them: older generated names have dashes, and fields promoted
/// to dimensions are named `prefix.dimension-slug`.
export const fieldSlugPattern = "[a-z0-9_.\\-]+";

export function matchesPattern(value: string, pattern: string): boolean {
  return new RegExp(`^(?:${pattern})$`).test(value);
}
