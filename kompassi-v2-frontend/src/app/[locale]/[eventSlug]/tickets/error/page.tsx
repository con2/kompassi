import Link from "next/link";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";
import type { Translations } from "@/translations/en";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
  searchParams: Promise<{
    error?: string;
  }>;
}

function getErrorMessage(error: any, translations: Translations) {
  const errorMessages: Record<string, { title: string; message: string }> =
    translations.Tickets.Order.errors;

  return errorMessages[error] ?? errorMessages.UNKNOWN_ERROR;
}

export default async function TicketsErrorPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const { title, message } = getErrorMessage(searchParams.error, translations);

  return (
    <ViewContainer>
      <ViewHeading>{title}</ViewHeading>
      <p>{message}</p>
      <Link className="btn btn-primary" href={`/${eventSlug}/tickets`}>
        {translations.Tickets.returnToTicketsPage}
      </Link>
    </ViewContainer>
  );
}
