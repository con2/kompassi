import {
  Column,
  DataTable,
  Messages,
  SignInRequired,
  ViewContainer,
  ViewHeading,
} from "@con2/components";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Alert, Button } from "react-bootstrap";

import { graphql } from "@/__generated__";
import { AdminPersonFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import "../graphql";
import { mergePeople } from "./actions";

const query = graphql(`
  query UserAdminMergePage($personIds: [Int!]!, $intoPersonId: Int) {
    admin {
      mergePreview(personIds: $personIds, intoPersonId: $intoPersonId) {
        into {
          id
        }
        people {
          ...AdminPerson
        }
        references {
          model
          field
          count
        }
        conflicts {
          model
          field
          personId
          description
        }
        canMerge
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const { locale } = await props.params;
  const translations = getTranslations(locale);

  return {
    title: getPageTitle({
      translations,
      viewTitle: translations.UserAdmin.merge.title,
    }),
  };
}

export const revalidate = 0;

function parseIds(value: string | undefined): number[] {
  return (value ?? "")
    .split(",")
    .map((id) => parseInt(id, 10))
    .filter((id) => !isNaN(id));
}

export default async function UserAdminMergePage(props: Props) {
  const searchParams = await props.searchParams;
  const { locale } = await props.params;
  const translations = getTranslations(locale);
  const t = translations.UserAdmin;
  const profileT = translations.Profile;

  const session = await auth();
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const personIds = parseIds(searchParams.ids);
  const requestedInto = parseIds(searchParams.into)[0];
  if (personIds.length < 2) {
    notFound();
  }

  const { data } = await getClient().query({
    query,
    variables: { personIds, intoPersonId: requestedInto ?? null },
  });
  const preview = data.admin.mergePreview;
  const intoId = preview.into.id;
  const mergeIds = personIds.filter((id) => String(id) !== intoId);

  const survivorHref = (personId: string) =>
    `/users/merge?${new URLSearchParams({ ids: personIds.join(","), into: personId })}`;

  const columns: Column<AdminPersonFragment>[] = [
    {
      slug: "survivor",
      title: t.merge.survivor,
      getCellContents: (row) =>
        row.id === intoId ? (
          <strong>{t.merge.survivorMarker}</strong>
        ) : (
          <Link
            href={survivorHref(row.id)}
            className="link-subtle"
            prefetch={false}
          >
            {t.merge.chooseSurvivor}
          </Link>
        ),
    },
    { slug: "id", title: t.attributes.id },
    { slug: "lastName", title: profileT.attributes.lastName },
    { slug: "firstName", title: profileT.attributes.firstName },
    { slug: "nick", title: profileT.attributes.nick },
    { slug: "email", title: profileT.attributes.email },
    {
      slug: "username",
      title: t.attributes.username,
      getCellContents: (row) => row.username ?? <em>{t.attributes.noUser}</em>,
    },
  ];

  const confirm = mergePeople.bind(null, parseInt(intoId, 10), mergeIds);

  return (
    <ViewContainer>
      <ViewHeading>{t.merge.title}</ViewHeading>

      <Messages searchParams={searchParams} messages={t.messages} />

      <p>{t.merge.explanation}</p>

      <DataTable columns={columns} rows={preview.people} />

      <h2 className="h4 mt-4">{t.merge.references}</h2>
      {preview.references.length === 0 ? (
        <p className="text-muted">{t.merge.noReferences}</p>
      ) : (
        <table className="table table-sm">
          <thead>
            <tr>
              <th>{t.merge.model}</th>
              <th>{t.merge.field}</th>
              <th>{t.merge.count}</th>
            </tr>
          </thead>
          <tbody>
            {preview.references.map((reference) => (
              <tr key={`${reference.model}.${reference.field}`}>
                <td>
                  <code>{reference.model}</code>
                </td>
                <td>
                  <code>{reference.field}</code>
                </td>
                <td>{reference.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {preview.conflicts.length > 0 && (
        <>
          <h2 className="h4 mt-4">{t.merge.conflicts}</h2>
          <Alert variant="danger">{t.merge.cannotMerge}</Alert>
          <table className="table table-sm">
            <thead>
              <tr>
                <th>{t.attributes.id}</th>
                <th>{t.merge.model}</th>
                <th>{t.merge.field}</th>
                <th>{t.merge.description}</th>
              </tr>
            </thead>
            <tbody>
              {preview.conflicts.map((conflict, index) => (
                <tr key={index}>
                  <td>{conflict.personId}</td>
                  <td>
                    <code>{conflict.model}</code>
                  </td>
                  <td>
                    <code>{conflict.field}</code>
                  </td>
                  <td>{conflict.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      <Alert variant="warning" className="mt-4">
        {t.merge.warning}
      </Alert>

      <form action={confirm}>
        <Button type="submit" variant="danger" disabled={!preview.canMerge}>
          {t.merge.confirm}
        </Button>{" "}
        <Link href="/users" className="btn btn-link">
          {t.actions.backToList}
        </Link>
      </form>
    </ViewContainer>
  );
}
