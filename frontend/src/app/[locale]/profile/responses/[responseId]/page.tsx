import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionBadge from "@/components/dimensions/DimensionBadge";
import SignInRequired from "@/components/errors/SignInRequired";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProfileSurveyResponsePage($locale: String!, $responseId: String!) {
    profile {
      forms {
        response(id: $responseId) {
          id
          createdAt
          values

          dimensions {
            ...DimensionBadge
          }

          form {
            title
            language
            fields
            event {
              slug
              name
            }
            survey {
              anonymity
            }
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    responseId: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;

  return {
    title: `${t.ownResponsesTitle} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function ProfileSurveyResponsePage({ params }: Props) {
  const { locale, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: {
      responseId,
      locale,
    },
  });

  if (!data.profile?.forms?.response) {
    notFound();
  }

  const t = translations.Survey;

  const response = data.profile.forms.response;
  const { createdAt, form } = response;
  const language = form.language;
  const { fields } = form;
  const values: Record<string, any> = response.values ?? {};

  const anonymity = form.survey?.anonymity;
  const anonymityMessages =
    translations.Survey.attributes.anonymity.secondPerson;

  validateFields(fields);

  // TODO using synthetic form fields for presentation is a hack
  // but it shall suffice until someone comes up with a Design Vision™
  const technicalFields: Field[] = [
    // TODO(#438) use DateTimeField
    {
      slug: "createdAt",
      type: "SingleLineText",
      title: t.attributes.createdAt,
    },
    {
      slug: "language",
      type: "SingleLineText",
      title: t.attributes.language,
    },
  ];
  const technicalValues = {
    createdAt: createdAt ? formatDateTime(createdAt, locale) : "",
    language,
  };

  const dimensions = response.dimensions ?? [];

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/profile/responses`}>
        &lt; {t.actions.returnToResponseList}
      </Link>

      <div className="d-flex">
        <ViewHeading>
          {t.responseDetailTitle}
          <ViewHeading.Sub>{form.title}</ViewHeading.Sub>
        </ViewHeading>
        {!!dimensions?.length && (
          <h3 className="ms-auto">
            {dimensions.map((dimension) => (
              <DimensionBadge
                key={dimension.dimension.slug}
                dimension={dimension}
              />
            ))}
          </h3>
        )}
      </div>

      {anonymity && (
        <p>
          <small>
            <strong>{anonymityMessages.title}: </strong>
            {anonymityMessages.choices[anonymity]}
          </small>
        </p>
      )}

      <div className="card mb-3">
        <div className="card-body">
          <h5 className="card-title mb-3">{t.attributes.technicalDetails}</h5>
          <SchemaForm
            fields={technicalFields}
            values={technicalValues}
            messages={translations.SchemaForm}
            readOnly
          />
        </div>
      </div>

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </ViewContainer>
  );
}
