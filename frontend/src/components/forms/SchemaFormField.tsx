import { ReactNode } from "react";

import { Heading, HeadingLevel } from "../helpers/Heading";
import ParagraphsDangerousHtml from "../helpers/ParagraphsDangerousHtml";
import makeInputId from "./makeInputId";
import { Field } from "./models";

function Label({ field, idPrefix }: { field: Field; idPrefix: string }) {
  const { type, title, required, slug } = field;
  const inputId = makeInputId(idPrefix, field);
  const className =
    type === "SingleCheckbox" ? "form-check-label" : "form-label fw-bold";

  return (
    <label className={className} htmlFor={inputId}>
      {title}
      {required && "*"}
    </label>
  );
}

interface SchemaFormFieldProps {
  field: Field;
  children?: ReactNode;
  idPrefix?: string;

  /// used for StaticText.title
  headingLevel?: HeadingLevel;
}

/**
 * SchemaFormField is responsible for rendering the chrome around the
 * form input including label, help text and error message.
 */
export default function SchemaFormField({
  field,
  children,
  headingLevel,
  idPrefix = "",
}: SchemaFormFieldProps) {
  const { type } = field;
  const title = field.required ? `${field.title}*` : field.title;

  // FIXME(SECURITY): cannot ParagraphsDangerousHtml user content like this, use Markdown or something
  const helpText =
    typeof field.helpText === "string" ? (
      <ParagraphsDangerousHtml html={field.helpText} />
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
        <div className="form-check mb-4">
          {children}
          <Label field={field} idPrefix={idPrefix} />
          {helpText && <div className="form-text">{helpText}</div>}
        </div>
      );

    default:
      return (
        <div className="mb-4">
          <Label field={field} idPrefix={idPrefix} />
          {children}
          {helpText && <div className="form-text">{helpText}</div>}
        </div>
      );
  }
}
