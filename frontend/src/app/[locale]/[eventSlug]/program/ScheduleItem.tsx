import { Event } from "./models";
import { ScheduleItemListFragment } from "@/__generated__/graphql";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";

interface Props {
  scheduleItem: ScheduleItemListFragment;
  event: Event;
  locale: string;
}

export default function ScheduleItem({ scheduleItem, locale, event }: Props) {
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
