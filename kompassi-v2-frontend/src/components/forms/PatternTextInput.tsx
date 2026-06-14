"use client";

interface Props {
  className?: string;
  type: string;
  defaultValue?: string;
  required?: boolean;
  readOnly?: boolean;
  id: string;
  name: string;
  pattern?: string;
  maxLength?: number;
  /** Custom validity message shown when the value does not match `pattern`. */
  patternDescription: string;
}

/**
 * A single-line text input that reports a custom validity message on pattern mismatch.
 *
 * This is the only part of SchemaFormInput that needs client-side event handlers, so it
 * is split out: SchemaFormInput stays a shared (server-renderable) component and only this
 * small component is shipped to the client, and only for fields that set patternDescription.
 */
export default function PatternTextInput({
  className,
  type,
  defaultValue,
  required,
  readOnly,
  id,
  name,
  pattern,
  maxLength,
  patternDescription,
}: Props) {
  return (
    <input
      className={className}
      type={type}
      defaultValue={defaultValue}
      required={required}
      readOnly={readOnly}
      id={id}
      name={name}
      pattern={pattern}
      maxLength={maxLength}
      title={patternDescription}
      onInvalid={(e) => {
        if (e.currentTarget.validity.patternMismatch) {
          e.currentTarget.setCustomValidity(patternDescription);
        }
      }}
      onChange={(e) => e.currentTarget.setCustomValidity("")}
    />
  );
}
