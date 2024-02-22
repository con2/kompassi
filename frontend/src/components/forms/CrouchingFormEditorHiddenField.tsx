"use client";

import { useState } from "react";
import FormEditor from "./FormEditor";
import { Field } from "./models";
import type { Translations } from "@/translations/en";

interface Props {
  initialFields: Field[];
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
}

/// Wraps FormEditor with a client component that provides the result as a hidden field.
export default function CrouchingFormEditorHiddenField({
  initialFields,
  messages,
}: Props) {
  const [fields, setFields] = useState(initialFields);

  return (
    <>
      <input type="hidden" name="fields" value={JSON.stringify(fields)} />
      <FormEditor
        value={initialFields}
        onChange={setFields}
        messages={messages}
      />
    </>
  );
}
