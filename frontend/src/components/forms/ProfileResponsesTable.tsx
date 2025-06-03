import Link from "next/link";
import { ReactNode } from "react";
import { Column, DataTable } from "../DataTable";
import DimensionBadge from "../dimensions/DimensionBadge";
import FormattedDateTime from "../FormattedDateTime";
import { ProfileResponsesTableRowFragment } from "@/__generated__/graphql";
import { auth } from "@/auth";
import { Translations } from "@/translations/en";

interface Props {
  responses: ProfileResponsesTableRowFragment[];
  messages: Translations["Survey"];
  locale: string;
  extraColumns?: Column<ProfileResponsesTableRowFragment>[];
  footer?: ReactNode;
}

export default async function ProfileResponsesTable({
  responses,
  messages: t,
  locale,
  extraColumns = [],
  footer,
}: Props) {
  const session = await auth();

  const columns: Column<ProfileResponsesTableRowFragment>[] = [
    {
      slug: "revisionCreatedAt",
      title: t.attributes.originalCreatedAt,
      getCellContents: (row) => (
        <Link href={`/profile/responses/${row.id}`} className="link-subtle">
          <FormattedDateTime
            value={row.revisionCreatedAt}
            locale={locale}
            scope={row.form.event}
            session={session}
          />
        </Link>
      ),
    },
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (row) => row.form.event.name,
    },
    ...extraColumns,
    {
      slug: "actions",
      title: "",
      className: "text-end",
      getCellContents: (row) => {
        if (!row.canEdit) {
          return null;
        }
        return (
          <Link
            href={`/profile/responses/${row.id}/edit`}
            className="link-subtle"
          >
            ✏ {t.actions.editResponse.label}
          </Link>
        );
      },
    },
  ];

  return (
    <DataTable rows={responses} columns={columns}>
      {footer && (
        <tfoot>
          <tr>
            <td colSpan={columns.length}>{footer}</td>
          </tr>
        </tfoot>
      )}
    </DataTable>
  );
}
