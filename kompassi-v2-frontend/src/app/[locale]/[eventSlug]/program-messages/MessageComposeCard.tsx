import { SubmitButton } from "@con2/components";
import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";

import formatRecipientFilterSummary from "./formatRecipientFilterSummary";
import RecipientFilterField from "./RecipientFilterField";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import type { Translations } from "@/translations/en";

interface RecipientFilterItem {
  dimension: string;
  values?: string[] | null;
}

interface Props {
  formId: string;
  action(formData: FormData): void;
  translations: Translations;
  locale: string;
  replyToAddresses: { id: string; name: string; email: string }[];
  recipientDimensions: DimensionValueSelectFragment[];
  recipientGroups: RecipientFilterItem[][];
  /// null when the message has not been saved yet, so the actual recipient count is
  /// not yet known (it depends on data that only exists once the filters are saved).
  recipientCount: number | null;
  values: {
    subject: string;
    dispatch: string;
    replyToId: string;
    body: string;
  };
  /// Label for the submit button. The caller decides the wording (eg. "Save draft" vs.
  /// "Save changes") since that depends on whether this message has been sent yet -
  /// something this component does not otherwise need to know.
  saveLabel: ReactNode;
  /// Optional text shown next to the submit button, eg. to make clear that saving does
  /// not send the message.
  saveHelpText?: ReactNode;
}

/// The subject/body/dispatch/reply-to/recipients form shared by the "new message" and
/// "edit message" views. The caller decides what `action` does (create vs. update).
export default function MessageComposeCard({
  formId,
  action,
  translations,
  locale,
  replyToAddresses,
  recipientDimensions,
  recipientGroups,
  recipientCount,
  values,
  saveLabel,
  saveHelpText,
}: Props) {
  const t = translations.Program.Message;

  const fields: Field[] = [
    {
      slug: "subject",
      type: "SingleLineText",
      title: t.attributes.subject.title,
      required: true,
    },
    {
      slug: "dispatch",
      type: "SingleSelect",
      presentation: "dropdown",
      title: t.attributes.dispatch.title,
      helpText: t.attributes.dispatch.helpText,
      required: true,
      choices: [
        {
          slug: "PER_PERSON",
          title: t.attributes.dispatch.choices.PER_PERSON,
        },
        {
          slug: "PER_INVOLVEMENT",
          title: t.attributes.dispatch.choices.PER_INVOLVEMENT,
        },
      ],
    },
    {
      slug: "replyToId",
      type: "SingleSelect",
      presentation: "dropdown",
      title: t.attributes.replyTo.title,
      helpText: t.attributes.replyTo.helpText,
      required: true,
      choices: [
        { slug: "DEFAULT", title: t.attributes.replyTo.useDefault },
        ...replyToAddresses.map((replyTo) => ({
          slug: replyTo.id,
          title: `${replyTo.name} <${replyTo.email}>`,
        })),
      ],
    },
    {
      slug: "body",
      type: "MarkdownText",
      title: t.attributes.body.title,
      helpText: t.attributes.body.helpText,
      required: true,
      rows: 14,
    },
  ];

  const recipientSummary = formatRecipientFilterSummary(
    recipientGroups,
    recipientDimensions,
  );

  return (
    <Card className="mt-3 mb-3">
      <CardBody>
        <p>
          <strong>{t.attributes.recipientCount.title}:</strong>{" "}
          {recipientSummary || t.recipientEditor.noFiltersYet}{" "}
          {recipientCount === null
            ? t.attributes.recipientCount.notYetKnown
            : t.attributes.recipientCount.value(recipientCount)}
        </p>
        <form id={formId} action={action} className="mt-3">
          <RecipientFilterField
            name="recipientFilters"
            initialGroups={recipientGroups}
            dimensions={recipientDimensions}
            modalTitle={t.actions.editRecipients.title}
            modalMessages={translations.Modal}
            confirmLabel={t.recipientEditor.confirm}
            editorMessages={t.recipientEditor}
          />

          <SchemaForm
            fields={fields}
            values={values}
            messages={translations.SchemaForm}
            locale={locale}
          />
          <div className="align-items-center d-flex mt-3">
            <SubmitButton className="btn btn-primary">{saveLabel}</SubmitButton>
            {saveHelpText && (
              <span className="form-text ms-2">{saveHelpText}</span>
            )}
          </div>
        </form>
      </CardBody>
    </Card>
  );
}
