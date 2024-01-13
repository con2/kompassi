import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import { Field, Layout } from "./models";

interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
}

export function SchemaForm({ fields, layout }: SchemaFormProps) {
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
            <SchemaFormInput field={field} value="" />
          </SchemaFormField>
        );
      })}
    </>
  );
}
