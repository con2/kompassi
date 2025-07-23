import { Temporal } from "@js-temporal/polyfill";
import { Scope } from "./models";
import { ScheduleItemListFragment } from "@/__generated__/graphql";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";
import { timezone as defaultTimezone } from "@/config";

interface Props {
  scheduleItem: ScheduleItemListFragment;
  event: Scope;
  locale: string;
}

export default function ScheduleItem({
  scheduleItem,
  locale,
  event: event,
}: Props) {
  return (
    <div>
      {scheduleItem.location && <span>{scheduleItem.location}, </span>}
      <FormattedDateTimeRange
        locale={locale}
        scope={event}
        session={null}
        start={scheduleItem.startTime}
        end={scheduleItem.endTime}
        includeDuration={true}
      />
      {scheduleItem.subtitle && <span> ({scheduleItem.subtitle})</span>}
    </div>
  );
}
