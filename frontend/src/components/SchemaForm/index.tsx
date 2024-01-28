import type { HeadingLevel } from "../helpers/Heading";
import { Field, Layout } from "./models";
import SchemaFormField from "./SchemaFormField";
import SchemaFormInput from "./SchemaFormInput";
import type { Translations } from "@/translations/en";

interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
  values?: Record<string, any>;
  messages: Translations["SchemaForm"];
  headingLevel?: HeadingLevel;
}

export function SchemaForm(props: SchemaFormProps) {
  const { fields, layout, values, messages, headingLevel } = props;
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
            headingLevel={headingLevel}
          >
            <SchemaFormInput
              field={field}
              value={values?.[field.slug]}
              messages={messages}
            />
          </SchemaFormField>
        );
      })}
    </>
  );
}
