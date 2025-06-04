import Link from "next/link";
import { notFound } from "next/navigation";

import { CardText, CardTitle } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";

import { updateProgramBasicInfo } from "../actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramAdminDetailSchedule(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        dimensions {
          slug
          title(lang: $locale)
        }

        program(slug: $programSlug) {
          slug
          title

          scheduleItems {
            slug
            subtitle
            location
            startTime
            endTime
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    programSlug: string;
  };
}

export const revalidate = 0;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.attributes.scheduleItems.title,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramAdminDetailSchedulePage({
  params,
}: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
  const iTem = translations.Program.ScheduleItem;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  if (!data.event?.program?.program) {
    notFound();
  }

  const event = data.event;
  const program = data.event.program.program;

  const DimensionsLink = ({ children }: { children: React.ReactNode }) => (
    <Link href={`/${event.slug}/program-dimensions`} className="link-subtle">
      {children}
    </Link>
  );

  const fields: Field[] = [
    {
      slug: "scheduleItems",
      ...t.attributes.scheduleItems,
      type: "MultiItemField",
      fields: [
        {
          slug: "slug",
          type: "SingleLineText",
          required: true,
          ...iTem.attributes.slug,
        },
        {
          slug: "subtitle",
          type: "SingleLineText",
          ...iTem.attributes.subtitle,
        },
        {
          slug: "startTime",
          type: "DateTimeField",
          required: true,
          ...iTem.attributes.startTime,
        },
        {
          slug: "durationMinutes",
          type: "NumberField",
          required: true,
          ...iTem.attributes.durationMinutes,
        },
        {
          slug: "room",
          type: "SingleSelect",
          choices: [],
          title: iTem.attributes.room.title,
          helpText: iTem.attributes.room.helpText(DimensionsLink),
        },
        {
          slug: "freeformLocation",
          type: "SingleLineText",
          ...iTem.attributes.freeformLocation,
        },
      ],
    },
  ];

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"scheduleItems"}
    >
      <Card>
        <CardBody>
          {" "}
          <form
            action={updateProgramBasicInfo.bind(
              null,
              locale,
              event.slug,
              program.slug,
            )}
          >
            <SchemaForm
              fields={fields}
              values={program}
              messages={translations.SchemaForm}
            />
            <SubmitButton>{translations.Common.submit}</SubmitButton>
          </form>
        </CardBody>
      </Card>
    </ProgramAdminDetailView>
  );
}
