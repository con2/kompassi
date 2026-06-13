import Link from "next/link";

import { PaymentStatus } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

interface Props {
  order: {
    status: PaymentStatus;
    canRequestCancellation: boolean;
  };
  cancelHref: string;
  contactEmail: string | null;
  messages: Translations["Tickets"]["Order"]["actions"]["requestCancellation"];
}

/// Renders a button link to the self-service cancellation page for eligible
/// orders. Paid orders that cannot be cancelled in self-service get a note to
/// contact ticket sales instead. Other orders get nothing.
export default function RequestCancellationSection({
  order,
  cancelHref,
  contactEmail,
  messages: t,
}: Props) {
  if (order.canRequestCancellation) {
    return (
      <div className="d-grid gap-2 mb-4">
        {/* prefetch disabled: only a small fraction of visitors ever open the
            cancellation page, so prefetching it from every order view is wasteful. */}
        <Link
          className="btn btn-outline-danger"
          href={cancelHref}
          prefetch={false}
        >
          {t.title}…
        </Link>
      </div>
    );
  }

  if (order.status === PaymentStatus.Paid) {
    return <p>{t.contactTicketSales(contactEmail)}</p>;
  }

  return null;
}
