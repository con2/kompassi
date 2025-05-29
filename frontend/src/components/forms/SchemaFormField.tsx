import { ReactNode } from "react";

import { Heading, HeadingLevel } from "../helpers/Heading";
import ParagraphsDangerousHtml from "../helpers/ParagraphsDangerousHtml";
import { Field, Layout, defaultLayout } from "./models";

function Label({ field, layout }: { field: Field; layout: Layout }) {
  const { type, title, required, slug } = field;
  const classNames =
    type === "SingleCheckbox"
      ? ["form-check-label"]
      : ["form-label", "fw-bold"];

  if (
    layout === "horizontal" &&
    !["SingleCheckbox", "DimensionSingleCheckbox"].includes(type)
  ) {
    classNames.push("col-md-3");
  }

  return (
    <label className={classNames.join(" ")} htmlFor={slug}>
      {title}
      {required && "*"}
    </label>
  );
}

interface SchemaFormFieldProps {
  layout?: Layout;
  field: Field;
  children?: ReactNode;

  /// used for StaticText.title
  headingLevel?: HeadingLevel;
}

/**
 * SchemaFormField is responsible for rendering the chrome around the
 * form input including label, help text and error message.
 */
export default function SchemaFormField({
  layout = defaultLayout,
  field,
  children,
  headingLevel,
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
      switch (layout) {
        case "horizontal":
          return (
            <div className="row mb-4">
              <div className="col-md-3">{title}</div>
              <div className="col-md-9">
                <div className="form-check">
                  {children}
                  <Label field={field} layout={layout} />
                  {helpText && <div className="form-text">{helpText}</div>}
                </div>
              </div>
            </div>
          );
        default:
          return (
            <div className="form-check mb-4">
              {children}
              <Label field={field} layout={layout} />
              {helpText && <div className="form-text">{helpText}</div>}
            </div>
          );
      }

    default:
      switch (layout) {
        case "horizontal":
          return (
            <div className="row mb-4">
              <Label field={field} layout={layout} />
              <div className="col-md-9">
                {children}
                {helpText && <div className="form-text">{helpText}</div>}
              </div>
            </div>
          );
        default:
          return (
            <div className="mb-4">
              <Label field={field} layout={layout} />
              {children}
              {helpText && <div className="form-text">{helpText}</div>}
            </div>
          );
      }
  }
}
