import Link from "next/link";
import { ReactNode } from "react";
import {
  DimensionValueSelectFragment,
  ProgramAdminDetailScheduleItemFragment,
} from "@/__generated__/graphql";
import { buildDimensionField } from "@/components/dimensions/DimensionValueSelectionForm";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import type { Translations } from "@/translations/en";
import { isValidSlug } from "@/services/tickets";

interface Props {
  event: {
    slug: string;
  };
  scheduleItem?: Partial<ProgramAdminDetailScheduleItemFragment>;
  dimensions: DimensionValueSelectFragment[];
  translations: Translations;
}

export function buildScheduleItemForm(
  eventSlug: string,
  editingExisting: boolean,
  roomDimension: DimensionValueSelectFragment | "pass-through" | "omit",
  translations?: Translations,
) {
  if (!isValidSlug(eventSlug)) {
    throw new Error("Invalid event slug");
  }

  const t = translations?.Program.ScheduleItem;

  const DimensionsLink = ({ children }: { children: ReactNode }) => (
    <Link
      href={`/${eventSlug}/program-dimensions`}
      className="link-subtle"
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </Link>
  );

  const fields: Field[] = [
    {
      slug: "slug",
      type: "SingleLineText",
      required: true,
      readOnly: editingExisting,
      title: t?.attributes.slug.title,
      helpText: editingExisting ? "" : t?.attributes.slug.helpText,
    },
    {
      slug: "subtitle",
      type: "SingleLineText",
      ...t?.attributes.subtitle,
    },
    {
      slug: "startTime",
      type: "DateTimeField",
      required: true,
      ...t?.attributes.startTime,
    },
    {
      slug: "durationMinutes",
      type: "NumberField",
      required: true,
      ...t?.attributes.durationMinutes,
    },
  ];

  switch (roomDimension) {
    case "pass-through":
      fields.push({
        slug: "room",
        type: "SingleLineText",
      });
      break;

    case "omit":
      break;

    default:
      fields.push({
        ...buildDimensionField(roomDimension, {}).field,
        title: t?.attributes.room.title,
        helpText: t?.attributes.room.helpText(DimensionsLink),
      });
  }

  fields.push({
    slug: "freeformLocation",
    type: "SingleLineText",
    ...t?.attributes.freeformLocation,
  });

  return fields;
}

export default function ScheduleItemForm({
  event,
  scheduleItem,
  dimensions,
  translations,
}: Props) {
  const editingExisting = !!scheduleItem?.startTime;
  const roomDimension = dimensions.find((d) => d.slug === "room");

  const fields = buildScheduleItemForm(
    event.slug,
    editingExisting,
    roomDimension || "omit",
    translations,
  );

  return (
    <SchemaForm
      fields={fields}
      values={scheduleItem}
      messages={translations.SchemaForm}
      highlightReadOnlyFields
    />
  );
}
