import { SchemaForm } from "@/components/SchemaForm";
import { FormSchema, dummyForm } from "@/components/SchemaForm/models";

async function getFormSchema(eventSlug: string, formSlug: string, locale: string): Promise<FormSchema> {
  return dummyForm;
}

interface NewProgramProps {
  params: {
    locale: string;
    eventSlug: string;
    formSlug: string;
  };
}

export default async function NewProgramPage({ params }: NewProgramProps) {
  const { locale, eventSlug, formSlug } = params;
  const schema = await getFormSchema(eventSlug, formSlug, locale);
  const { fields, layout, title } = schema;

  return (
    <div className="container mt-4">
      <h1 className="mb-4">{title}</h1>
      <SchemaForm fields={fields} layout={"horizontal"} />
    </div>
  );
}
