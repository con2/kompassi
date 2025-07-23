import { TextFieldSummary } from "@/components/forms/models";
import Linebreaks from "@/components/helpers/Linebreaks";
import { Translations } from "@/translations/en";

interface TextFieldSummaryComponentProps {
  fieldSummary: TextFieldSummary;
  translations: Translations;
}

export default function TextFieldSummaryComponent({
  fieldSummary,
  translations,
}: TextFieldSummaryComponentProps) {
  const t = translations.Survey;
  const { summary, countResponses, countMissingResponses } = fieldSummary;
  return (
    <>
      {fieldSummary.summary.map((item, idx) => (
        <div key={idx} className="card mb-2">
          <div className="card-body p-2 ps-3 pe-3">
            <Linebreaks text={item} />
          </div>
        </div>
      ))}
      <p className="text-muted">
        {t.attributes.countResponses}: {countResponses}.{" "}
        {t.attributes.countMissingResponses}: {countMissingResponses}.
      </p>
    </>
  );
}
