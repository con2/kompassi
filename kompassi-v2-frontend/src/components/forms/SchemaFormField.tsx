import { Markdown } from "@con2/components";
import { makeInputId } from "@con2/components/helpers";
import { ReactNode } from "react";

import { Heading, HeadingLevel } from "./Heading";
import { Field } from "./models";

function Label({
  field,
  idPrefix,
  children,
  className = "form-label fw-bold",
}: {
  field: Field;
  idPrefix: string;
  children: ReactNode;
  className?: string;
}) {
  const { type } = field;
  const inputId = makeInputId(idPrefix, field);
  className = type === "SingleCheckbox" ? "form-check-label" : className;

  return (
    <label className={className} htmlFor={inputId}>
      {children}
    </label>
  );
}

interface Props {
  field: Field;
  children?: ReactNode;
  idPrefix?: string;
  highlightReadOnlyFields?: boolean;
  /// used for StaticText.title
  headingLevel?: HeadingLevel;
  fieldMargin?: string;
  labelClassName?: string;
}

/**
 * SchemaFormField is responsible for rendering the chrome around the
 * form input including label, help text and error message.
 */
export default function SchemaFormField({
  field,
  children,
  headingLevel,
  highlightReadOnlyFields = false,
  fieldMargin = "mb-4",
  labelClassName = "form-label fw-bold",
  idPrefix = "",
}: Props) {
  const { type } = field;
  let title = <>{field.title}</>;
  if (highlightReadOnlyFields && field.readOnly) {
    title = <>{title} 🔒</>;
  } else if (field.required) {
    title = <>{title}*</>;
  }

  const helpText =
    typeof field.helpText === "string" ? (
      <Markdown input={field.helpText} />
    ) : (
      field.helpText
    );

  if (type === "StaticText") {
    return (
      <>
        {title && <Heading level={headingLevel}>{title}</Heading>}
        {helpText}
        {children}
      </>
    );
  } else if (type === "Divider") {
    return <hr />;
  } else if (type === "Spacer") {
    return <div className="pb-3" />;
  }

  switch (type) {
    case "SingleCheckbox":
    case "DimensionSingleCheckbox":
      return (
        <div className={`form-check ${fieldMargin}`}>
          {children}
          <Label field={field} idPrefix={idPrefix} className={labelClassName}>
            {title}
          </Label>
          {helpText && <div className="form-text">{helpText}</div>}
        </div>
      );

    default:
      return (
        <div className={fieldMargin}>
          <Label field={field} idPrefix={idPrefix} className={labelClassName}>
            {title}
          </Label>
          {children}
          {helpText && <div className="form-text">{helpText}</div>}
        </div>
      );
  }
}
