import ButtonGroup from "react-bootstrap/ButtonGroup";
import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import { FieldType, fieldTypes } from "./models";
import { T } from "../../translations";

interface AddFieldDropdownProps {
  title: string;
  onSelect(fieldType: FieldType): void;
}

const AddFieldDropdown = ({ title, onSelect }: AddFieldDropdownProps) => {
  const t = T((r) => r.FormEditor);
  return (
    <DropdownButton title={title} size="sm" variant="outline-primary">
      {fieldTypes.map((fieldType) => (
        <Dropdown.Item key={fieldType} onClick={() => onSelect(fieldType)}>
          {t((r) => r.FieldTypes[fieldType])}
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
};

export default AddFieldDropdown;
