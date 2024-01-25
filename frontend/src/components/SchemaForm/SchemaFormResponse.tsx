import { Field, Layout } from "./models";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import type { Translations } from "@/translations/en";

interface SchemaFormResponseProps {
  fields: Field[];
  layout: Layout;
  values: Record<string, unknown>;
  messages: Translations["SchemaForm"];
}

/**
 * Provides a read-only view of a form response.
 */
export function SchemaFormResponse(props: SchemaFormResponseProps) {
  const { fields, layout, values, messages } = props;

  return (
    <>
      {fields.map((field, index) => {
        let slug = field.slug;
        if (!slug) {
          console.warn(`Field ${index} has no slug`);
          slug = `field-${index}`;
        }

        const value = values[slug];

        return (
          <SchemaFormField key={slug} field={field} layout={layout}>
            <SchemaFormInput
              field={field}
              value={value}
              messages={messages}
              readOnly
            />
          </SchemaFormField>
        );
      })}
    </>
  );
}
