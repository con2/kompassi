import { Choice, SelectFieldSummary } from "@/components/forms/models";
import { Translations } from "@/translations/en";

interface SelectFieldSummaryComponentProps {
  translations: Translations;
  choices: Choice[];
  fieldSummary: SelectFieldSummary;
  showMissingResponses?: boolean;
}

export default function SelectFieldSummaryComponent({
  translations,
  choices,
  fieldSummary,
  showMissingResponses = true,
}: SelectFieldSummaryComponentProps) {
  const { countResponses, countMissingResponses, summary } = fieldSummary;
  const t = translations.Survey;

  return (
    <table className="table table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">{t.attributes.choice}</th>
          <th scope="col">{t.attributes.percentageOfResponses}</th>
          <th scope="col">{t.attributes.countResponses}</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(summary).map(([choiceSlug, countThisChoice]) => {
          const choice = choices.find((c) => c.slug === choiceSlug);
          const choiceTitle = choice?.title || (
            <>
              <span title={t.warnings.choiceNotFound}>⚠️</span>{" "}
              <em>{choiceSlug}</em>
            </>
          );
          const percentage = countResponses
            ? Math.round((countThisChoice / countResponses) * 100)
            : 0;

          return (
            <tr key={choiceSlug}>
              <td className="align-middle" scope="row">
                {choiceTitle}
              </td>
              <td className="align-middle" style={{ width: "30%" }}>
                <div className="progress">
                  <div
                    className="progress-bar"
                    role="progressbar"
                    style={{
                      width: `${percentage}%`,
                    }}
                    aria-valuenow={percentage}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  >
                    {percentage}%
                  </div>
                </div>
              </td>
              <td className="align-middle" style={{ width: "10%" }}>
                {countThisChoice}
              </td>
            </tr>
          );
        })}
        {showMissingResponses && (
          <tr>
            <td>
              ❓{" "}
              <em className="text-muted">
                {t.attributes.countMissingResponses}
              </em>
            </td>
            <td></td>
            <td>
              <span className="text-muted">{countMissingResponses}</span>
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
}
