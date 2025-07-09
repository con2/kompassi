"use client";

import React from "react";

import { Dimension } from "../dimensions/models";
import AddFieldDropdown from "./AddFieldDropdown";
import EditFieldModal from "./EditFieldModal";
import FormEditorControls from "./FormEditorControls";
import { addField, removeField, replaceField } from "./formEditorLogic";
import { Modal, useModal } from "./LegacyModal";
import { Field, FieldType, emptyField } from "./models";
import newField from "./newField";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import type { Translations } from "@/translations/en";

import "./FormEditor.scss";

interface Props {
  value: Field[];
  onChange(fields: Field[]): void;
  onPromoteFieldToDimension(fieldSlug: string): Promise<void>;
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
  dimensions: Dimension[];
}

/// The end user facing SchemaForm operates on enriched fields
/// that have the choices already populated for dimension fields.
/// The form editor operates on raw fields and enjoys no such luxury.
function injectChoices(field: Field, dimensions: Dimension[]): Field {
  if (
    // is of a type that can has dimension values as choices
    (field.type === "DimensionSingleSelect" ||
      field.type === "DimensionMultiSelect") &&
    // has a dimension set
    field.dimension &&
    // has no choices pre-populated by the server
    (!field.choices || field.choices.length === 0)
  ) {
    // TODO(#643) subsetValues
    const dimension = dimensions.find((d) => d.slug === field.dimension);
    if (dimension) {
      return {
        ...field,
        choices: dimension.values.map(({ slug, title }) => ({
          slug,
          title: title || slug,
        })),
      };
    }
  }
  return field;
}

/** Fully controlled form editor component. */
export default function FormEditor(props: Props) {
  const {
    value,
    onChange,
    onPromoteFieldToDimension: onPromoteFieldToDimension,
    messages,
    dimensions,
  } = props;
  const t = messages.FormEditor;

  const [targetFieldName, setTargetFieldName] = React.useState("");
  const [editExisting, setEditExisting] = React.useState(false);
  const [fieldBeingEdited, setFieldBeingEdited] = React.useState(emptyField);
  const [editFieldModalOpen, setEditFieldModalOpen] = React.useState(false);

  const removeFieldModal = useModal();

  const fields = value.map((field) => injectChoices(field, dimensions));

  const handleAddField = React.useCallback(
    (fieldType: FieldType, aboveFieldSlug?: string) => {
      const usedIdentifiers = fields.map((field) => field.slug);
      const field = newField(fieldType, usedIdentifiers);

      if (["Divider", "Spacer"].includes(fieldType)) {
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
            <SchemaFormField key={field.slug} field={field}>
              <SchemaFormInput
                field={field}
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
              onPromoteFieldToDimension={onPromoteFieldToDimension}
              messages={messages.FormEditor}
            />
          </div>
        </div>
      ))}
      <AddFieldDropdown
        title={t.addField}
        onSelect={handleAddField}
        messages={messages.FormEditor}
      />

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
          fieldToEdit={fieldBeingEdited}
          onSubmit={(values) => {
            const newFields = editExisting
              ? replaceField(fields, targetFieldName, values)
              : addField(fields, values, targetFieldName);

            setEditFieldModalOpen(false);
            onChange(newFields);
          }}
          onClose={() => setEditFieldModalOpen(false)}
          dimensions={dimensions}
          messages={messages}
        />
      )}
    </div>
  );
}
