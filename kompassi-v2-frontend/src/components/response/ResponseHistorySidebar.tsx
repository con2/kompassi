import { Translations } from "@/translations/en";
import FormattedDateTime from "../FormattedDateTime";
import { graphql } from "@/__generated__";
import { ResponseHistorySidebarFragment } from "@/__generated__/graphql";
import { Session } from "next-auth";
import ModalButton from "../ModalButton";
import { ProfileFields } from "../profile/ProfileFields";
import Link from "next/link";

graphql(`
  fragment ResponseHistorySidebar on FullResponseType {
    id
    originalCreatedAt
    originalCreatedBy {
      fullName
      ...FullSelectedProfile
    }
    revisionCreatedAt
    revisionCreatedBy {
      fullName
    }
    language
    form {
      survey {
        profileFieldSelector {
          ...FullProfileFieldSelector
        }
      }
    }

    supersededBy {
      ...ResponseRevision
    }
    oldVersions {
      ...ResponseRevision
    }
  }
`);

interface Props {
  messages: {
    Survey: Translations["Survey"];
    Profile: Translations["Profile"];
  };
  event: {
    slug: string;
    timezone: string;
  };
  response: ResponseHistorySidebarFragment;
  locale: string;
  session: Session | null;
  responsesBaseUrl: string;
}

export default function ResponseHistorySidebar({
  messages,
  event,
  response,
  locale,
  session,
  responsesBaseUrl,
}: Props) {
  const t = messages.Survey;
  return (
    <div className="card mb-3 h-100">
      <div className="card-body">
        <h5 className="card-title mb-3">{t.attributes.technicalDetails}</h5>

        <div className="mb-4">
          <label className="form-label fw-bold">
            {t.attributes.originalCreatedAt}
          </label>
          <div>
            <FormattedDateTime
              value={response.originalCreatedAt}
              locale={locale}
              scope={event}
              session={session}
            />
          </div>
        </div>

        {response.originalCreatedBy && (
          <div className="mb-4">
            <label className="form-label fw-bold">
              {t.attributes.originalCreatedBy}
            </label>
            <div>
              <ModalButton
                className="btn btn-link p-0 link-subtle"
                label={response.originalCreatedBy.fullName + "…"}
                title={t.actions.viewProfile.title}
                messages={t.actions.viewProfile.modalActions}
              >
                <ProfileFields
                  profileFieldSelector={
                    response.form.survey.profileFieldSelector
                  }
                  profile={response.originalCreatedBy}
                  messages={messages.Profile}
                />
              </ModalButton>
            </div>
          </div>
        )}

        {response.oldVersions.length > 0 && (
          <>
            <div className="mb-4">
              <label className="form-label fw-bold">
                {t.attributes.currentVersionCreatedAt}
              </label>
              <div>
                <FormattedDateTime
                  value={response.revisionCreatedAt}
                  locale={locale}
                  scope={event}
                  session={session}
                />
              </div>
            </div>

            {response.revisionCreatedBy && (
              <div className="mb-4">
                <label className="form-label fw-bold">
                  {t.attributes.currentVersionCreatedBy}
                </label>
                <div>{response.revisionCreatedBy.fullName}</div>
              </div>
            )}

            <div className="mb-4">
              <label className="form-label fw-bold">
                {t.ResponseHistory.title}
              </label>
              <ul className="list-unstyled m-0">
                {response.oldVersions.map((version) => (
                  <li key={version.id}>
                    <Link
                      href={`${responsesBaseUrl}/${version.id}`}
                      className="link-subtle"
                    >
                      <FormattedDateTime
                        value={version.revisionCreatedAt}
                        locale={locale}
                        scope={event}
                        session={session}
                      />
                      {version.revisionCreatedBy && (
                        <> ({version.revisionCreatedBy?.displayName})</>
                      )}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
