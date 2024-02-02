"use client";

import "./FormEditor.scss";
import getFieldEditorFields from "./getFieldEditorFields";
import { Modal, useModal } from "./LegacyModal";
import { Field } from "./models";
import { SchemaForm } from "./SchemaForm";
import type { Translations } from "@/translations/en";

interface EditFieldModalProps {
  initialValues: Field;
  onSubmit(field: Field): void;
  onClose(): void;
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
}

const EditFieldModal = ({
  initialValues,
  onSubmit,
  onClose,
  messages,
}: EditFieldModalProps) => {
  const t = messages.FormEditor;
  const fields = getFieldEditorFields(initialValues.type, messages.FormEditor);
  const modal = useModal({ isOpen: true });

  return (
    <Modal
      {...modal}
      title={t.editField}
      onClose={onClose}
      messages={t.editFieldModal.actions}
    >
      <SchemaForm fields={fields} messages={messages.SchemaForm} readOnly />
    </Modal>
  );
};

export default EditFieldModal;
