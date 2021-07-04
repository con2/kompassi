import React from "react";

import { useFormik } from "formik";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";

import { Field, Layout } from "./models";
import { fieldsToYup } from "./validation";
import SchemaFormInput from "./SchemaFormInput";
import SchemaFormField from "./SchemaFormField";

interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
  initialValues?: any;
  showSubmitButton?: boolean; // default true
  onSubmit(values: any): void;
}

const SchemaForm = (props: SchemaFormProps) => {
  const { fields, onSubmit, showSubmitButton } = props;
  const initialValues = props.initialValues ?? {};
  const layout = props.layout ?? "vertical";

  const validationSchema = React.useMemo(() => fieldsToYup(fields), [fields]);
  const { handleSubmit, handleChange, values, errors, isSubmitting } =
    useFormik({
      initialValues,
      onSubmit,
      validationSchema,
    });

  return (
    <Form noValidate onSubmit={handleSubmit}>
      {fields.map((field) => (
        <SchemaFormField
          layout={layout}
          key={field.name}
          field={field}
          error={errors[field.name]}
        >
          <SchemaFormInput
            field={field}
            value={values[field.name] || ""}
            onChange={handleChange}
            error={errors[field.name]}
          />
        </SchemaFormField>
      ))}
      <Button
        type="submit"
        disabled={isSubmitting}
        className={showSubmitButton ?? true ? "" : "sr-only"}
      >
        {(isSubmitting && (
          <>
            <Spinner animation="border" size="sm" /> Submitting...
          </>
        )) ||
          "Submit"}
      </Button>
    </Form>
  );
};
export default SchemaForm;
