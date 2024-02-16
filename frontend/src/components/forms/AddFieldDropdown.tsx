"use client";

import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import { FieldType, fieldTypes } from "./models";
import type { Translations } from "@/translations/en";

interface Props {
  title: string;
  onSelect(fieldType: FieldType): void;
  messages: Translations["FormEditor"];
}

export default function AddFieldDropdown({ title, onSelect, messages }: Props) {
  return (
    <DropdownButton title={title} size="sm" variant="outline-primary">
      {fieldTypes.map((fieldType) => (
        <Dropdown.Item key={fieldType} onClick={() => onSelect(fieldType)}>
          {messages.fieldTypes[fieldType]}
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
}
