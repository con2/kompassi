import React from "react";

import {
  Field,
  FieldType,
  FormSchema,
  emptyField,
  nonValueFieldTypes,
} from "./models";
import { T } from "../../translations";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import FormEditorControls from "./FormEditorControls";
import AddFieldDropdown from "./AddFieldDropdown";

import "./FormEditor.scss";
import { addField, removeField, replaceField } from "./formEditorLogic";
import { Modal, useModal } from "../common/Modal";
import SchemaForm from "./SchemaForm";
import { fieldEditorMapping } from "./editFieldForm";
import generateUniqueIdentifier from "../../utils/generateUniqueIdentifier";

interface FormEditorProps {
  value: FormSchema;
  onChange(value: FormSchema): void;
}

/** Fully controlled form editor component. */
const FormEditor = ({ value: schema, onChange }: FormEditorProps) => {
  const noop = React.useCallback(() => {}, []);
  const { layout } = schema;
  const t = T((r) => r.FormEditor);

  const [targetFieldName, setTargetFieldName] = React.useState("");
  const [editExisting, setEditExisting] = React.useState(false);
  const [fieldBeingEdited, setFieldBeingEdited] = React.useState(emptyField);
  const editFieldModal = useModal();
  const removeFieldModal = useModal();

  /** Handles trivial changes (move up, down) that require no further user interaction. */
  const handleChangeFields = React.useCallback(
    (fields: Field[]) => onChange({ ...schema, fields }),
    [schema]
  );

  const handleAddField = React.useCallback(
    (fieldType: FieldType, aboveFieldName?: string) => {
      const newField = {
        type: fieldType,
        name: generateUniqueIdentifier(
          fieldType,
          schema.fields.map((field) => field.name)
        ),
      };

      if (nonValueFieldTypes.includes(fieldType)) {
        // This field type has no options to be edited by the user,
        // so skip the edit dialog.
        onChange({
          ...schema,
          fields: addField(schema.fields, newField, aboveFieldName),
        });
      } else {
        setEditExisting(false);
        setTargetFieldName(aboveFieldName ?? "");
        setFieldBeingEdited(newField);
        editFieldModal.open();
      }
    },
    [schema, editFieldModal]
  );

  const handleEditField = React.useCallback(
    (fieldName: string) => {
      const fieldToEdit = schema.fields.find(
        (field) => field.name === fieldName
      );

      if (!fieldToEdit) {
        throw new Error(
          "Asked to edit non-existent field (this shouldn't happen)"
        );
      }

      setEditExisting(true);
      setTargetFieldName(fieldName);
      setFieldBeingEdited(fieldToEdit);
      editFieldModal.open();
    },
    [schema, editFieldModal]
  );

  const onEditDialogClose = React.useCallback(
    (ok: boolean) => {
      if (!ok) {
        return;
      }

      const fields = editExisting
        ? replaceField(schema.fields, targetFieldName, fieldBeingEdited)
        : addField(schema.fields, fieldBeingEdited, targetFieldName);

      onChange({ ...schema, fields });
    },
    [onChange, schema, editExisting, targetFieldName, fieldBeingEdited]
  );

  const handleRemoveField = React.useCallback(
    (fieldName: string) => {
      setTargetFieldName(fieldName);
      removeFieldModal.open();
    },
    [removeFieldModal]
  );

  const onRemoveFieldDialogClose = React.useCallback(
    (ok: boolean) => {
      if (ok) {
        onChange({
          ...schema,
          fields: removeField(schema.fields, targetFieldName),
        });
      }
    },
    [onChange, schema, targetFieldName]
  );

  return (
    <div className="FormEditor">
      {schema.fields.map((field) => (
        <div key={field.name} className="FormEditor-field">
          <div className="FormEditor-background">
            <SchemaFormField
              layout={layout}
              key={field.name}
              field={field}
              error={null}
            >
              <SchemaFormInput
                field={field}
                value={""}
                onChange={noop}
                error={null}
                readOnly={true}
              />
            </SchemaFormField>
            <FormEditorControls
              schema={schema}
              field={field}
              onChangeFields={handleChangeFields}
              onAddField={handleAddField}
              onRemoveField={handleRemoveField}
              onEditField={handleEditField}
            />
          </div>
        </div>
      ))}
      <AddFieldDropdown
        title={t((r) => r.addField)}
        onSelect={handleAddField}
      />

      <Modal
        {...removeFieldModal}
        title={t((r) => r.RemoveFieldModal.title)}
        okLabel={t((r) => r.RemoveFieldModal.yes)}
        cancelLabel={t((r) => r.RemoveFieldModal.no)}
        onClose={onRemoveFieldDialogClose}
      >
        {t((r) => r.RemoveFieldModal.message)}
      </Modal>

      <Modal
        {...editFieldModal}
        title={t((r) => r.editField)}
        onClose={onEditDialogClose}
      >
        <SchemaForm
          fields={fieldEditorMapping[fieldBeingEdited.type]}
          initialValues={fieldBeingEdited}
          onSubmit={(values) => console.log(values)}
        />
      </Modal>
    </div>
  );
};

export default FormEditor;
