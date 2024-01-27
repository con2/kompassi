import { createDimension } from "../../actions";
import EditDimensionForm from "../../EditDimensionForm";
import InterceptingRouteModal from "@/components/InterceptingRouteModal";
import { getTranslations } from "@/translations";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export default function NewDimensionModal({ params }: Props) {
  const { eventSlug, surveySlug, locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey.editDimensionModal;

  return (
    <InterceptingRouteModal
      title={t.addTitle}
      messages={t.actions}
      action={createDimension.bind(null, eventSlug, surveySlug)}
    >
      <EditDimensionForm
        headingLevel="h5"
        messages={{
          SchemaForm: translations.SchemaForm,
          Survey: translations.Survey,
        }}
      />
    </InterceptingRouteModal>
  );
}
