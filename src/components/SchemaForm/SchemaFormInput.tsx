import { Field } from "./models";

interface SchemaFormInputProps {
  field: Field;
  value: any;
  readOnly?: boolean;
}

const defaultRows = 8;

/** SchemaFormInput is responsible for rendering the actual input component. */
const SchemaFormInput = ({ field, value, readOnly }: SchemaFormInputProps) => {
  const { slug, type, required, htmlType } = field;
  // TODO: make id unique in a deterministic fashion
  switch (type) {
    case "Spacer":
    case "Divider":
    case "StaticText":
      return null;
    case "RadioMatrix":
      // TODO
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
    case "SingleCheckbox":
      // FIXME: Required checkboxes fail in a funny way.
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
      const choices = field.choices ?? [];
      choices.unshift({ slug: "", title: "" });

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
    case "MultiSelect":
      return (
        <>
          {field.choices?.map((choice) => (
            <div key={choice.slug} className="mb-2">
              <input
                className="form-check-input"
                type="checkbox"
                // defaultChecked={!!value}
                disabled={readOnly}
                // FIXME
                id={choice.slug}
                name={choice.slug}
              />{" "}
              <label htmlFor={choice.slug} className="form-check-label">
                {choice.title}
              </label>
            </div>
          ))}
        </>
      );
    // default:
    //   throw new Error(`field.type not implemented: ${field.type}`);
  }
};

export default SchemaFormInput;
