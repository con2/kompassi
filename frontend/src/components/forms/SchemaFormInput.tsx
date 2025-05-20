import { Temporal } from "@js-temporal/polyfill";
import type { Field } from "./models";
import UploadedFileCards from "./UploadedFileCards";
import { timezone } from "@/config";
import type { Translations } from "@/translations/en";

interface SchemaFormInputProps {
  field: Field;
  value?: any;
  readOnly?: boolean;
  messages: Translations["SchemaForm"];
}

const defaultRows = 8;

/// Full ISO 8601 to YYYY-MM-DDTHH:MM in local time.
/// This is used to render the value attribute of <input type="datetime-local">.
function dateTimeToHtml(value: string) {
  return Temporal.Instant.from(value)
    .toZonedDateTimeISO(timezone)
    .toString()
    .slice(0, 16);
}

/** SchemaFormInput is responsible for rendering the actual input component. */
function SchemaFormInput({
  field,
  value,
  messages,
  readOnly: elementReadOnly = false,
}: SchemaFormInputProps) {
  const {
    slug,
    type,
    required,
    htmlType,
    readOnly: fieldReadOnly = false,
  } = field;
  const readOnly = elementReadOnly || fieldReadOnly;

  // TODO: make id unique in a deterministic fashion
  switch (type) {
    case "Spacer":
    case "Divider":
    case "StaticText":
      return null;
    case "SingleLineText":
      return (
        <input
          className="form-control"
          type={htmlType ?? "text"}
          defaultValue={value}
          required={required}
          readOnly={readOnly}
          id={slug}
          name={slug}
        />
      );
    case "MultiLineText":
      return (
        <textarea
          className="form-control"
          rows={field.rows ?? defaultRows}
          defaultValue={value}
          required={required}
          readOnly={readOnly}
          id={slug}
          name={slug}
        />
      );
    case "NumberField":
    case "DecimalField":
      return (
        <input
          className="form-control"
          type="number"
          defaultValue={value}
          required={required}
          readOnly={readOnly}
          id={slug}
          name={slug}
          step={field.decimalPlaces ? 1 / 10 ** field.decimalPlaces : 1}
          inputMode={field.decimalPlaces ? "decimal" : "numeric"}
          min={field.minValue}
          max={field.maxValue}
        />
      );
    case "SingleCheckbox":
    case "DimensionSingleCheckbox":
      return (
        <input
          className="form-check-input"
          type="checkbox"
          defaultChecked={!!value}
          required={required}
          disabled={readOnly}
          id={slug}
          name={slug}
        />
      );
    case "SingleSelect":
    case "DimensionSingleSelect":
      let choices = field.choices ?? [];

      switch (field.presentation) {
        case "dropdown":
          choices = [{ slug: "", title: "" }, ...field.choices];

          return (
            <select
              className="form-select"
              required={required}
              disabled={readOnly}
              id={slug}
              name={slug}
              defaultValue={value}
            >
              {choices.map((choice) => (
                <option value={choice.slug} key={choice.slug}>
                  {choice.title}
                </option>
              ))}
            </select>
          );
        case "radio":
        default:
          // radio button group
          return (
            <>
              {choices.map((choice) => (
                <div key={choice.slug} className="mb-2">
                  <input
                    className="form-check-input"
                    type="radio"
                    required={required}
                    disabled={readOnly}
                    id={choice.slug}
                    name={slug}
                    value={choice.slug}
                    defaultChecked={choice.slug === value}
                  />{" "}
                  <label htmlFor={choice.slug} className="form-check-label">
                    {choice.title}
                  </label>
                </div>
              ))}
            </>
          );
      }
    case "MultiSelect":
    case "DimensionMultiSelect":
      return (
        <>
          {field.choices?.map((choice) => {
            const name = `${field.slug}.${choice.slug}`;
            return (
              <div key={choice.slug} className="mb-2">
                <input
                  className="form-check-input"
                  type="checkbox"
                  defaultChecked={value?.includes(choice.slug)}
                  disabled={readOnly}
                  id={name}
                  name={name}
                />{" "}
                <label htmlFor={name} className="form-check-label">
                  {choice.title}
                </label>
              </div>
            );
          })}
        </>
      );
    case "RadioMatrix":
      const questions = field.questions ?? [];
      return (
        <table className="table table-striped">
          <thead>
            <tr>
              <th></th>
              {field.choices?.map((choice) => (
                <th key={choice.slug} scope="col">
                  {choice.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {questions.map((question) => (
              <tr key={question.slug}>
                <td scope="row">{question.title}</td>
                {field.choices?.map((choice) => (
                  <td key={choice.slug}>
                    <input
                      className="form-check-input"
                      type="radio"
                      required={required}
                      disabled={readOnly}
                      name={`${field.slug}.${question.slug}`}
                      value={choice.slug}
                      defaultChecked={choice.slug === value?.[question.slug]}
                      title={`${choice.title}`}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      );
    case "FileUpload":
      if (readOnly) {
        return <UploadedFileCards urls={value} messages={messages} />;
      } else {
        // TODO what if readOnly or value but not both?
        return (
          <input
            className="form-control"
            type="file"
            id={slug}
            name={slug}
            required={required}
            multiple={field.multiple}
          />
        );
      }
    case "DateField":
      return (
        <input
          className="form-control"
          type={"date"}
          defaultValue={value}
          required={required}
          readOnly={readOnly}
          id={slug}
          name={slug}
        />
      );
    case "TimeField":
      return (
        <input
          className="form-control"
          pattern="[0-9]{1,2}:[0-9]{2}"
          defaultValue={value}
          required={required}
          readOnly={readOnly}
          id={slug}
          name={slug}
        />
      );
    case "DateTimeField":
      return (
        <input
          className="form-control"
          type="datetime-local"
          defaultValue={value ? dateTimeToHtml(value) : undefined}
          required={required}
          readOnly={readOnly}
          id={slug}
          name={slug}
        />
      );
    default:
      const exhaustiveCheck: never = type;
      throw new Error(`Unknown field type ${exhaustiveCheck}`);
  }
}

export default SchemaFormInput;
