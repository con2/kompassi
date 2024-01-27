import Link from "next/link";
import { notFound } from "next/navigation";
import { createDimension } from "../actions";
import EditDimensionForm from "../EditDimensionForm";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SubmitButton from "@/components/SchemaForm/SubmitButton";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query NewDimensionPage(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String!
  ) {
    event(slug: $eventSlug) {
      name
      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.actions.addDimension,
  });

  return { title };
}

export default async function NewDimensionPage({ params }: Props) {
  const { eventSlug, surveySlug, locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const survey = data.event.forms.survey;

  return (
    <ViewContainer>
      <Link
        className="link-subtle"
        href={`/events/${eventSlug}/surveys/${surveySlug}/dimensions`}
      >
        &lt; {t.actions.returnToDimensionList}
      </Link>

      <ViewHeading>
        {t.actions.addDimension}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </ViewHeading>

      <form action={createDimension.bind(null, eventSlug, surveySlug)}>
        <EditDimensionForm
          headingLevel="h5"
          messages={{
            SchemaForm: translations.SchemaForm,
            Survey: translations.Survey,
          }}
        />
        <SubmitButton>{t.editDimensionModal.actions.submit}</SubmitButton>
      </form>
    </ViewContainer>
  );
}
