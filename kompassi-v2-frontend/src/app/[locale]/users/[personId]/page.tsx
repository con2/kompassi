import {
  FormattedDateTime,
  Messages,
  SignInRequired,
  ViewContainer,
  ViewHeading,
} from "@con2/components";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Card, CardBody } from "react-bootstrap";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import "../graphql";

const query = graphql(`
  query UserAdminPersonPage($personId: Int!) {
    admin {
      person(id: $personId) {
        ...AdminPerson
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    personId: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const { locale } = await props.params;
  const translations = getTranslations(locale);

  return {
    title: getPageTitle({
      translations,
      viewTitle: translations.UserAdmin.personTitle,
    }),
  };
}

export const revalidate = 0;

export default async function UserAdminPersonPage(props: Props) {
  const searchParams = await props.searchParams;
  const { locale, personId } = await props.params;
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

  const { data } = await getClient().query({
    query,
    variables: { personId: parseInt(personId, 10) },
  });
  const person = data.admin.person;
  if (!person) {
    notFound();
  }

  const yesNo = (value: boolean) => (value ? t.yes : t.no);
  const dateOrEmpty = (value?: string | null) =>
    value ? <FormattedDateTime value={value} locale={locale} /> : "";

  const rows: [string, React.ReactNode][] = [
    [t.attributes.id, person.id],
    [profileT.attributes.firstName, person.firstName],
    [profileT.attributes.lastName, person.lastName],
    [profileT.attributes.nick, person.nick],
    [profileT.attributes.email, person.email],
    [profileT.attributes.phoneNumber, person.phoneNumber],
    [profileT.attributes.discordHandle, person.discordHandle],
    [t.attributes.username, person.username ?? <em>{t.attributes.noUser}</em>],
    [t.attributes.isActive, yesNo(person.isActive)],
    [t.attributes.isSuperuser, yesNo(person.isSuperuser)],
    [t.attributes.emailVerifiedAt, dateOrEmpty(person.emailVerifiedAt)],
    [t.attributes.dateJoined, dateOrEmpty(person.dateJoined)],
    [t.attributes.lastLogin, dateOrEmpty(person.lastLogin)],
    [
      t.attributes.groups,
      person.groups.length === 0 ? (
        <em>{t.attributes.noGroups}</em>
      ) : (
        <ul className="list-unstyled mb-0">
          {person.groups.map((group) => (
            <li key={group}>
              <code>{group}</code>
            </li>
          ))}
        </ul>
      ),
    ],
    [t.attributes.notes, person.notes],
  ];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.personTitle}
        <ViewHeading.Sub>{person.displayName}</ViewHeading.Sub>
      </ViewHeading>

      <Messages searchParams={searchParams} messages={t.messages} />

      <Card className="mb-4">
        <CardBody>
          <table className="table table-sm mb-0">
            <tbody>
              {rows.map(([label, value]) => (
                <tr key={label}>
                  <th scope="row">{label}</th>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardBody>
      </Card>

      <p>
        <Link href="/users" className="link-subtle">
          {t.actions.backToList}
        </Link>
      </p>
      <p className="text-muted">{t.combineHint}</p>
    </ViewContainer>
  );
}
