export default function searchParamsToFormData(
  searchParams: URLSearchParams,
): FormData {
  const formData = new FormData();

  for (const [key, value] of searchParams.entries()) {
    formData.append(key, value);
  }

  return formData;
}
