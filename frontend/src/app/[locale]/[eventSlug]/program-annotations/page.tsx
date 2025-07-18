import { notFound } from "next/navigation";

import { Badge } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import { putEventAnnotation } from "./actions";
import { graphql } from "@/__generated__";
import {
  ProgramAdminEventAnnotationFragment,
  PutEventAnnotationAction,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { mangleAnnotationSlug } from "@/components/annotations/models";
import { Column, DataTable } from "@/components/DataTable";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramAdminEventAnnotation on EventAnnotationType {
    annotation {
      slug
      title(lang: $locale)
      description(lang: $locale)
      type
      isComputed
      isPublic
      isShownInDetail
      isInternal
      isApplicableToProgramItems
      isApplicableToScheduleItems
    }
    isActive
    programFormFields
  }
`);

const query = graphql(`
  query ProgramAdminEventAnnotations($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        eventAnnotations {
          ...ProgramAdminEventAnnotation
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
  searchParams: Record<string, string>;
}

export const revalidate = 0;

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Annotation.listTitle,
  });
  return { title };
}

const annotationFlags = [
  "isShownInDetail",
  // "isApplicableToProgramItems",
  // "isApplicableToScheduleItems",
  // "isPublic",
  // "isComputed",
  "isInternal",
] as const;

export default async function ProgramAdminAnnotationsPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Annotation;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  if (!data.event?.program?.eventAnnotations) {
    notFound();
  }

  const event = data.event;
  const eventAnnotations = data.event.program.eventAnnotations.filter(
    (ea) => !ea.annotation.isComputed,
  );

  const columns: Column<ProgramAdminEventAnnotationFragment>[] = [
    {
      slug: "annotation",
      title: t.singleTitle,
      className: "col-6 py-3",
      getCellContents: (row) => (
        <>
          <p>
            <strong>{row.annotation.title}</strong> (
            <code>{row.annotation.slug}</code>)
          </p>
          <p>{row.annotation.description}</p>
          <div>
            {annotationFlags.map((flag) => {
              const flagValue = row.annotation[flag];
              if (!flagValue) {
                return null;
              }
              return (
                <Badge key={flag} bg="secondary" className="me-2">
                  {t.attributes[flag].title}
                </Badge>
              );
            })}
          </div>
        </>
      ),
    },
    {
      slug: "properties",
      title: t.attributes.properties.title,
      className: "col-6 py-3",
      getCellContents: (row) => {
        const slug = mangleAnnotationSlug(row.annotation.slug);
        const fields: Field[] = [
          {
            slug: "isActive",
            type: "SingleCheckbox",
            title: t.attributes.isActive.checkboxLabel(row.annotation.slug),
            readOnly: row.annotation.slug.startsWith("internal:"),
          },
          {
            slug: "programFormFields",
            type: "MultiLineText",
            rows: 5,
            title: t.attributes.programFormFields.title,
          },
        ];
        const values = {
          ...row,
          programFormFields: row.programFormFields?.join("\n") || "",
        };
        return (
          <form
            action={putEventAnnotation.bind(
              null,
              eventSlug,
              row.annotation.slug,
            )}
          >
            <SchemaForm
              fields={fields}
              values={values}
              messages={translations.SchemaForm}
              idPrefix={slug}
              className="m-0 p-0"
              labelClassName="form-label"
              fieldMargin="mb-3"
            />
            <SubmitButton className="mt-1 btn btn-sm btn-primary">
              {t.eventAnnotationsAdmin.actions.saveWithoutRefresh.title}
            </SubmitButton>
            <SubmitButton
              className="mt-1 ms-2 btn btn-sm btn-warning"
              name="action"
              value={PutEventAnnotationAction.SaveAndRefresh}
              confirmationMessage={
                t.eventAnnotationsAdmin.actions.saveAndRefresh
                  .confirmationMessage
              }
            >
              {t.eventAnnotationsAdmin.actions.saveAndRefresh.title}…
            </SubmitButton>
          </form>
        );
      },
    },
  ];

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active="annotations"
      searchParams={searchParams}
    >
      <Card className="mt-3 mb-3">
        <CardBody>
          <CardTitle>{t.eventAnnotationsAdmin.title}</CardTitle>
          {t.eventAnnotationsAdmin.message}
          <p>
            <em>{t.attributes.isActive.title}:</em>{" "}
            {t.attributes.isActive.description}
          </p>
          <p>
            <em>{t.attributes.programFormFields.title}:</em>{" "}
            {t.attributes.programFormFields.description}
          </p>
          <p>
            <em>{t.eventAnnotationsAdmin.actions.saveWithoutRefresh.title}:</em>{" "}
            {t.eventAnnotationsAdmin.actions.saveWithoutRefresh.description}
          </p>
          <p>
            <em>{t.eventAnnotationsAdmin.actions.saveAndRefresh.title}:</em>{" "}
            {t.eventAnnotationsAdmin.actions.saveAndRefresh.description}
          </p>
          <p>
            {t.eventAnnotationsAdmin.actions.createAnnotation.toBeImplemented}
          </p>
        </CardBody>
      </Card>
      <DataTable rows={eventAnnotations} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.eventAnnotationsAdmin.tableFooter(
                eventAnnotations.length,
                eventAnnotations.filter((ea) => ea.isActive).length,
              )}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ProgramAdminView>
  );
}
