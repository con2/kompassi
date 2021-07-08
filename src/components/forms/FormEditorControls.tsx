import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Stack from "react-bootstrap/Stack";

import {
  canEditField,
  canMoveDown,
  canMoveUp,
  moveDown,
  moveUp,
} from "./formEditorLogic";
import { Field, FieldType } from "./models";
import { T } from "../../translations";
import AddFieldDropdown from "./AddFieldDropdown";

import "./FormEditor.scss";

interface FormEditorControlsProps {
  value: Field[];
  field: Field;
  onChange(fields: Field[]): void;
  onAddField(fieldType: FieldType, aboveFieldName: string): void;
  onRemoveField(fieldName: string): void;
  onEditField(fieldName: string): void;
}

const FormEditorControls = ({
  value: fields,
  field,
  onAddField,
  onChange,
  onRemoveField,
  onEditField,
}: FormEditorControlsProps) => {
  const t = T((r) => r.FormEditor);

  return (
    <Stack direction="horizontal" gap={2}>
      <ButtonGroup>
        <AddFieldDropdown
          title={t((r) => r.addFieldAbove) + "…"}
          onSelect={(fieldType) => onAddField(fieldType, field.name)}
        />
      </ButtonGroup>
      <ButtonGroup>
        <Button
          size="sm"
          onClick={() => onChange(moveUp(fields, field.name))}
          variant="outline-secondary"
          disabled={!canMoveUp(fields, field.name)}
        >
          {t((r) => r.moveUp)}
        </Button>
        <Button
          size="sm"
          onClick={() => onChange(moveDown(fields, field.name))}
          variant="outline-secondary"
          disabled={!canMoveDown(fields, field.name)}
        >
          {t((r) => r.moveDown)}
        </Button>
      </ButtonGroup>
      <ButtonGroup>
        <Button
          size="sm"
          onClick={() => onEditField(field.name)}
          disabled={!canEditField(field)}
          variant="outline-secondary"
        >
          {t((r) => r.editField)}…
        </Button>
        <Button
          size="sm"
          onClick={() => onRemoveField(field.name)}
          variant="outline-danger"
        >
          {t((r) => r.removeField)}…
        </Button>
      </ButtonGroup>
    </Stack>
  );
};

export default FormEditorControls;
