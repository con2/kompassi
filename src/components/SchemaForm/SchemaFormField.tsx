import { ReactNode } from "react";

import { Field, Layout } from "./models";

function Label({ field, layout }: { field: Field; layout: Layout }) {
  const { type, title, required, name } = field;
  const classNames =
    type === "SingleCheckbox" ? ["form-check-label"] : ["form-label"];

  if (layout === "horizontal" && type !== "SingleCheckbox") {
    classNames.push("col-md-3");
  }

  if (required) {
    classNames.push("fw-bold");
  }

  return (
    <label className={classNames.join(" ")} htmlFor={name}>
      {title}
      {required && "*"}
    </label>
  );
}

interface SchemaFormFieldProps {
  layout: Layout;
  field: Field;
  children: ReactNode;
}

/**
 * SchemaFormField is responsible for rendering the chrome around the
 * form input including label, help text and error message.
 */
export default function SchemaFormField({
  layout,
  field,
  children,
}: SchemaFormFieldProps) {
  const { type, helpText } = field;
  const title = field.required ? `${field.title}*` : field.title;

  if (type === "StaticText" && !title) {
    // Full-width static text
    return <p>{helpText}</p>;
  } else if (type === "Divider") {
    return <hr />;
  } else if (type === "Spacer") {
    return <div className="pb-3" />;
  }

  switch (type) {
    case "SingleCheckbox":
      switch (layout) {
        case "horizontal":
          return (
            <div className="row mb-3">
              <div className="col-md-3" />
              <div className="col-md-9">
                <div className="form-check">
                  {children}
                  <Label field={field} layout={layout} />
                  {helpText && (
                    <div className="form-text text-muted">{helpText}</div>
                  )}
                </div>
              </div>
            </div>
          );
        default:
          return (
            <div className="form-check mb-3">
              {children}
              <Label field={field} layout={layout} />
              {helpText && (
                <div className="form-text text-muted">{helpText}</div>
              )}
            </div>
          );
      }

    default:
      switch (layout) {
        case "horizontal":
          return (
            <div className="row mb-3">
              <Label field={field} layout={layout} />
              <div className="col-md-9">
                {children}
                {helpText && (
                  <div className="form-text text-muted">{helpText}</div>
                )}
              </div>
            </div>
          );
        case "vertical":
        default:
          return (
            <div className="mb-3">
              <Label field={field} layout={layout} />
              {children}
              {helpText && (
                <div className="form-text text-muted">{helpText}</div>
              )}
            </div>
          );
      }
  }
}
