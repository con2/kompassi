import Link from "next/link";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardTitle from "react-bootstrap/CardTitle";
import FavoriteButton from "./FavoriteButton";
import { getProgramColorBorder } from "./style";
import { ProgramListFragment } from "@/__generated__/graphql";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";

// XXX
interface Event {
  slug: string;
}

interface Props {
  event: Event;
  program: ProgramListFragment;
  locale: string;
  isLoggedIn: boolean;
}

export default function ProgramCard({
  program,
  event,
  locale,
  isLoggedIn,
}: Props) {
  return (
    <Card
      key={program.slug}
      className="mb-3"
      style={getProgramColorBorder(program)}
    >
      <CardBody>
        <div className="d-flex justify-content-between">
          <CardTitle>
            <CardLink
              as={Link}
              href={`/events/${event.slug}/programs/${program.slug}`}
              className="link-subtle"
            >
              {program.title}
            </CardLink>
          </CardTitle>
          {isLoggedIn && <FavoriteButton slug={program.slug} />}
        </div>
        {program.scheduleItems.map((scheduleItem, index) => (
          <div key={index} className="d-flex justify-content-between">
            <div>
              <FormattedDateTimeRange
                locale={locale}
                scope={event}
                session={null}
                start={scheduleItem.startTime}
                end={scheduleItem.endTime}
                includeDuration={true}
              />
            </div>
            <div>{scheduleItem.location}</div>
          </div>
        ))}
      </CardBody>
    </Card>
  );
}
