import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import { Field, Layout } from "./models";

interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
}

export function SchemaForm({ fields, layout }: SchemaFormProps) {
  return (
    <form>
      {fields.map((field) => (
        <SchemaFormField key={field.name} field={field} layout={layout ?? "vertical"}>
          <SchemaFormInput field={field} value="" />
        </SchemaFormField>
      ))}
    </form>
  );
}
