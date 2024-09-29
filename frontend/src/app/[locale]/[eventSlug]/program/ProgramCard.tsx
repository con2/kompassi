import Link from "next/link";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardTitle from "react-bootstrap/CardTitle";
import FavoriteButton from "./FavoriteButton";
import { Event } from "./models";
import ScheduleItem from "./ScheduleItem";
import { getProgramColorBorder } from "./style";
import { ProgramListFragment } from "@/__generated__/graphql";

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
              href={`/${event.slug}/programs/${program.slug}`}
              className="link-subtle"
            >
              {program.title}
            </CardLink>
          </CardTitle>
          {isLoggedIn && <FavoriteButton slug={program.slug} />}
        </div>
        {program.scheduleItems.map((scheduleItem, index) => (
          <div key={index} className="d-flex justify-content-between">
            <ScheduleItem
              event={event}
              scheduleItem={scheduleItem}
              locale={locale}
            />
          </div>
        ))}
      </CardBody>
    </Card>
  );
}
