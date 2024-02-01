import { Field } from "./models";
import { T } from "../../translations";

import "./FormEditor.scss";
import { Modal, useModal } from "../common/Modal";
import SchemaForm, { useSchemaForm } from "./SchemaForm";
import { fieldEditorMapping } from "./editFieldForm";

interface EditFieldModalProps {
  initialValues: Field;
  onSubmit(field: Field): void;
  onClose(): void;
}

const EditFieldModal = ({
  initialValues,
  onSubmit,
  onClose,
}: EditFieldModalProps) => {
  const form = useSchemaForm(
    {
      fields: fieldEditorMapping[initialValues.type],
      showSubmitButton: false,
    },
    {
      initialValues,
      onSubmit(values) {
        onSubmit(values);
        modal.close();
      },
    }
  );

  const modal = useModal({ isOpen: true });
  const t = T((r) => r.FormEditor);

  return (
    <Modal
      {...modal}
      title={t((r) => r.editField)}
      onSubmit={() => {
        form.formik.submitForm();
        return false;
      }}
      onClose={onClose}
    >
      <SchemaForm {...form} />
    </Modal>
  );
};

export default EditFieldModal;
