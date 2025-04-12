import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import SurveyEditorTabs from "../../../surveys/[surveySlug]/edit/SurveyEditorTabs";
import { deleteProgramForm } from "./actions";
import { Survey } from "./models";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import type { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  event: {
    name: string;
    slug: string;
  };
  survey: Survey;
  activeTab: string;
  children: ReactNode;
}

/// TODO could this / should this be a layout?
export default function ProgramFormEditorView({
  translations,
  event,
  survey,
  activeTab,
  children,
}: Props) {
  const t = translations.Program.ProgramForm;

  return (
    <ProgramAdminView
      translations={translations}
      event={event}
      active="programForms"
      queryString=""
      actions={
        <ModalButton
          title={t.actions.deleteProgramForm.title}
          messages={t.actions.deleteProgramForm.modalActions}
          className="btn btn-outline-danger"
          submitButtonVariant="danger"
          action={deleteProgramForm.bind(null, event.slug, survey.slug)}
          disabled={!survey.canRemove}
          // TODO disabledMessage={t.actions.deleteSurvey.cannotRemove}
        >
          {t.actions.deleteProgramForm.confirmation(
            survey.title || survey.slug,
          )}
        </ModalButton>
      }
    >
      <h2 className="mb-3 mt-3">{survey.title || survey.slug}</h2>
      <SurveyEditorTabs
        eventSlug={event.slug}
        survey={survey}
        translations={translations}
        active={activeTab}
        mode="program-forms"
      />
      <Card className="mb-2">
        <CardBody>{children}</CardBody>
      </Card>
    </ProgramAdminView>
  );
}
