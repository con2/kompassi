export default function searchParamsToFormData(
  searchParams: URLSearchParams,
): FormData {
  console.log("searchParamsToFormData", {
    searchParams: Object.fromEntries(searchParams.entries()),
  });
  const formData = new FormData();

  for (const [key, value] of searchParams.entries()) {
    formData.append(key, value);
  }

  return formData;
}
