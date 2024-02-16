"use client";

import React from "react";

import EditFieldModal from "./EditFieldModal";
import FormEditorControls from "./FormEditorControls";
import { addField, removeField, replaceField } from "./formEditorLogic";
import { Modal, useModal } from "./LegacyModal";
import {
  FieldType,
  emptyField,
  nonValueFieldTypes,
  Field,
  Layout,
  defaultLayout,
} from "./models";
import newField from "./newField";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import type { Translations } from "@/translations/en";

import "./FormEditor.scss";

interface FormEditorProps {
  value: Field[];
  layout?: Layout;
  onChange(fields: Field[]): void;
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
}

/** Fully controlled form editor component. */
export default function FormEditor(props: FormEditorProps) {
  const { value: fields, onChange, messages } = props;
  const t = messages.FormEditor;
  const layout = props.layout ?? defaultLayout;

  const [targetFieldName, setTargetFieldName] = React.useState("");
  const [editExisting, setEditExisting] = React.useState(false);
  const [fieldBeingEdited, setFieldBeingEdited] = React.useState(emptyField);
  const [editFieldModalOpen, setEditFieldModalOpen] = React.useState(false);

  const removeFieldModal = useModal();

  const handleAddField = React.useCallback(
    (fieldType: FieldType, aboveFieldSlug?: string) => {
      const usedIdentifiers = fields.map((field) => field.slug);
      const field = newField(fieldType, usedIdentifiers);

      if (nonValueFieldTypes.includes(fieldType)) {
        // This field type has no options to be edited by the user,
        // so skip the edit dialog.
        onChange(addField(fields, field, aboveFieldSlug));
      } else {
        setEditExisting(false);
        setTargetFieldName(aboveFieldSlug ?? "");
        setFieldBeingEdited(field);
        setEditFieldModalOpen(true);
      }
    },
    [fields, onChange],
  );

  const handleEditField = React.useCallback(
    (slug: string) => {
      const fieldToEdit = fields.find((field) => field.slug === slug);

      if (!fieldToEdit) {
        throw new Error(
          "Asked to edit non-existent field (this shouldn't happen)",
        );
      }

      setEditExisting(true);
      setTargetFieldName(slug);
      setFieldBeingEdited(fieldToEdit);
      setEditFieldModalOpen(true);
    },
    [fields],
  );

  const handleRemoveField = React.useCallback(
    (slug: string) => {
      setTargetFieldName(slug);
      removeFieldModal.open();
    },
    [removeFieldModal],
  );

  return (
    <div className="FormEditor">
      {fields.map((field) => (
        <div key={field.slug} className="FormEditor-field">
          <div className="FormEditor-background">
            <SchemaFormField layout={layout} key={field.slug} field={field}>
              <SchemaFormInput
                field={field}
                value={""}
                readOnly={true}
                messages={messages.SchemaForm}
              />
            </SchemaFormField>
            <FormEditorControls
              value={fields}
              field={field}
              onChange={onChange}
              onAddField={handleAddField}
              onRemoveField={handleRemoveField}
              onEditField={handleEditField}
              messages={messages.FormEditor}
            />
          </div>
        </div>
      ))}
      {/* <AddFieldDropdown title={t.addField} onSelect={handleAddField} /> */}

      <Modal
        {...removeFieldModal}
        title={t.removeFieldModal.title}
        messages={t.removeFieldModal.actions}
        onSubmit={() => onChange(removeField(fields, targetFieldName))}
      >
        {t.removeFieldModal.message}
      </Modal>

      {editFieldModalOpen && (
        <EditFieldModal
          initialValues={fieldBeingEdited}
          onSubmit={(values) => {
            const newFields = editExisting
              ? replaceField(fields, targetFieldName, values)
              : addField(fields, values, targetFieldName);

            onChange(newFields);
          }}
          onClose={() => setEditFieldModalOpen(false)}
          messages={messages}
        />
      )}
    </div>
  );
}
