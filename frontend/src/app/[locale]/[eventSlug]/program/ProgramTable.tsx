import Link from "next/link";
import FavoriteButton from "./FavoriteButton";
import ScheduleItem from "./ScheduleItem";
import { getProgramColorBorder } from "./style";
import { ProgramListFragment } from "@/__generated__/graphql";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";
import type { Translations } from "@/translations/en";

// XXX
interface Event {
  slug: string;
}

interface Props {
  event: Event;
  programs: ProgramListFragment[];
  locale: string;
  isLoggedIn: boolean;
  translations: Translations;
}

export default function ProgramTable({
  programs,
  event,
  locale,
  isLoggedIn,
  translations,
}: Props) {
  const t = translations.Program;
  const columns: Column<ProgramListFragment>[] = [
    {
      slug: "title",
      title: t.attributes.title,
      getCellContents(row) {
        return (
          <Link
            href={`/${event.slug}/programs/${row.slug}`}
            className="link-subtle"
          >
            {row.title}
          </Link>
        );
      },
      getCellElement(row, children) {
        return (
          <td
            scope="row"
            style={getProgramColorBorder(row)}
            className="align-middle"
          >
            {children}
          </td>
        );
      },
    },
    {
      slug: "scheduleItems",
      title: t.attributes.placeAndTime,
      getCellContents(row) {
        return (
          <>
            {row.scheduleItems.map((scheduleItem, index) => (
              <ScheduleItem
                event={event}
                scheduleItem={scheduleItem}
                locale={locale}
                key={index}
              />
            ))}
          </>
        );
      },
    },
  ];

  if (isLoggedIn) {
    columns.push({
      slug: "actions",
      title: <span className="visually-hidden">{t.attributes.actions}</span>,
      getCellContents(row) {
        return <FavoriteButton slug={row.slug} />;
      },
    });
  }

  return <DataTable rows={programs} columns={columns} />;
}
