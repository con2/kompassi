import { FileUploadFieldSummary } from "@/components/forms/models";
import UploadedFileCards from "@/components/forms/UploadedFileCards";
import { Translations } from "@/translations/en";

interface Props {
  fieldSummary: FileUploadFieldSummary;
  translations: Translations;
}

export default function FileUploadFieldSummaryComponent({
  fieldSummary,
  translations,
}: Props) {
  const t = translations.Survey;
  const { summary, countResponses, countMissingResponses } = fieldSummary;
  return (
    <>
      <UploadedFileCards urls={summary} messages={translations.SchemaForm} />
      <p className="text-muted">
        {t.attributes.countResponses}: {countResponses}.{" "}
        {t.attributes.countMissingResponses}: {countMissingResponses}.
      </p>
    </>
  );
}
