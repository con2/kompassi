import { graphql } from "@/__generated__";
import {
  AnnotationsFormAnnotationFragment,
  DimensionValueSelectFragment,
  InvolvedPersonDetailInvolvementFragment,
  InvolvementType,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionValueSelectionForm from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
import { ProfileFields } from "@/components/profile/ProfileFields";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { Translations } from "@/translations/en";
import { notFound } from "next/navigation";
import { Card, CardBody, CardText, CardTitle } from "react-bootstrap";
import { updateCombinedPerks } from "./actions";
import AnnotationsForm from "@/components/annotations/AnnotationsForm";
import { validateCachedAnnotations } from "@/components/annotations/models";

graphql(`
  fragment InvolvedPersonDetailInvolvement on LimitedInvolvementType {
    id
    type
    title
    adminLink
    isActive
    cachedDimensions
    cachedAnnotations
  }
`);

graphql(`
  fragment InvolvedPersonDetail on ProfileWithInvolvementType {
    id
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
    fullName

    profileFieldSelector {
      ...FullProfileFieldSelector
    }

    isActive

    involvements {
      ...InvolvedPersonDetailInvolvement
    }
  }
`);

const query = graphql(`
  query PersonPage($eventSlug: String!, $locale: String, $personId: Int!) {
    event(slug: $eventSlug) {
      slug
      name
      timezone

      involvement {
        dimensions(publicOnly: false, isShownInDetail: true) {
          ...CachedDimensionsBadges
          ...DimensionValueSelect
        }

        annotations(publicOnly: false, perksOnly: true) {
          ...AnnotationsFormAnnotation
        }

        person(id: $personId) {
          ...InvolvedPersonDetail
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    personId: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const personId = parseInt(params.personId, 10);
  const translations = getTranslations(locale);
  const t = translations.Involvement;
  const profileT = translations.Profile;

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, personId },
  });

  if (!data.event?.involvement?.person) {
    notFound();
  }

  const { event } = data;
  const title = getPageTitle({
    translations,
    event,
    viewTitle: profileT.singleTitle,
    subject: data.event.involvement.person.fullName,
  });
  return {
    title,
  };
}

function CombinedPerksCard({
  involvement,
  translations,
  dimensions,
  annotations,
  onChange,
}: {
  involvement: InvolvedPersonDetailInvolvementFragment;
  translations: Translations;
  dimensions: DimensionValueSelectFragment[];
  annotations: AnnotationsFormAnnotationFragment[];
  onChange: (formData: FormData) => Promise<void>;
}) {
  const t = translations.Involvement;

  validateCachedDimensions(involvement.cachedDimensions);
  validateCachedAnnotations(annotations, involvement.cachedAnnotations);

  annotations = annotations.filter((annotation) => !annotation.isComputed);

  return (
    <Card className="mb-3">
      <CardBody>
        <CardTitle>{t.attributes.combinedPerks.title}</CardTitle>
        <CardText>{t.attributes.combinedPerks.message}</CardText>
        <DimensionValueSelectionForm
          dimensions={dimensions}
          cachedDimensions={involvement.cachedDimensions}
          translations={translations}
          onChange={onChange}
        />
        <AnnotationsForm
          schema={annotations}
          values={involvement.cachedAnnotations}
          messages={translations.SchemaForm}
        />
      </CardBody>
    </Card>
  );
}

export default async function PersonPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const personId = parseInt(params.personId, 10);
  const translations = getTranslations(locale);
  const profileT = translations.Profile;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, personId },
  });

  if (!data.event?.involvement?.person) {
    notFound();
  }

  const { event } = data;
  const { person, dimensions, annotations } = data.event.involvement;

  const combinedPerksInvolvement = person.involvements.find(
    (i) => i.type === InvolvementType.CombinedPerks,
  );

  return (
    <InvolvementAdminView
      translations={translations}
      event={event}
      active="people"
      searchParams={searchParams}
    >
      <h3 className="mt-3 mb-3">{person.fullName}</h3>
      <Card className="mb-3">
        <CardBody>
          <CardTitle>{profileT.singleTitle}</CardTitle>
          <ProfileFields
            profile={person}
            profileFieldSelector={person.profileFieldSelector}
            messages={translations.Profile}
            className="row mt-3"
            fieldClassName="col-md-4 mb-3"
          />
        </CardBody>
      </Card>

      {combinedPerksInvolvement && (
        <CombinedPerksCard
          dimensions={dimensions}
          annotations={annotations}
          involvement={combinedPerksInvolvement}
          translations={translations}
          onChange={updateCombinedPerks.bind(
            null,
            locale,
            event.slug,
            person.id,
          )}
        />
      )}
    </InvolvementAdminView>
  );
}
