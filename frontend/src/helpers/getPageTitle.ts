import { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  event?: { name: string } | null | undefined;
  subject?: string | null | undefined;
  viewTitle?: string | null | undefined;
}

export default function getPageTitle(props: Props) {
  const { translations, event, subject, viewTitle } = props;
  const parts = [];

  if (event) {
    parts.push(event.name + ":");
  }

  if (subject) {
    parts.push(subject);

    if (viewTitle) {
      parts.push(`(${viewTitle})`);
    }
  } else if (viewTitle) {
    parts.push(viewTitle);
  }

  if (parts.length > 0) {
    parts.push("–");
  }

  parts.push(translations.Brand.plainAppName);

  return parts.join(" ");
}
