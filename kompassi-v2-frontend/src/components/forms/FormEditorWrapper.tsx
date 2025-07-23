"use client";

import { useCallback, useState } from "react";
import FormEditor from "./FormEditor";
import { Field } from "./models";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

interface Props {
  initialFields: Field[];
  dimensions: DimensionValueSelectFragment[];
  messages: {
    FormEditor: Translations["FormEditor"];
    SchemaForm: Translations["SchemaForm"];
  };
  onChange(newFields: Field[]): Promise<void>;
  onPromoteFieldToDimension(fieldSlug: string): Promise<void>;
}

/// Wraps FormEditor with a client component that holds the state and handles calling the server action.
/// TODO Unify with FormEditor
export default function FormEditorWrapper({
  initialFields,
  messages,
  onChange,
  onPromoteFieldToDimension: onPromoteFieldToDimension,
  dimensions,
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
    <FormEditor
      dimensions={dimensions}
      value={fields}
      messages={messages}
      onChange={handleChange}
      onPromoteFieldToDimension={onPromoteFieldToDimension}
    />
  );
}
