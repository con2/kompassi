"use client";

import React from "react";

import AddFieldDropdown from "./AddFieldDropdown";
import EditFieldModal from "./EditFieldModal";
import FormEditorControls from "./FormEditorControls";
import { addField, removeField, replaceField } from "./formEditorLogic";
import { Modal, useModal } from "./LegacyModal";
import { Field, FieldType, emptyField } from "./models";
import newField from "./newField";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
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
  dimensions: DimensionValueSelectFragment[];
}

/// The end user facing SchemaForm operates on enriched fields
/// that have the choices already populated for dimension fields.
/// The form editor operates on raw fields and enjoys no such luxury.
function injectChoices(
  field: Field,
  dimensions: DimensionValueSelectFragment[],
): Field {
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

/// Inverse of injectChoices. Dimension fields' choices are only ever populated for display
/// in the editor (see injectChoices above) or by server side enrichment (for the responder
/// facing SchemaForm). They must never be persisted, or they will freeze stale values and
/// translations in place until the field is next edited.
function stripInjectedChoices(field: Field): Field {
  if (
    (field.type === "DimensionSingleSelect" ||
      field.type === "DimensionMultiSelect") &&
    field.dimension
  ) {
    return { ...field, choices: [] };
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

  const handleChange = React.useCallback(
    (newFields: Field[]) => onChange(newFields.map(stripInjectedChoices)),
    [onChange],
  );

  const handleAddField = React.useCallback(
    (fieldType: FieldType, aboveFieldSlug?: string) => {
      const usedIdentifiers = fields.map((field) => field.slug);
      const field = newField(fieldType, usedIdentifiers);

      if (["Divider", "Spacer"].includes(fieldType)) {
        // This field type has no options to be edited by the user,
        // so skip the edit dialog.
        handleChange(addField(fields, field, aboveFieldSlug));
      } else {
        setEditExisting(false);
        setTargetFieldName(aboveFieldSlug ?? "");
        setFieldBeingEdited(field);
        setEditFieldModalOpen(true);
      }
    },
    [fields, handleChange],
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
              onChange={handleChange}
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
        onSubmit={() => handleChange(removeField(fields, targetFieldName))}
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
            handleChange(newFields);
          }}
          onClose={() => setEditFieldModalOpen(false)}
          dimensions={dimensions}
          messages={messages}
        />
      )}
    </div>
  );
}
