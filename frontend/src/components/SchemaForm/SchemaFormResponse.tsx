import { Field, Layout, nonValueFieldTypes } from "./models";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";

interface SchemaFormResponseProps {
  fields: Field[];
  layout: Layout;
  values: Record<string, unknown>;
}

/**
 * Provides a read-only view of a form response.
 */
export function SchemaFormResponse(props: SchemaFormResponseProps) {
  const { fields, layout, values } = props;

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
            <SchemaFormInput field={field} value={value} readOnly />
          </SchemaFormField>
        );
      })}
    </>
  );
}
