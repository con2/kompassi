import { Field, Layout } from "./models";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";

interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
  values?: Record<string, any>;
}

export function SchemaForm({ fields, layout, values }: SchemaFormProps) {
  return (
    <>
      {fields.map((field, index) => {
        let slug = field.slug;
        if (!slug) {
          console.warn(`Field ${index} has no slug`);
          slug = `field-${index}`;
        }

        return (
          <SchemaFormField
            key={slug}
            field={field}
            layout={layout ?? Layout.Vertical}
          >
            <SchemaFormInput field={field} value={values?.[field.slug]} />
          </SchemaFormField>
        );
      })}
    </>
  );
}
