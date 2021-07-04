import React from "react";

import { Field, FieldType, FormSchema } from "./models";
import { T } from "../../translations";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import FormEditorControls from "./FormEditorControls";
import AddFieldDropdown from "./AddFieldDropdown";

import "./FormEditor.scss";
import { removeField } from "./formEditorLogic";
import { Modal, useModal } from "../common/Modal";

interface FormEditorProps {
  value: FormSchema;
  onChange(value: FormSchema): void;
}

/** Fully controlled form editor component. */
const FormEditor = ({ value: schema, onChange }: FormEditorProps) => {
  const noop = React.useCallback(() => {}, []);
  const { layout } = schema;
  const removeFieldModal = useModal();
  const t = T((r) => r.FormEditor);

  const handleChangeFields = React.useCallback(
    (fields: Field[]) => onChange({ ...schema, fields }),
    [schema]
  );
  const handleAddField = React.useCallback(
    (fieldType: FieldType) => {},
    [schema]
  );
  const handleRemoveField = React.useCallback(
    async (fieldName: string) => {
      const okToRemove = await removeFieldModal.execute();
      if (okToRemove) {
        onChange({ ...schema, fields: removeField(schema.fields, fieldName) });
      }
    },
    [schema, removeFieldModal]
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
            />
          </div>
        </div>
      ))}
      <AddFieldDropdown
        title={t((r) => r.addField)}
        onSelect={handleAddField}
      />

      <Modal {...removeFieldModal} title={t((r) => r.RemoveFieldModal.title)}>
        {t((r) => r.RemoveFieldModal.message)}
      </Modal>
    </div>
  );
};

export default FormEditor;
