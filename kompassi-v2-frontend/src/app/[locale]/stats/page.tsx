import { ViewContainer, ViewHeading } from "@con2/components";

import { graphql } from "@/__generated__";
import { ReportFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import Report from "@/components/reports/Report";
import { timezone as defaultTimezone } from "@/config";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query StatsPage($locale: String) {
    kompassiStats(lang: $locale) {
      ...Report
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale } = params;
  const translations = getTranslations(locale);

  return {
    title: getPageTitle({
      translations,
      viewTitle: translations.StatsView.title,
    }),
  };
}

export const revalidate = 0;

export default async function StatsPage(props: Props) {
  const params = await props.params;
  const { locale } = params;
  const translations = getTranslations(locale);

  const { data } = await getClient().query({
    query,
    variables: { locale },
  });

  const reports = data.kompassiStats as ReportFragment[];

  return (
    <ViewContainer>
      <ViewHeading>{translations.StatsView.title}</ViewHeading>
      {reports.map((report) => (
        <Report
          key={report.slug}
          report={report}
          timezone={defaultTimezone}
          locale={locale}
        />
      ))}
    </ViewContainer>
  );
}
