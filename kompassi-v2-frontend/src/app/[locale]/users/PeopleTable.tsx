"use client";

import { Column, DataTable, FormattedDateTime } from "@con2/components";
import Link from "next/link";
import { useState } from "react";
import { Button } from "react-bootstrap";

import { AdminPersonFragment } from "@/__generated__/graphql";

/// Only plain strings: this is a client component, and a translation function
/// cannot cross the server boundary.
export interface PeopleTableMessages {
  id: string;
  lastName: string;
  firstName: string;
  nick: string;
  email: string;
  username: string;
  noUser: string;
  lastLogin: string;
  select: string;
  combineSelected: string;
  count: string;
}

interface Props {
  people: AdminPersonFragment[];
  locale: string;
  messages: PeopleTableMessages;
}

export function mergeHref(personIds: string[]) {
  return `/users/merge?${new URLSearchParams({ ids: personIds.join(",") })}`;
}

/// The list of people with a checkbox per row so that duplicate accounts
/// can be selected and combined.
export default function PeopleTable({ people, locale, messages }: Props) {
  const [selected, setSelected] = useState<string[]>([]);
  const t = messages;

  function toggle(personId: string) {
    setSelected((current) =>
      current.includes(personId)
        ? current.filter((id) => id !== personId)
        : [...current, personId],
    );
  }

  const columns: Column<AdminPersonFragment>[] = [
    {
      slug: "select",
      title: "",
      getCellContents: (row) => (
        <input
          type="checkbox"
          className="form-check-input"
          checked={selected.includes(row.id)}
          onChange={() => toggle(row.id)}
          aria-label={t.select}
        />
      ),
    },
    {
      slug: "id",
      title: t.id,
      getCellContents: (row) => (
        <Link href={`/users/${row.id}`} className="link-subtle">
          {row.id}
        </Link>
      ),
    },
    {
      slug: "lastName",
      title: t.lastName,
      getCellContents: (row) => (
        <Link href={`/users/${row.id}`} className="link-subtle">
          {row.lastName}
        </Link>
      ),
    },
    {
      slug: "firstName",
      title: t.firstName,
    },
    {
      slug: "nick",
      title: t.nick,
    },
    {
      slug: "email",
      title: t.email,
    },
    {
      slug: "username",
      title: t.username,
      getCellContents: (row) => row.username ?? <em>{t.noUser}</em>,
    },
    {
      slug: "lastLogin",
      title: t.lastLogin,
      getCellContents: (row) =>
        row.lastLogin ? (
          <FormattedDateTime value={row.lastLogin} locale={locale} />
        ) : (
          ""
        ),
    },
  ];

  return (
    <>
      <DataTable columns={columns} rows={people}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>{t.count}</td>
          </tr>
        </tfoot>
      </DataTable>
      <Button
        as={Link as any}
        href={mergeHref(selected)}
        variant="primary"
        disabled={selected.length < 2}
        className="mb-4"
      >
        {t.combineSelected} ({selected.length})
      </Button>
    </>
  );
}
