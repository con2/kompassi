/// Parses the hidden `recipientFilters` form field (a JSON-encoded OR-of-AND-groups
/// array produced by RecipientFilterEditor). Returns [] when absent/empty, and throws a
/// clear error instead of a raw SyntaxError if the value is present but not valid JSON,
/// so a tampered submission fails cleanly rather than as an opaque 500.
export default function parseRecipientFilters(
  raw: FormDataEntryValue | null,
): unknown {
  if (typeof raw !== "string" || !raw) {
    return [];
  }

  try {
    return JSON.parse(raw);
  } catch {
    throw new Error("Invalid recipientFilters: not valid JSON");
  }
}
