import { MessageCard } from "@con2/components";
import { getLocale } from "next-intl/server";

import { getTranslations } from "@/translations";

// Rendered into every flight payload regardless of whether a 403 actually happens
// (see create-component-tree.js in Next's app-router internals), so this must stay
// cheap: no auth(), no GraphQL, no DB.
export default async function Forbidden() {
  const locale = await getLocale();
  const t = getTranslations(locale).PermissionDenied;

  return <MessageCard container title={t.title} message={t.message} />;
}
