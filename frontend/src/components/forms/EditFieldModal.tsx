"use client";

import { useCallback, useMemo } from "react";
import Modal from "react-bootstrap/Modal";
import {
  fieldToValues,
  formDataToField,
  getFieldEditorFields,
} from "./editFieldForm";
import "./FormEditor.scss";
import { Field } from "./models";
import { SchemaForm } from "./SchemaForm";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

interface EditFieldModalProps {
  fieldToEdit: Field;
  onSubmit(field: Field): void;
  onClose(): void;
  dimensions: DimensionValueSelectFragment[];
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
}: EditFieldModalProps) => {
  const t = messages.FormEditor.editFieldModal;
  const fields = getFieldEditorFields(
    fieldToEdit.type,
    messages.FormEditor.editFieldForm,
    dimensions,
  );

  const handleSubmit = useCallback(
    (event: React.SyntheticEvent) => {
      event.preventDefault();
      const formData = new FormData(event.target as HTMLFormElement);
      const field = formDataToField(fields, fieldToEdit, formData);
      onSubmit(field);
    },
    [fieldToEdit, fields, onSubmit],
  );
  const values = useMemo(() => fieldToValues(fieldToEdit), [fieldToEdit]);

  return (
    <Modal show={true} onHide={onClose}>
      <Modal.Header closeButton>
        <Modal.Title>
          {t.title}: {messages.FormEditor.fieldTypes[fieldToEdit.type]}
        </Modal.Title>
      </Modal.Header>
      <form onSubmit={handleSubmit}>
        <Modal.Body>
          <SchemaForm
            fields={fields}
            values={values}
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
