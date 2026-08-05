"use client";
import { ModalButton } from "@con2/components";

import { useState } from "react";

import RecipientFilterEditor, { FilterGroup } from "./RecipientFilterEditor";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

interface RecipientFilterItem {
  dimension: string;
  values?: string[] | null;
}

interface Props {
  name: string;
  initialGroups: RecipientFilterItem[][];
  dimensions: DimensionValueSelectFragment[];
  modalTitle: string;
  modalMessages: Translations["Modal"];
  confirmLabel: string;
  editorMessages: Translations["Program"]["Message"]["recipientEditor"];
  buttonClassName?: string;
}

function groupsToJson(groups: FilterGroup[]) {
  const cleaned = groups
    .map((group) =>
      Object.entries(group)
        .filter(([, values]) => values.length > 0)
        .map(([dimension, values]) => ({ dimension, values })),
    )
    .filter((group) => group.length > 0);
  return JSON.stringify(cleaned);
}

function toFilterGroups(
  recipientGroups: RecipientFilterItem[][],
): FilterGroup[] {
  const converted = recipientGroups.map((group) => {
    const record: Record<string, string[]> = {};
    for (const item of group) {
      record[item.dimension] = item.values ?? [];
    }
    return record;
  });
  return converted.length > 0 ? converted : [{}];
}

/// Owns the recipientFilters selection state so it survives the "Edit recipients"
/// modal being closed and reopened - react-bootstrap's Modal unmounts its body while
/// hidden, so state must live in a component that stays mounted for as long as the
/// page does, not in the modal's children. Renders a hidden input holding the current
/// selection as JSON; place this inside the compose <form> so it gets submitted with
/// the rest of the message.
export default function RecipientFilterField({
  name,
  initialGroups,
  dimensions,
  modalTitle,
  modalMessages,
  confirmLabel,
  editorMessages,
  buttonClassName = "btn btn-outline-secondary btn-sm",
}: Props) {
  const [groups, setGroups] = useState<FilterGroup[]>(() =>
    toFilterGroups(initialGroups),
  );

  return (
    <>
      <input type="hidden" name={name} value={groupsToJson(groups)} readOnly />
      <ModalButton
        title={modalTitle}
        messages={modalMessages}
        confirmLabel={confirmLabel}
        className={buttonClassName}
      >
        <RecipientFilterEditor
          groups={groups}
          onChange={setGroups}
          dimensions={dimensions}
          messages={editorMessages}
        />
      </ModalButton>
    </>
  );
}
