import { Temporal } from "@js-temporal/polyfill";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import makeInputId from "./makeInputId";
import type { Choice, Field, SingleSelectPresentation } from "./models";
import { SchemaForm } from "./SchemaForm";
import UploadedFileCards from "./UploadedFileCards";
import { timezone } from "@/config";
import type { Translations } from "@/translations/en";
import { Fragment } from "react";

interface SchemaFormInputProps {
  field: Field;
  idPrefix?: string;
  namePrefix?: string;
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
  messages: t,
  idPrefix = "",
  namePrefix = "",
  readOnly: elementReadOnly = false,
}: SchemaFormInputProps) {
  const { type, required, htmlType, readOnly: fieldReadOnly = false } = field;
  const readOnly = elementReadOnly || fieldReadOnly;
  const id = makeInputId(idPrefix, field);

  let { slug } = field;
  if (namePrefix) {
    slug = `${namePrefix}.${slug}`;
  }

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
          id={id}
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
          id={id}
          name={slug}
        />
      );
    case "NumberField":
    case "DecimalField":
      return (
        <input
          className="form-control"
          type="number"
          defaultValue={Number.isNaN(value) ? "" : value}
          required={required}
          readOnly={readOnly}
          id={id}
          name={slug}
          step={field.decimalPlaces ? 1 / 10 ** field.decimalPlaces : 1}
          inputMode={field.decimalPlaces ? "decimal" : "numeric"}
          min={field.minValue}
          max={field.maxValue}
          key={"" + value}
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
          id={id}
          name={slug}
          key={"" + value}
        />
      );
    case "Tristate":
    case "SingleSelect":
    case "DimensionSingleSelect":
      let choices: Choice[];
      let presentation: SingleSelectPresentation;
      if (field.type === "Tristate") {
        choices = [
          { slug: "true", title: t.boolean.true },
          { slug: "false", title: t.boolean.false },
        ];
        presentation = "dropdown";
      } else {
        choices = field.choices || [];
        presentation = field.presentation || "radio";
      }

      switch (presentation) {
        case "dropdown":
          choices = [{ slug: "", title: "" }, ...choices];

          // FIXME React 19 / Next 15 regression?
          // On AutoSelectForms, when onChange calls requestSubmit, defaultValue={value} does receive the new value
          // but the select still reverts to the original value from when the page was loaded.
          // As a workaround, key={value} forces the select to re-render.
          // It has the side effect of the select losing focus, which is not ideal.
          return (
            <select
              className="form-select"
              required={required}
              disabled={readOnly}
              id={id}
              name={slug}
              defaultValue={value}
              key={value}
            >
              {choices.map((choice) => (
                <option
                  value={choice.slug}
                  key={choice.slug}
                  disabled={choice.disabled}
                >
                  {choice.title}
                </option>
              ))}
            </select>
          );
        case "radio":
        default:
          // radio button group
          return (
            <Fragment key={value}>
              {choices.map((choice) => {
                const choiceId = makeInputId(idPrefix, field, choice);
                return (
                  <div key={choice.slug} className="mb-2">
                    <input
                      className="form-check-input"
                      type="radio"
                      required={required}
                      disabled={readOnly || choice.disabled}
                      id={choiceId}
                      name={slug}
                      value={choice.slug}
                      defaultChecked={choice.slug === value}
                    />{" "}
                    <label htmlFor={choiceId} className="form-check-label">
                      {choice.title}
                    </label>
                  </div>
                );
              })}
            </Fragment>
          );
      }
    case "MultiSelect":
    case "DimensionMultiSelect":
      return (
        <Fragment key={JSON.stringify(value)}>
          {field.choices?.map((choice) => {
            const name = `${field.slug}.${choice.slug}`;
            const choiceId = `${idPrefix}${idPrefix ? "-" : ""}${field.slug}-${
              choice.slug
            }`;
            return (
              <div key={choice.slug} className="mb-2">
                <input
                  className="form-check-input"
                  type="checkbox"
                  defaultChecked={value?.includes(choice.slug)}
                  disabled={readOnly}
                  id={choiceId}
                  name={name}
                />{" "}
                <label htmlFor={choiceId} className="form-check-label">
                  {choice.title}
                </label>
              </div>
            );
          })}
        </Fragment>
      );
    case "RadioMatrix":
      const questions = field.questions ?? [];
      return (
        <table key={JSON.stringify(value)} className="table table-striped">
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
        return <UploadedFileCards urls={value} messages={t} />;
      } else {
        // TODO what if readOnly or value but not both?
        return (
          <input
            className="form-control"
            type="file"
            id={id}
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
          id={id}
          name={slug}
          key={value}
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
          id={id}
          name={slug}
          key={value}
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
          id={id}
          name={slug}
          key={value}
        />
      );
    case "MultiItemField":
      return (
        <Card className="mb-3" key={JSON.stringify(value)}>
          <CardBody>
            <SchemaForm
              fields={field.fields}
              idPrefix={`${id}`}
              namePrefix={slug}
              values={value}
              readOnly={readOnly}
              messages={t}
            />
          </CardBody>
        </Card>
      );
    default:
      const exhaustiveCheck: never = type;
      throw new Error(`Unknown field type ${exhaustiveCheck}`);
  }
}

export default SchemaFormInput;
