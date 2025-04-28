import { ReactNode } from "react";

import ModalButton from "../ModalButton";
import DimensionForm from "./DimensionForm";
import DimensionValueForm from "./DimensionValueForm";
import { makeColorTranslucent } from "./helpers";
import {
  DimensionRowGroupFragment,
  ValueFieldsFragment,
} from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

interface Props {
  dimensions: DimensionRowGroupFragment[];
  translations: Translations;

  onCreateDimension(formData: FormData): Promise<void>;
  onUpdateDimension(dimensionSlug: string, formData: FormData): Promise<void>;
  onDeleteDimension(dimensionSlug: string): Promise<void>;
  onReorderDimensions(dimensionSlugs: string[]): Promise<void>;

  onCreateDimensionValue(
    dimensionSlug: string,
    formData: FormData,
  ): Promise<void>;
  onUpdateDimensionValue(
    dimensionSlug: string,
    valueSlug: string,
    formData: FormData,
  ): Promise<void>;
  onDeleteDimensionValue(
    dimensionSlug: string,
    valueSlug: string,
  ): Promise<void>;
  onReorderDimensionValues(
    dimensionSlug: string,
    valueSlugs: string[],
  ): Promise<void>;
}

export function DimensionEditor({
  dimensions,
  translations,
  onCreateDimension,
  onUpdateDimension,
  onDeleteDimension,
  onReorderDimensions,
  onCreateDimensionValue,
  onUpdateDimensionValue,
  onDeleteDimensionValue,
  onReorderDimensionValues,
}: Props) {
  const t = translations.Survey;

  function DeleteButton({
    subject,
    action,
    children,
  }: {
    subject: {
      title?: string | null;
      slug: string;
      canRemove: boolean;
    };
    action: (formData: FormData) => void;
    children?: ReactNode;
  }) {
    return (
      <ModalButton
        className="btn btn-link btn-sm p-0 link-xsubtle me-1"
        title={t.actions.deleteDimension.title}
        label={subject.canRemove ? "❌" : "🔒"}
        messages={t.actions.deleteDimension.modalActions}
        action={action}
        submitButtonVariant="danger"
        disabled={!subject.canRemove}
      >
        {children}
      </ModalButton>
    );
  }

  function DimensionCells({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    const rowspan = dimension.values.length + 1;
    const dimensionEditIcon = dimension.isTechnical ? "🔧" : "✏️";
    return (
      <>
        <td rowSpan={rowspan} scope="rowgroup">
          <DeleteButton
            subject={dimension}
            action={onDeleteDimension.bind(null, dimension.slug)}
          >
            <p>
              {t.actions.deleteDimension.confirmation(
                dimension.title || dimension.slug,
              )}
            </p>
          </DeleteButton>

          <ModalButton
            className="btn btn-link btn-sm p-0 link-xsubtle me-1"
            title={t.actions.editDimension}
            label={
              <>
                <span className="me-2">{dimensionEditIcon}</span>
                <code>{dimension.slug}</code>
              </>
            }
            messages={t.editDimensionModal.actions}
            action={onUpdateDimension.bind(null, dimension.slug)}
            disabled={dimension.isTechnical}
          >
            <DimensionForm
              messages={{
                SchemaForm: translations.SchemaForm,
                Survey: translations.Survey,
              }}
              dimension={dimension}
            />
          </ModalButton>
        </td>
        <td rowSpan={rowspan} scope="rowgroup">
          {dimension.title}
        </td>
      </>
    );
  }

  function AddValueCell({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    return (
      <td colSpan={3}>
        <ModalButton
          className="btn btn-link btn-sm p-0 link-xsubtle"
          title={t.actions.addDimensionValue}
          label={
            <>
              <span className="me-2">➕</span>
              {t.actions.addDimensionValue}
            </>
          }
          messages={t.editValueModal.actions}
          action={onCreateDimensionValue.bind(null, dimension.slug)}
        >
          {" "}
          <DimensionValueForm
            messages={{
              SchemaForm: translations.SchemaForm,
              Survey: translations.Survey,
            }}
          />
        </ModalButton>
      </td>
    );
  }

  function ValueCells({
    value,
    dimension,
  }: {
    value: ValueFieldsFragment;
    dimension: DimensionRowGroupFragment;
  }) {
    const backgroundColor = value.color && makeColorTranslucent(value.color);
    const valueEditIcon = value.isTechnical ? "🔧" : "✏️";

    return (
      <>
        <td style={{ backgroundColor }}>
          <DeleteButton
            subject={value}
            action={onDeleteDimensionValue.bind(
              null,
              dimension.slug,
              value.slug,
            )}
          >
            <p>
              {t.actions.deleteDimensionValue.confirmation(
                dimension.title || dimension.slug,
                value.title || value.slug,
              )}
            </p>
          </DeleteButton>
          <ModalButton
            className="btn btn-link btn-sm p-0 link-xsubtle"
            title={t.actions.editDimensionValue}
            label={
              <>
                <span className="me-2">{valueEditIcon}</span>
                <code>{value.slug}</code>
              </>
            }
            messages={t.editValueModal.actions}
            action={onUpdateDimensionValue.bind(
              null,
              dimension.slug,
              value.slug,
            )}
            disabled={value.isTechnical}
          >
            <DimensionValueForm
              messages={{
                SchemaForm: translations.SchemaForm,
                Survey: translations.Survey,
              }}
              value={value}
            />
          </ModalButton>
        </td>
        <td style={{ backgroundColor }}>{value.title}</td>
      </>
    );
  }

  function DimensionRowGroup({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    if (dimension.values.length === 0) {
      return (
        <tr style={{ borderWidth: "3px 0 3px 0" }}>
          <DimensionCells dimension={dimension} />
          <AddValueCell dimension={dimension} />
        </tr>
      );
    }

    return (
      <>
        {dimension.values.map((value, valueIndex) => {
          return (
            <tr key={`${dimension.slug}.${value.slug}`}>
              {valueIndex === 0 && <DimensionCells dimension={dimension} />}
              <ValueCells dimension={dimension} value={value} />
            </tr>
          );
        })}
        <tr>
          <AddValueCell dimension={dimension} />
        </tr>
      </>
    );
  }

  const countValues = dimensions.reduce(
    (acc, dimension) => acc + dimension.values.length,
    0,
  );

  return (
    <table className="table">
      <thead>
        <tr>
          <th colSpan={2}>{t.attributes.dimensions}</th>
          <th colSpan={2}>{t.attributes.values}</th>
        </tr>
        <tr style={{ borderWidth: "1px 0 3px 0" }}>
          <th scope="col">{t.attributes.slug.title}</th>
          <th scope="col">{t.attributes.title}</th>
          <th scope="col">{t.attributes.slug.title}</th>
          <th scope="col">{t.attributes.title}</th>
        </tr>
      </thead>
      <tbody>
        {dimensions.map((dimension) => (
          <DimensionRowGroup key={dimension.slug} dimension={dimension} />
        ))}
        <tr>
          <td colSpan={4}>
            <ModalButton
              className="btn btn-link btn-sm p-0 link-xsubtle"
              title={t.actions.addDimension}
              label={
                <>
                  <span className="me-2">➕</span>
                  {t.actions.addDimension}
                </>
              }
              messages={t.editDimensionModal.actions}
              action={onCreateDimension}
            >
              <DimensionForm
                messages={{
                  SchemaForm: translations.SchemaForm,
                  Survey: translations.Survey,
                }}
              />
            </ModalButton>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colSpan={4}>
            {t.dimensionTableFooter(dimensions.length, countValues)}
          </td>
        </tr>
      </tfoot>
    </table>
  );
}
