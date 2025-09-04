import { ButtonGroup } from "react-bootstrap";
import { deleteScheduleItem, putScheduleItem } from "./actions";
import ScheduleItemForm from "./ScheduleItemForm";
import {
  DimensionValueSelectFragment,
  ProgramAdminDetailScheduleItemFragment,
} from "@/__generated__/graphql";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import { formatDurationMinutes } from "@/components/FormattedDateTimeRange";
import ModalButton from "@/components/ModalButton";
import { getTranslations } from "@/translations";

interface Props {
  locale: string;
  program: {
    slug: string;
  };
  event: {
    slug: string;
    timezone: string;
  };
  dimensions: DimensionValueSelectFragment[];
  scheduleItems: ProgramAdminDetailScheduleItemFragment[];
}

export default async function ScheduleItemTable({
  locale,
  event,
  program,
  dimensions,
  scheduleItems,
}: Props) {
  const translations = getTranslations(locale);
  const t = translations.Program.ScheduleItem;
  const session = await auth();

  const columns: Column<ProgramAdminDetailScheduleItemFragment>[] = [
    // {
    //   slug: "slug",
    //   title: t.attributes.slug.title,
    // },
    {
      slug: "subtitle",
      title: t.attributes.subtitle.title,
      getCellContents: (row) => {
        const title = row.subtitle ? (
          <>{row.subtitle}</>
        ) : (
          <em>{t.attributes.subtitle.noSubtitle}</em>
        );
        const lock = row.isPublic ? null : (
          <>
            {" "}
            <span title={t.attributes.isPublic.notPublic}>🔒</span>
          </>
        );
        return (
          <>
            {title}
            {lock}
          </>
        );
      },
    },
    {
      slug: "startTime",
      title: t.attributes.startTime.title,
      getCellContents: (row) => (
        <FormattedDateTime
          value={row.startTime}
          scope={event}
          session={session}
          locale={locale}
          options={{ dateStyle: "full", timeStyle: "short" }}
        />
      ),
    },
    {
      slug: "duration",
      title: t.attributes.duration.title,
      getCellContents: (row) => (
        <>
          {formatDurationMinutes(row.durationMinutes, locale)} (
          {row.durationMinutes} min)
        </>
      ),
    },
    {
      slug: "location",
      title: t.attributes.location.title,
    },
    {
      slug: "actions",
      title: "",
      getCellElement: (row, children) => (
        <td className="text-end">{children}</td>
      ),
      getCellContents: (row) => (
        <ButtonGroup>
          <ModalButton
            className="btn btn-outline-primary btn-sm"
            title={t.actions.edit.title}
            label={t.actions.edit.label + "…"}
            messages={t.actions.edit.modalActions}
            action={putScheduleItem.bind(
              null,
              locale,
              event.slug,
              program.slug,
              row.slug,
            )}
          >
            <ScheduleItemForm
              event={event}
              scheduleItem={row}
              dimensions={dimensions}
              translations={translations}
            />
          </ModalButton>
          <ModalButton
            className="btn btn-outline-danger btn-sm"
            title={t.actions.remove.title}
            label={t.actions.remove.label + "…"}
            messages={t.actions.remove.modalActions}
            submitButtonVariant="danger"
            action={deleteScheduleItem.bind(
              null,
              locale,
              event.slug,
              program.slug,
              row.slug,
            )}
          >
            {t.actions.remove.message(row.title)}
          </ModalButton>
        </ButtonGroup>
      ),
    },
  ];

  const uniquenessInsurance =
    scheduleItems.length > 0 ? `-${scheduleItems.length + 1}` : "";
  const newScheduleItem: Partial<ProgramAdminDetailScheduleItemFragment> = {
    slug: `${program.slug}${uniquenessInsurance}`,
  };

  return (
    <DataTable columns={columns} rows={scheduleItems}>
      <tfoot>
        <tr>
          <td colSpan={2}>{t.tableFooter(scheduleItems.length)}</td>
          <td colSpan={columns.length - 2} className="text-end">
            <ButtonGroup>
              <ModalButton
                className="btn btn-outline-primary btn-sm"
                title={t.actions.add.title}
                label={t.actions.add.label + "…"}
                messages={t.actions.add.modalActions}
                action={putScheduleItem.bind(
                  null,
                  locale,
                  event.slug,
                  program.slug,
                  null, // schedule item slug extracted from form data
                )}
              >
                <ScheduleItemForm
                  event={event}
                  translations={translations}
                  scheduleItem={newScheduleItem}
                  dimensions={dimensions}
                />
              </ModalButton>
            </ButtonGroup>
          </td>
        </tr>
      </tfoot>
    </DataTable>
  );
}
