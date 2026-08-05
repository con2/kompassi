import { slugifyDash } from "@con2/components/helpers";

const tryFields = ["slug", "title_en", "title_fi", "title_sv"];

/// Try earnest to force a valid slug into the form data.
export function forceSlug(
  formData: Record<string, FormDataEntryValue>,
  slugify: typeof slugifyDash = slugifyDash,
): Record<string, FormDataEntryValue> {
  const newFormData = { ...formData };

  for (const field of tryFields) {
    if (typeof newFormData[field] === "string" && newFormData[field]) {
      const slug = slugify("" + newFormData[field]);
      newFormData.slug = slug;
      break;
    }
  }

  return newFormData;
}
