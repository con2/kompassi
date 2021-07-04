import React from "react";
import Form from "react-bootstrap/Form";

import { Field } from "./models";

interface SchemaFormInputProps {
  field: Field;
  value: any;
  readOnly?: boolean;
  error?: any;
  onChange(e: React.ChangeEvent<any>): void;
}

/** SchemaFormInput is responsible for rendering the actual input component. */
const SchemaFormInput = ({
  field,
  value,
  onChange,
  error,
  readOnly,
}: SchemaFormInputProps) => {
  switch (field.type) {
    case "SingleLineText":
      return (
        <Form.Control
          type="text"
          value={value}
          onChange={onChange}
          required={field.required}
          isInvalid={!!error}
          readOnly={readOnly}
        />
      );
    case "MultiLineText":
      return (
        <Form.Control
          as="textarea"
          value={value}
          onChange={onChange}
          required={field.required}
          isInvalid={!!error}
          readOnly={readOnly}
        />
      );
    case "SingleCheckbox":
      // FIXME: Required checkboxes fail in a funny way.
      return (
        <Form.Check.Input
          type="checkbox"
          value={value}
          onChange={onChange}
          isInvalid={!!error}
          required={field.required}
          disabled={readOnly}
        />
      );
    default:
      throw new Error(`field.type not implemented: ${field.type}`);
  }
};

export default SchemaFormInput;
