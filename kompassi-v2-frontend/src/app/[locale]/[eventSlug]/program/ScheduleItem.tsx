import { FormattedDateTimeRange } from "@con2/components";
import { ScheduleItemListFragment } from "@/__generated__/graphql";
import { Scope } from "./models";

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
        timezone={event.timezone}
        start={scheduleItem.startTime}
        end={scheduleItem.endTime}
        includeDuration={true}
      />
      {scheduleItem.subtitle && <span> ({scheduleItem.subtitle})</span>}
    </div>
  );
}
