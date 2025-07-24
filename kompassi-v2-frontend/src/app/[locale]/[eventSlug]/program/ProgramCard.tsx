import Link from "next/link";

import {
  ScheduleItemListFragment,
  ScheduleProgramFragment,
} from "@/__generated__/graphql";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardTitle from "react-bootstrap/CardTitle";
import FavoriteButton from "./FavoriteButton";
import { Scope } from "./models";
import ScheduleItem from "./ScheduleItem";
import { getProgramColorBorder } from "./style";
import type { Translations } from "@/translations/en";

interface Props {
  event: Scope;
  program: ScheduleProgramFragment;
  scheduleItem: ScheduleItemListFragment;
  locale: string;
  isLoggedIn: boolean;
  messages: Translations["Program"];
}

export default function ProgramCard({
  program,
  scheduleItem,
  event,
  locale,
  isLoggedIn,
  messages: t,
}: Props) {
  return (
    <Card className="mb-3" style={getProgramColorBorder(program)}>
      <CardBody>
        <div className="d-flex justify-content-between">
          <CardTitle>
            {program.isCancelled && (
              <span className="text-danger fw-bold me-2">
                ❌ {t.attributes.cancelled.title}:
              </span>
            )}
            <CardLink
              as={Link}
              href={`/${event.slug}/programs/${program.slug}`}
              className="link-subtle"
            >
              {program.title}
            </CardLink>
          </CardTitle>
          {isLoggedIn && <FavoriteButton scheduleItem={scheduleItem} />}
        </div>
        <div className="d-flex justify-content-between">
          <ScheduleItem
            event={event}
            scheduleItem={scheduleItem}
            locale={locale}
          />
        </div>
      </CardBody>
    </Card>
  );
}
