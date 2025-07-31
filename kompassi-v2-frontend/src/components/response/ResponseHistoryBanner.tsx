import { graphql } from "@/__generated__";
import {
  ProfileResponseHistoryBannerFragment,
  ResponseHistoryBannerFragment,
} from "@/__generated__/graphql";
import { Scope } from "@/app/[locale]/[eventSlug]/program/models";
import { auth } from "@/auth";
import type { Translations } from "@/translations/en";
import Link from "next/link";
import { Alert } from "react-bootstrap";
import FormattedDateTime from "../FormattedDateTime";
import { OldVersionAlert } from "./OldVersionAlert";

graphql(`
  fragment ResponseRevision on LimitedResponseType {
    id
    revisionCreatedAt
    revisionCreatedBy {
      displayName
    }
  }
`);

graphql(`
  fragment ResponseHistoryBanner on FullResponseType {
    id
    supersededBy {
      ...ResponseRevision
    }
    oldVersions {
      ...ResponseRevision
    }
    originalCreatedAt
  }
`);

graphql(`
  fragment ProfileResponseHistoryBanner on ProfileResponseType {
    id
    supersededBy {
      ...ResponseRevision
    }
    oldVersions {
      ...ResponseRevision
    }
    originalCreatedAt
  }
`);

interface Props {
  basePath: string;
  response:
    | ResponseHistoryBannerFragment
    | ProfileResponseHistoryBannerFragment;
  messages: {
    ResponseHistory: Translations["Survey"]["ResponseHistory"];
    OldVersionAlert: Translations["Survey"]["OldVersionAlert"];
  };
  locale: string;
  scope: Scope;
}

export async function ResponseHistoryBanner({
  basePath,
  messages,
  response,
  scope,
  locale,
}: Props) {
  const session = await auth();
  const t = messages.ResponseHistory;

  return (
    <>
      {response.supersededBy && (
        <OldVersionAlert
          supersededBy={response.supersededBy}
          basePath={basePath}
          messages={messages.OldVersionAlert}
        />
      )}
      {response.oldVersions.length > 0 && (
        <Alert variant="info" className="mb-4">
          <h5>{t.title}</h5>
          <p>{t.message}</p>
          <ul className="list-unstyled m-0">
            {response.oldVersions.map((version) => (
              <li key={version.id}>
                <Link
                  href={`${basePath}/${version.id}`}
                  className="link-subtle"
                >
                  <FormattedDateTime
                    value={version.revisionCreatedAt}
                    locale={locale}
                    scope={scope}
                    session={session}
                  />
                </Link>
              </li>
            ))}
          </ul>
        </Alert>
      )}
    </>
  );
}
