import { notFound } from "next/navigation";

import ButtonGroup from "react-bootstrap/ButtonGroup";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import {
  deleteProgramHost,
  inviteProgramHost,
  overrideFormattedHosts,
  resendInvitation,
  revokeInvitation,
  updateProgramHostDimensions,
} from "./actions";
import { annotationSlugs } from "./consts";
import { graphql } from "@/__generated__";
import {
  ProgramAdminDetailHostFragment,
  ProgramAdminDetailInvitationFragment,
  ProgramHostRole,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import AnnotationsForm from "@/components/annotations/AnnotationsForm";
import { validateCachedAnnotations } from "@/components/annotations/models";
import { Column, DataTable } from "@/components/DataTable";
import { buildKeyDimensionColumns } from "@/components/dimensions/ColoredDimensionTableCell";
import { buildDimensionValueSelectionForm } from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations, SupportedLanguage } from "@/translations";

graphql(`
  fragment ProgramAdminDetailHost on LimitedProgramHostType {
    id
    cachedDimensions
    programHostRole
    person {
      fullName
      firstName
      lastName
      nick
      email
      phoneNumber
      discordHandle
    }
  }
`);

graphql(`
  fragment ProgramAdminDetailInvitation on LimitedInvitationType {
    id
    email
    createdAt
    cachedDimensions
  }
`);

