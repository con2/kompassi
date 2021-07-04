import React from "react";

import {
  FieldType,
  FormSchema,
  emptyField,
  nonValueFieldTypes,
} from "./models";
import { addField, removeField, replaceField } from "./formEditorLogic";
import { Modal, useModal } from "../common/Modal";
import { T } from "../../translations";
import AddFieldDropdown from "./AddFieldDropdown";
import EditFieldModal from "./EditFieldModal";
import FormEditorControls from "./FormEditorControls";
import generateUniqueIdentifier from "../../utils/generateUniqueIdentifier";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";

import "./FormEditor.scss";

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
  const [editFieldModalOpen, setEditFieldModalOpen] = React.useState(false);

  const removeFieldModal = useModal();

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
        setEditFieldModalOpen(true);
      }
    },
    [schema]
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
      setEditFieldModalOpen(true);
    },
    [schema]
  );

  const handleRemoveField = React.useCallback(
    (fieldName: string) => {
      setTargetFieldName(fieldName);
      removeFieldModal.open();
    },
    [removeFieldModal]
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
              onChangeFields={(fields) => onChange({ ...schema, fields })}
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
        onSubmit={() =>
          onChange({
            ...schema,
            fields: removeField(schema.fields, targetFieldName),
          })
        }
      >
        {t((r) => r.RemoveFieldModal.message)}
      </Modal>

      {editFieldModalOpen && (
        <EditFieldModal
          initialValues={fieldBeingEdited}
          onSubmit={(values) => {
            const fields = editExisting
              ? replaceField(schema.fields, targetFieldName, values)
              : addField(schema.fields, values, targetFieldName);

            onChange({ ...schema, fields });
          }}
          onClose={() => {
            console.log("onClose");
            setEditFieldModalOpen(false);
          }}
        />
      )}
    </div>
  );
};

export default FormEditor;
