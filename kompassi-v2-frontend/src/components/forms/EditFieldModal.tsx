"use client";

import { useCallback, useMemo, useState } from "react";
import Modal from "react-bootstrap/Modal";
import {
  encodeDimensionChoice,
  fieldToValues,
  findEditorDimensionByChoice,
  formDataToField,
  getFieldEditorFields,
  type AnnotationOption,
  type EditorDimension,
  type FormEditorContext,
} from "./editFieldForm";
import "./FormEditor.scss";
import { DimensionUniverse, Field } from "./models";
import { SchemaForm } from "./SchemaForm";
import type { Translations } from "@/translations/en";

interface EditFieldModalProps {
  fieldToEdit: Field;
  onSubmit(field: Field): void;
  onClose(): void;
  dimensions: EditorDimension[];
  defaultDimensionUniverse?: DimensionUniverse;
  annotations: AnnotationOption[];
  formContext: FormEditorContext;
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
}

const EditFieldModal = ({
  fieldToEdit,
  onSubmit,
  onClose,
  messages,
  dimensions,
  defaultDimensionUniverse,
  annotations,
  formContext,
}: EditFieldModalProps) => {
  const t = messages.FormEditor.editFieldModal;
  const values = useMemo(
    () => fieldToValues(fieldToEdit, defaultDimensionUniverse),
    [fieldToEdit, defaultDimensionUniverse],
  );

  // The value checkboxes follow the dimension dropdown, so its value must be known while editing.
  // A new field has no dimension yet, and the required dropdown then shows its first choice.
  const [dimensionChoice, setDimensionChoice] = useState<string>(
    () =>
      values.dimension ??
      (dimensions.length ? encodeDimensionChoice(dimensions[0]) : ""),
  );
  const handleChange = useCallback((event: React.FormEvent) => {
    const target = event.target as HTMLInputElement;
    if (target.name === "dimension") {
      setDimensionChoice(target.value);
    }
  }, []);

  // The subset saved for the field's own dimension means nothing for another dimension.
  const formValues = useMemo(
    () =>
      dimensionChoice === values.dimension
        ? values
        : { ...values, subsetValues: undefined },
    [values, dimensionChoice],
  );

  const fields = useMemo(
    () =>
      getFieldEditorFields(
        fieldToEdit.type,
        messages.FormEditor.editFieldForm,
        dimensions,
        annotations,
        formContext,
        findEditorDimensionByChoice(dimensions, dimensionChoice),
      ),
    [
      fieldToEdit.type,
      messages.FormEditor.editFieldForm,
      dimensions,
      annotations,
      formContext,
      dimensionChoice,
    ],
  );

  const handleSubmit = useCallback(
    (event: React.SyntheticEvent) => {
      event.preventDefault();
      const formData = new FormData(event.target as HTMLFormElement);
      const field = formDataToField(
        fields,
        fieldToEdit,
        formData,
        defaultDimensionUniverse,
      );
      onSubmit(field);
    },
    [fieldToEdit, fields, onSubmit, defaultDimensionUniverse],
  );

  return (
    <Modal show={true} onHide={onClose} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>
          {t.title}: {messages.FormEditor.fieldTypes[fieldToEdit.type]}
        </Modal.Title>
      </Modal.Header>
      <form onSubmit={handleSubmit} onChange={handleChange}>
        <Modal.Body>
          <SchemaForm
            fields={fields}
            values={formValues}
            messages={messages.SchemaForm}
          />
        </Modal.Body>
        <Modal.Footer>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            {t.actions.cancel}
          </button>
          <button type="submit" className="btn btn-primary">
            {t.actions.submit}
          </button>
        </Modal.Footer>
      </form>
    </Modal>
  );
};

export default EditFieldModal;
