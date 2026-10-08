"use client";

import { useCallback, useState } from "react";
import FormEditor from "./FormEditor";
import type {
  AnnotationOption,
  EditorDimension,
  FormEditorContext,
} from "./editFieldForm";
import { DimensionUniverse, Field } from "./models";
import type { Translations } from "@/translations/en";

interface Props {
  initialFields: Field[];
  dimensions: EditorDimension[];
  defaultDimensionUniverse?: DimensionUniverse;
  annotations?: AnnotationOption[];
  formContext?: FormEditorContext;
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
  defaultDimensionUniverse,
  annotations,
  formContext,
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
      defaultDimensionUniverse={defaultDimensionUniverse}
      annotations={annotations}
      formContext={formContext}
      value={fields}
      messages={messages}
      onChange={handleChange}
      onPromoteFieldToDimension={onPromoteFieldToDimension}
    />
  );
}
