import { Temporal } from "@js-temporal/polyfill";
import { formatDateTime } from "../FormattedDateTime";
import { ProductListFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

interface Props {
  product: ProductListFragment;
  messages: Translations["Tickets"]["Product"];
  locale: string;
}

export default function ProductAvailability({
  product,
  messages: t,
  locale,
}: Props) {
  let activityEmoji = product.isAvailable ? "✅" : "❌";
  let message = "";

  // TODO(#436) proper handling of event & session time zones
  // Change untilTime(t: String): String to UntilTime(props: { children: ReactNode }): ReactNode
  // and init as <….UntilTime><FormattedDateTime … /></UntilTime>?
  if (product.isAvailable) {
    if (product.availableUntil) {
      message = t.serverAttributes.isAvailable.untilTime(
        formatDateTime(product.availableUntil, locale),
      );
    } else {
      message = t.serverAttributes.isAvailable.untilFurtherNotice;
    }
  } else {
    if (
      product.availableFrom &&
      Temporal.Instant.compare(
        Temporal.Instant.from(product.availableFrom),
        Temporal.Now.instant(),
      ) > 0
    ) {
      activityEmoji = "⏳";
      message = t.serverAttributes.isAvailable.openingAt(
        formatDateTime(product.availableFrom, locale),
      );
    } else {
      message = t.serverAttributes.isAvailable.notAvailable;
    }
  }

  return (
    <>
      {activityEmoji} {message}
    </>
  );
}
