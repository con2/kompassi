"use client";

import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";

import formatRecipientFilterSummary from "./formatRecipientFilterSummary";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

export type FilterGroup = Record<string, string[]>;

interface Props {
  groups: FilterGroup[];
  onChange(groups: FilterGroup[]): void;
  dimensions: DimensionValueSelectFragment[];
  messages: Translations["Program"]["Message"]["recipientEditor"];
  readOnly?: boolean;
}

function toFilterItems(groups: FilterGroup[]) {
  return groups
    .map((group) =>
      Object.entries(group)
        .filter(([, values]) => values.length > 0)
        .map(([dimension, values]) => ({ dimension, values })),
    )
    .filter((group) => group.length > 0);
}

/// Editor for a Message's recipientFilters: an OR of AND-groups of dimension value
/// selections. A controlled component - the caller (RecipientFilterField) owns
/// `groups`, so the selection survives this editor - and the modal it's normally shown
/// in - being unmounted (react-bootstrap's Modal unmounts its body while hidden).
export default function RecipientFilterEditor({
  groups,
  onChange,
  dimensions,
  messages: t,
  readOnly = false,
}: Props) {
  function toggleValue(
    groupIndex: number,
    dimensionSlug: string,
    valueSlug: string,
    checked: boolean,
  ) {
    onChange(
      groups.map((group, idx) => {
        if (idx !== groupIndex) return group;
        const current = group[dimensionSlug] ?? [];
        const next = checked
          ? [...current, valueSlug]
          : current.filter((slug) => slug !== valueSlug);
        return { ...group, [dimensionSlug]: next };
      }),
    );
  }

  const liveSummary = formatRecipientFilterSummary(
    toFilterItems(groups),
    dimensions,
  );

  return (
    <div>
      <p className="text-muted small">
        {t.currentSelection}: {liveSummary || t.noFiltersYet}
      </p>
      {groups.map((group, groupIndex) => (
        <Card className="mb-2" key={groupIndex}>
          <CardBody>
            {groupIndex > 0 && (
              <p className="text-muted small mb-2">{t.orSeparator}</p>
            )}
            <div className="row row-cols-md-auto g-3">
              {dimensions.map((dimension) => (
                <div className="col-12" key={dimension.slug}>
                  <strong className="d-block mb-1">
                    {dimension.title ?? dimension.slug}
                  </strong>
                  {dimension.values.map((value) => {
                    const checked = (group[dimension.slug] ?? []).includes(
                      value.slug,
                    );
                    const inputId = `recipient-filter-${groupIndex}-${dimension.slug}-${value.slug}`;
                    return (
                      <div className="form-check" key={value.slug}>
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id={inputId}
                          checked={checked}
                          disabled={readOnly}
                          onChange={(event) =>
                            toggleValue(
                              groupIndex,
                              dimension.slug,
                              value.slug,
                              event.target.checked,
                            )
                          }
                        />
                        <label className="form-check-label" htmlFor={inputId}>
                          {value.title ?? value.slug}
                        </label>
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
            {!readOnly && groups.length > 1 && (
              <Button
                variant="outline-danger"
                size="sm"
                className="mt-2"
                onClick={() =>
                  onChange(groups.filter((_, idx) => idx !== groupIndex))
                }
              >
                {t.removeGroup}
              </Button>
            )}
          </CardBody>
        </Card>
      ))}
      {!readOnly && (
        <Button
          variant="outline-secondary"
          size="sm"
          onClick={() => onChange([...groups, {}])}
        >
          {t.addGroup}
        </Button>
      )}
    </div>
  );
}
