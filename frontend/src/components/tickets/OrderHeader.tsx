import Section from "../Section";
import { PaymentStatus } from "@/__generated__/graphql";
import FormattedDateTime from "@/components/FormattedDateTime";
import ViewHeading from "@/components/ViewHeading";
import { Translations } from "@/translations/en";

interface Props {
  locale: string;
  order: {
    formattedOrderNumber: string;
    createdAt: string;
    status: PaymentStatus;
  };
  messages: Translations["Tickets"];
  session?: {}; // TODO timezone stuff
  event: {
    name: string;
  };
}

export default function OrderHeader({
  order,
  messages,
  locale,
  session,
  event,
}: Props) {
  const t = messages.Order;
  const {
    title,
    shortTitle: paymentStatus,
    message,
  } = t.attributes.status.choices[order.status];

  return (
    <>
      <ViewHeading>
        {title}
        <ViewHeading.Sub>{messages.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>
      <p>{message}</p>

      <Section>
        <div>
          <strong>{t.attributes.orderNumberFull}</strong>:{" "}
          {order.formattedOrderNumber}
        </div>
        <div>
          <strong>{t.attributes.createdAt}</strong>:{" "}
          <FormattedDateTime
            value={order.createdAt}
            locale={locale}
            scope={event}
            session={session}
          />
        </div>
      </Section>
    </>
  );
}
