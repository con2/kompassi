"use client";

import { useCallback, useState } from "react";
import FormEditor from "./FormEditor";
import { Field } from "./models";
import type { Translations } from "@/translations/en";

interface Props {
  initialFields: Field[];
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
  onChange(newFields: Field[]): Promise<void>;
}

/// Wraps FormEditor with a client component that holds the state and handles calling the server action.
export default function FormEditorWrapper({
  initialFields,
  messages,
  onChange,
}: Props) {
  const [fields, setFields] = useState(initialFields);

  const handleChange = useCallback(
    (newFields: Field[]) => {
      setFields(newFields);
      // TODO feedback of success/error
      onChange(newFields);
    },
    [onChange],
  );

  return (
    <FormEditor value={fields} onChange={handleChange} messages={messages} />
  );
}
