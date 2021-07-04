import React from "react";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { Field, Layout } from "./models";

const labelColumnWidth = 3;

interface SchemaFormFieldProps {
  layout: Layout;
  field: Field;
  error?: any;
}

/**
 * SchemaFormField is responsible for rendering the chrome around the
 * form input including label, help text and error message.
 */
const SchemaFormField: React.FC<SchemaFormFieldProps> = ({
  layout,
  field,
  children,
  error,
}) => {
  const { name, type, helpText } = field;
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
      // https://react-bootstrap.github.io/components/forms/#forms-form-check
      return (
        <Form.Group controlId={name}>
          <Form.Check type="checkbox">
            {children}
            <Form.Check.Label>{title}</Form.Check.Label>
            {error && (
              <Form.Control.Feedback type="invalid">
                {error}
              </Form.Control.Feedback>
            )}
            {helpText && (
              <Form.Text className="text-muted mb-3">{helpText}</Form.Text>
            )}
          </Form.Check>{" "}
        </Form.Group>
      );
    default:
      switch (layout) {
        case "horizontal":
          return (
            <Form.Group as={Row} controlId={name}>
              <Form.Label column md={labelColumnWidth}>
                {title}
              </Form.Label>
              <Col md={9}>
                {children}
                {error && (
                  <Form.Control.Feedback type="invalid">
                    {error}
                  </Form.Control.Feedback>
                )}
                {helpText && (
                  <Form.Text className="text-muted">{helpText}</Form.Text>
                )}
              </Col>
            </Form.Group>
          );
        case "vertical":
        default:
          return (
            <Form.Group controlId={name}>
              <Form.Label>{title}</Form.Label>
              {children}
              {error && (
                <Form.Control.Feedback type="invalid">
                  {error}
                </Form.Control.Feedback>
              )}
              {helpText && (
                <Form.Text className="text-muted">{helpText}</Form.Text>
              )}
            </Form.Group>
          );
      }
  }
};

export default SchemaFormField;
