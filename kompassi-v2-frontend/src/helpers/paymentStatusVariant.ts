import { PaymentStatus } from "@/__generated__/graphql";

/// Bootstrap text/variant colour for a payment status, or undefined for
/// statuses that don't need to stand out from the surrounding text.
export default function paymentStatusVariant(
  status: PaymentStatus,
): string | undefined {
  switch (status) {
    case PaymentStatus.PaidAfterCancellation:
      return "danger";
    default:
      return undefined;
  }
}
