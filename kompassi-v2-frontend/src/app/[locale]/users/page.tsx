import {
  DimensionFilters,
  SignInRequired,
  ViewContainer,
  ViewHeading,
} from "@con2/components";
import { decodeBoolean } from "@con2/components/helpers";
import Link from "next/link";
import { ReactNode } from "react";
import { Alert } from "react-bootstrap";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import PeopleTable from "./PeopleTable";
import "./graphql";

const query = graphql(`
  query UserAdminPage($search: String, $returnNone: Boolean = false) {
    admin {
      people(search: $search, returnNone: $returnNone) {
        ...AdminPerson
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
      viewTitle: translations.UserAdmin.listTitle,
    }),
  };
}

export const revalidate = 0;

export default async function UserAdminPage(props: Props) {
  const searchParams = await props.searchParams;
  const { locale } = await props.params;
  const translations = getTranslations(locale);
  const t = translations.UserAdmin;

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

  const { search = "", force = "false" } = searchParams;
  const showResults = decodeBoolean(force) || !!search;

  const { data } = await getClient().query({
    query,
    variables: { search, returnNone: !showResults },
  });
  const people = data.admin.people;

  function ForceLink({ children }: { children: ReactNode }) {
    const strongWithTheForce = new URLSearchParams({
      search,
      force: "strong",
    }).toString();
    return (
      <Link
        href={`/users?${strongWithTheForce}`}
        className="link-subtle"
        prefetch={false}
      >
        {children}
      </Link>
    );
  }

  return (
    <ViewContainer>
      <ViewHeading>{t.listTitle}</ViewHeading>

      <DimensionFilters
        dimensions={[]}
        className="mt-1"
        search={true}
        messages={t.filters}
        locale={locale}
      />

      {showResults ? (
        <PeopleTable
          people={people}
          locale={locale}
          messages={{
            id: t.attributes.id,
            lastName: translations.Profile.attributes.lastName,
            firstName: translations.Profile.attributes.firstName,
            nick: translations.Profile.attributes.nick,
            email: translations.Profile.attributes.email,
            username: t.attributes.username,
            noUser: t.attributes.noUser,
            lastLogin: t.attributes.lastLogin,
            select: t.actions.select,
            combineSelected: t.actions.combineSelected,
            count: t.attributes.count(people.length),
          }}
        />
      ) : (
        <Alert variant="warning">{t.noFiltersApplied(ForceLink)}</Alert>
      )}
    </ViewContainer>
  );
}