const query = graphql(`
  query ProgramAdminDetailHosts(
    $eventSlug: String!
    $programSlug: String!
    $annotationSlugs: [String!]!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      forms {
        inviteForms: surveys(
          includeInactive: true
          app: PROGRAM_V2
          purpose: INVITE
        ) {
          slug
          title(lang: $locale)
          cachedDefaultInvolvementDimensions
        }
      }

      program {
        involvementDimensions(publicOnly: false) {
          ...ColoredDimensionTableCell
          ...DimensionValueSelect
        }
        annotations(slug: $annotationSlugs, publicOnly: false) {
          ...AnnotationsFormAnnotation
        }
        program(slug: $programSlug) {
          slug
          title
          canInviteProgramHost

          cachedAnnotations(slug: $annotationSlugs, publicOnly: false)

          dimensions(publicOnly: false) {
            ...ProgramDimensionBadge
          }
          programHosts(includeInactive: true) {
            ...ProgramAdminDetailHost
          }
          invitations {
            ...ProgramAdminDetailInvitation
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    programSlug: string;
  }>;
  searchParams: Promise<{
    success?: string;
  }>;
}

export const revalidate = 0;

// must be in sync with the supported languages in Invitation.send in backend
const supportedInviteLanguages: SupportedLanguage[] = ["fi", "en"];

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale, annotationSlugs },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.ProgramHost.listTitle,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramAdminDetailPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const profileT = translations.Profile;
  const inviT = translations.Invitation;
  const t = translations.Program.ProgramHost;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale, annotationSlugs },
  });
  if (!data.event?.program?.program) {
    notFound();
  }

  const event = data.event;
  const program = data.event.program.program;
  const programHosts = data.event.program.program.programHosts;
  const invitations = data.event.program.program.invitations;
  const annotations = data.event.program.annotations;
  const defaultProgramForm = data.event.forms?.inviteForms[0];

  const involvementDimensions = data.event.program.involvementDimensions ?? [];
  const involvementDimensionColumns = buildKeyDimensionColumns(
    involvementDimensions.filter((dimension) => dimension.slug !== "state"),
  );
  // TODO this makes limited sense if there are multiple accept invite forms
  const involvementDimensionDefaults =
    defaultProgramForm?.cachedDefaultInvolvementDimensions ?? {};
  validateCachedDimensions(involvementDimensionDefaults);
  const {
    fields: involvementDimensionFields,
    values: involvementDimensionValues,
  } = buildDimensionValueSelectionForm(
    involvementDimensions,
    involvementDimensionDefaults,
    "omit",
    "involvement_dimensions",
  );

  const programHostColumns: Column<ProgramAdminDetailHostFragment>[] = [
    {
      slug: "lastName",
      title: profileT.advancedAttributes.lastName.title,
      getCellContents: (row) => row.person.lastName,
    },
    {
      slug: "firstName",
      title: profileT.advancedAttributes.firstName.title,
      getCellContents: (row) => row.person.firstName,
    },
    {
      slug: "nick",
      title: profileT.advancedAttributes.nick.title,
      getCellContents: (row) => row.person.nick,
    },
    {
      slug: "email",
      title: profileT.advancedAttributes.email.title,
      getCellContents: (row) => row.person.email,
    },
    {
      slug: "phoneNumber",
      title: profileT.advancedAttributes.phoneNumber.title,
      getCellContents: (row) => row.person.phoneNumber,
    },
    {
      slug: "discordHandle",
      title: profileT.advancedAttributes.discordHandle.title,
      getCellContents: (row) => row.person.discordHandle,
    },
    ...involvementDimensionColumns,
    {
      slug: "role",
      title: (
        <>
          <span className="visually-hidden">{t.attributes.role.title}</span>
        </>
      ),
      getCellContents: (row) =>
        row.programHostRole === ProgramHostRole.Offerer ? (
          <span title={t.attributes.role.choices.OFFERER.description}>👑</span>
        ) : (
          <></>
        ),
    },
    {
      slug: "actions",
      title: "",
      className: "text-end",
      getCellContents: (row) => {
        validateCachedDimensions(row.cachedDimensions);
        const { fields, values } = buildDimensionValueSelectionForm(
          involvementDimensions,
          row.cachedDimensions,
          "omit",
        );
        return (
          <ButtonGroup>
            <ModalButton
              className="btn btn-outline-primary btn-sm"
              label={t.actions.editProgramHost.label + "…"}
              title={t.actions.editProgramHost.title}
              messages={t.actions.editProgramHost.modalActions}
              disabled={!program.canInviteProgramHost}
              action={updateProgramHostDimensions.bind(
                null,
                locale,
                eventSlug,
                row.id,
              )}
            >
              <div className="mb-3">
                <div className="form-label fw-bold">{t.singleTitle}</div>
                <div>{row.person.fullName}</div>
              </div>
              <SchemaForm
                fields={fields}
                values={values}
                messages={translations.SchemaForm}
              />
            </ModalButton>
            <ModalButton
              className="btn btn-outline-danger btn-sm"
              label={t.actions.removeProgramHost.label + "…"}
              title={t.actions.removeProgramHost.title}
              messages={t.actions.removeProgramHost.modalActions}
              submitButtonVariant="danger"
              action={deleteProgramHost.bind(
                null,
                locale,
                eventSlug,
                programSlug,
                row.id,
              )}
            >
              {t.actions.removeProgramHost.message(
                row.person.fullName,
                program.title,
              )}
            </ModalButton>
          </ButtonGroup>
        );
      },
    },
  ];

  const invitationColumns: Column<ProgramAdminDetailInvitationFragment>[] = [
    {
      slug: "createdAt",
      title: inviT.attributes.createdAt,
      getCellContents: (row) => (
        <FormattedDateTime
          locale={locale}
          value={row.createdAt}
          scope={event}
          session={session}
        />
      ),
    },
    {
      slug: "email",
      title: inviT.attributes.email,
    },
    ...involvementDimensionColumns,
    {
      slug: "actions",
      title: "",
      className: "text-end",
      getCellContents: (row) => (
        <ButtonGroup>
          <ModalButton
            className="btn btn-outline-primary btn-sm"
            label={inviT.actions.resend.label + "…"}
            title={inviT.actions.resend.title}
            messages={inviT.actions.resend.modalActions}
            submitButtonVariant="primary"
            action={resendInvitation.bind(
              null,
              locale,
              eventSlug,
              program.slug,
              row.id,
            )}
          >
            {inviT.actions.resend.message(row.email)}
          </ModalButton>
          <ModalButton
            className="btn btn-outline-danger btn-sm"
            label={inviT.actions.revoke.label + "…"}
            title={inviT.actions.revoke.title}
            messages={inviT.actions.revoke.modalActions}
            submitButtonVariant="danger"
            action={revokeInvitation.bind(
              null,
              locale,
              eventSlug,
              program.slug,
              row.id,
            )}
          >
            {inviT.actions.revoke.message(row.email)}
          </ModalButton>
        </ButtonGroup>
      ),
    },
  ];

  const inviteProgramHostFields: Field[] = [
    {
      slug: "email",
      type: "SingleLineText",
      htmlType: "email",
      required: true,
      ...t.actions.inviteProgramHost.attributes.email,
    },
    {
      slug: "surveySlug",
      type: "SingleSelect",
      presentation: "dropdown",
      required: true,
      choices:
        data.event.forms?.inviteForms.map(({ slug, title }) => ({
          slug,
          title: `${slug}: ${title}`,
        })) ?? [],
      ...t.actions.inviteProgramHost.attributes.survey,
    },
    {
      slug: "language",
      type: "SingleSelect",
      presentation: "dropdown",
      required: true,
      choices: supportedInviteLanguages.map((languageCode) => ({
        slug: languageCode,
        title: translations.LanguageSwitcher.supportedLanguages[languageCode],
      })),
      ...t.actions.inviteProgramHost.attributes.language,
    },
  ];

  if (involvementDimensionFields.length > 0) {
    inviteProgramHostFields.push({
      slug: "dimensionsHeader",
      type: "StaticText",
      ...t.actions.inviteProgramHost.attributes.dimensionsHeader,
    });
    inviteProgramHostFields.push(...involvementDimensionFields);
  }

  const inviteProgramHostDefaults = {
    surveySlug: defaultProgramForm?.slug,
    language: locale,
    ...involvementDimensionValues,
  };

  validateCachedAnnotations(annotations, program.cachedAnnotations);
  const overrideFormattedHostsAnnotation = annotations[1];

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"programHosts"}
      searchParams={searchParams}
    >
      <DataTable rows={programHosts} columns={programHostColumns}>
        <tfoot>
          <tr>
            <td colSpan={programHostColumns.length - 2}>
              {t.attributes.count(programHosts.length)}
            </td>
            <td className="text-end" colSpan={2}>
              <ModalButton
                className="btn btn-outline-primary btn-sm"
                label={t.actions.inviteProgramHost.title + "…"}
                title={t.actions.inviteProgramHost.title}
                messages={t.actions.inviteProgramHost.modalActions}
                disabled={!program.canInviteProgramHost}
                action={inviteProgramHost.bind(
                  null,
                  locale,
                  eventSlug,
                  programSlug,
                )}
              >
                <p>{t.actions.inviteProgramHost.message}</p>
                <SchemaForm
                  fields={inviteProgramHostFields}
                  values={inviteProgramHostDefaults}
                  messages={translations.SchemaForm}
                  headingLevel="h5"
                />
              </ModalButton>
            </td>
          </tr>
        </tfoot>
      </DataTable>

      {invitations.length > 0 && (
        <>
          <h4 className="mt-5">{inviT.listTitle}</h4>
          <p>{inviT.listDescription}</p>
          <DataTable rows={invitations} columns={invitationColumns}>
            <tfoot>
              <tr>
                <td colSpan={invitationColumns.length - 1}>
                  {inviT.attributes.count(invitations.length)}
                </td>
              </tr>
            </tfoot>
          </DataTable>
        </>
      )}

      <Card className="mt-5">
        <CardBody>
          <CardTitle>{overrideFormattedHostsAnnotation.title}</CardTitle>
          <form
            action={overrideFormattedHosts.bind(
              null,
              locale,
              event.slug,
              program.slug,
            )}
          >
            <AnnotationsForm
              schema={annotations}
              values={program.cachedAnnotations}
              messages={translations.SchemaForm}
            />
            <SubmitButton>
              {translations.Common.standardActions.save}
            </SubmitButton>
          </form>
        </CardBody>
      </Card>
    </ProgramAdminDetailView>
  );
}
