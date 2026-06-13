import { requestOrderCancellation } from "./actions";
import FormattedDateTime from "@/components/FormattedDateTime";
import SubmitButton from "@/components/forms/SubmitButton";
import OrderCancellationView from "@/components/tickets/OrderCancellationView";
import { getOrder } from "@/services/tickets";
import { getTranslations } from "@/translations";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    orderId: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

/// Order cancellation request page. See OrderCancellationView for PII concerns.
export default async function OrderCancellationPage(props: Props) {
  const { locale, eventSlug, orderId } = await props.params;
  const searchParams = await props.searchParams;
  const data = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const cancelT = t.cancelPage;

  // A link was just sent. Requesting another one immediately is throttled by
  // design, so disable the button to avoid an inevitable failure.
  const cancellationRequested =
    searchParams.success === "cancellationRequested";

  return (
    <OrderCancellationView
      title={cancelT.title}
      eventSlug={eventSlug}
      orderId={orderId}
      data={data}
      messages={t}
      searchParams={searchParams}
    >
      {cancelT.explanation}

      {data.order.cancellationDeadline && (
        <p>
          {cancelT.deadline(
            <FormattedDateTime
              value={data.order.cancellationDeadline}
              locale={locale}
              scope={undefined}
              session={undefined}
            />,
          )}
        </p>
      )}

      <form
        action={requestOrderCancellation.bind(null, locale, eventSlug, orderId)}
      >
        <div className="d-grid gap-2 mb-4">
          <SubmitButton
            className={
              cancellationRequested
                ? "btn btn-secondary btn-lg"
                : "btn btn-danger btn-lg"
            }
            disabled={cancellationRequested}
          >
            {cancellationRequested
              ? cancelT.actions.cancellationLinkSent
              : cancelT.actions.sendConfirmationEmail}
          </SubmitButton>
        </div>
      </form>
    </OrderCancellationView>
  );
}
