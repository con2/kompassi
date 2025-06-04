import type { HeadingLevel } from "../helpers/Heading";
import { Field } from "./models";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import type { Translations } from "@/translations/en";

interface SchemaFormProps {
  fields: Field[];
  values?: Record<string, any>;
  messages: Translations["SchemaForm"];
  headingLevel?: HeadingLevel;
  readOnly?: boolean;
  className?: string;

  /// For when you need to render multiple SchemaForms that may have fields with the same slug
  idPrefix?: string;

  /// For nested SchemaForms
  namePrefix?: string;
}

export function SchemaForm(props: SchemaFormProps) {
  const {
    fields,
    values,
    messages,
    headingLevel,
    readOnly,
    className = "",
    idPrefix,
    namePrefix,
  } = props;
  return (
    <div className={className}>
      {fields.map((field, index) => {
        let slug = field.slug;
        if (!slug) {
          console.warn(`Field ${index} has no slug`);
          slug = `field-${index}`;
        }

        if (namePrefix) {
          slug = `${namePrefix}.${slug}`;
        }

        return (
          <SchemaFormField
            key={slug}
            field={field}
            headingLevel={headingLevel}
            idPrefix={idPrefix}
          >
            <SchemaFormInput
              field={field}
              value={values?.[field.slug]}
              messages={messages}
              readOnly={readOnly}
              idPrefix={idPrefix}
            />
          </SchemaFormField>
        );
      })}
    </div>
  );
}
