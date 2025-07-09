"use client";

import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import ButtonToolbar from "react-bootstrap/ButtonToolbar";
import Stack from "react-bootstrap/Stack";

import { Dimension } from "../dimensions/models";
import ModalButton from "../ModalButton";
import AddFieldDropdown from "./AddFieldDropdown";
import { canMoveDown, canMoveUp, moveDown, moveUp } from "./formEditorLogic";
import { Field, FieldType, fieldTypesConvertibleToDimension } from "./models";
import type { Translations } from "@/translations/en";

import "./FormEditor.scss";

interface FormEditorControlsProps {
  value: Field[];
  field: Field;
  onChange(fields: Field[]): void;
  onAddField(fieldType: FieldType, aboveFieldName: string): void;
  onRemoveField(fieldName: string): void;
  onEditField(fieldName: string): void;
  onPromoteFieldToDimension(fieldName: string): void;
  dimensions?: Dimension[];
  messages: Translations["FormEditor"];
}

const FormEditorControls = ({
  value: fields,
  field,
  onAddField,
  onChange,
  onRemoveField,
  onEditField,
  onPromoteFieldToDimension,
  messages,
  dimensions = [],
}: FormEditorControlsProps) => {
  const converT =
    messages.advancedFieldTypes.SingleSelect.promoteFieldToDimension;
  const canPromoteFieldToDimension =
    !!onPromoteFieldToDimension &&
    fieldTypesConvertibleToDimension.includes(field.type);
  const isNewDimension =
    canPromoteFieldToDimension &&
    dimensions.findIndex((d) => d.slug === field.slug) !== -1;

  return (
    <ButtonToolbar className="mt-1">
      <Stack direction="horizontal" gap={2}>
        <ButtonGroup>
          <AddFieldDropdown
            title={messages.addFieldAbove + "…"}
            onSelect={(fieldType) => onAddField(fieldType, field.slug)}
            messages={messages}
          />
        </ButtonGroup>
        <ButtonGroup>
          <Button
            size="sm"
            onClick={() => onChange(moveUp(fields, field.slug))}
            variant="outline-secondary"
            disabled={!canMoveUp(fields, field.slug)}
          >
            {messages.moveUp}
          </Button>
          <Button
            size="sm"
            onClick={() => onChange(moveDown(fields, field.slug))}
            variant="outline-secondary"
            disabled={!canMoveDown(fields, field.slug)}
          >
            {messages.moveDown}
          </Button>
        </ButtonGroup>
        <ButtonGroup>
          <Button
            size="sm"
            onClick={() => onEditField(field.slug)}
            variant="outline-secondary"
          >
            {messages.editField}…
          </Button>
          <Button
            size="sm"
            onClick={() => onRemoveField(field.slug)}
            variant="outline-danger"
          >
            {messages.removeField}…
          </Button>
        </ButtonGroup>
        {canPromoteFieldToDimension && (
          <ModalButton
            className="btn btn-outline-secondary btn-sm"
            title={`${converT.title}: ${field.slug}`}
            messages={converT.modalActions}
            action={onPromoteFieldToDimension.bind(null, field.slug)}
          >
            {isNewDimension ? converT.newDimension : converT.existingDimension}
          </ModalButton>
        )}
      </Stack>
    </ButtonToolbar>
  );
};

export default FormEditorControls;
