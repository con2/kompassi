import { SchemaForm } from "@/components/SchemaForm";
import { FormSchema, dummyForm } from "@/components/SchemaForm/models";
import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const query = gql(`
  query ProgrammeExampleQuery($eventSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      dimensions {
        title(lang: $locale)
      }

      offerForms {
        shortDescription(lang: $locale)
        form(lang: $locale) {
          title
          fields
        }
      }
    }
  }
`);

interface NewProgramProps {
  params: {
    locale: string;
    eventSlug: string;
    formSlug: string;
  };
}

export async function generateMetadata({ params }: NewProgramProps) {
  const { locale, eventSlug, formSlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  // TODO
  const { event } = data;
  return {
    title: `${event?.name}: ${dummyForm.title} – Kompassi`,
  };
}

export default async function NewProgramPage({ params }: NewProgramProps) {
  const { locale, eventSlug, formSlug } = params;
  const schema = dummyForm;
  const { fields, layout, title } = schema;

  return (
    <div className="container mt-4">
      <h1 className="mb-4">{title}</h1>
      <SchemaForm fields={fields} layout={"horizontal"} />
    </div>
  );
}
