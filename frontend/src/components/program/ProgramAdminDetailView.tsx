import Link from "next/link";
import { ReactNode } from "react";
import DimensionBadge from "../dimensions/DimensionBadge";
import ProgramAdminDetailTabs, {
  ProgramAdminTab,
} from "./ProgramAdminDetailTabs";
import { graphql } from "@/__generated__";
import {
  DimensionBadgeFragment,
  ProgramDimensionBadgeFragment,
} from "@/__generated__/graphql";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import type { Translations } from "@/translations/en";

graphql(`
  fragment ProgramDimensionBadge on ProgramDimensionValueType {
    dimension {
      slug
      title(lang: $locale)
    }

    value {
      slug
      title(lang: $locale)
      color
    }
  }
`);

interface Event {
  slug: string;
  name: string;
}

interface Program {
  slug: string;
  title: string;
  dimensions: ProgramDimensionBadgeFragment[];
}

interface Props {
  event: Event;
  program: Program;
  translations: Translations;
  active: ProgramAdminTab;
  children?: ReactNode;
  actions?: ReactNode;
}

export default function ProgramAdminDetailView({
  event,
  program,
  translations,
  active,
  children,
  actions,
}: Props) {
  const t = translations.Program;

  console.log(program.dimensions);
  const stateDimension = program.dimensions.find(
    (d) => d.dimension.slug === "state",
  );

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/${event.slug}/program-admin`}>
        &lt; {t.actions.returnToProgramAdminList(event.name)}
      </Link>

      <ViewHeadingActionsWrapper className="mt-2">
        <h3 className="mb-3">
          {program.title}
          <ViewHeading.Sub>{t.inEvent(event.name)}</ViewHeading.Sub>
          {stateDimension && (
            <DimensionBadge subjectDimensionValue={stateDimension} />
          )}
        </h3>
        <ViewHeadingActions>{actions}</ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <ProgramAdminDetailTabs
        eventSlug={event.slug}
        programSlug={program.slug}
        translations={translations}
        active={active}
      />

      {children}
    </ViewContainer>
  );
}
