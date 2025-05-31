import Link from "next/link";
import { Alert } from "react-bootstrap";
import FormattedDateTime from "../FormattedDateTime";
import { OldVersionAlert } from "./OldVersionAlert";
import { graphql } from "@/__generated__";
import { ResponseRevisionFragment } from "@/__generated__/graphql";
import { Scope } from "@/app/[locale]/[eventSlug]/program/models";
import { auth } from "@/auth";
import type { Translations } from "@/translations/en";

graphql(`
  fragment ResponseRevision on LimitedResponseType {
    id
    createdAt
    createdBy {
      displayName
    }
  }
`);

interface Props {
  basePath: string;
  supersededBy: ResponseRevisionFragment | null | undefined;
  oldVersions: ResponseRevisionFragment[];
  messages: {
    ResponseHistory: Translations["Survey"]["ResponseHistory"];
    OldVersionAlert: Translations["Survey"]["OldVersionAlert"];
  };
  locale: string;
  scope: Scope;
}

export async function ResponseHistory({
  basePath,
  supersededBy,
  oldVersions,
  messages,
  scope,
  locale,
}: Props) {
  const session = await auth();
  const t = messages.ResponseHistory;

  return (
    <>
      {supersededBy && (
        <OldVersionAlert
          supersededBy={supersededBy}
          basePath={basePath}
          messages={messages.OldVersionAlert}
        />
      )}
      {oldVersions.length > 0 && (
        <Alert variant="info" className="mb-4">
          <h5>{t.title}</h5>
          <p>{t.message}</p>
          <ul className="list-unstyled m-0">
            {oldVersions.map((version) => (
              <li key={version.id}>
                <Link
                  href={`${basePath}/${version.id}`}
                  className="link-subtle"
                >
                  <FormattedDateTime
                    value={version.createdAt}
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
