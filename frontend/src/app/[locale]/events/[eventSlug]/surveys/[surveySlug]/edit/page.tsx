import Link from "next/link";
import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { updateSurvey } from "./actions";
import SurveyEditorTabs from "./SurveyEditorTabs";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment EditSurveyPage on SurveyType {
    slug
    title(lang: $locale)
    loginRequired
    anonymity
    maxResponsesPerUser
    countResponsesByCurrentUser

    languages {
      title
      language
    }
  }
`);

const query = graphql(`
  query EditSurveyPageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          ...EditSurveyPage
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

export const revalidate = 0;

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
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.editSurveyPage.title,
  });

  return { title };
}

export default async function EditSurveyPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data?.event?.forms?.survey) {
    notFound();
  }

  const { event } = data;
  const survey = data?.event?.forms?.survey;
  const {
    loginRequired,
    anonymity,
    maxResponsesPerUser,
    countResponsesByCurrentUser,
  } = survey;

  const fields: Field[] = [
    {
      slug: "loginRequired",
      type: "SingleCheckbox",
      ...t.attributes.loginRequired,
    },
    {
      slug: "maxResponsesPerUser",
      type: "NumberField",
      ...t.attributes.maxResponsesPerUser,
    },
  ];

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/events/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>

      <ViewHeading>
        {t.editSurveyPage.title}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </ViewHeading>

      <SurveyEditorTabs
        eventSlug={eventSlug}
        survey={data.event.forms.survey}
        translations={translations}
        active="properties"
      />
      <Card>
        <CardBody>
          <form action={updateSurvey.bind(null, eventSlug, surveySlug)}>
            <SchemaForm fields={fields} messages={translations.SchemaForm} />
            <SubmitButton>{t.actions.saveProperties}</SubmitButton>
          </form>
        </CardBody>
      </Card>
    </ViewContainer>
  );
}
