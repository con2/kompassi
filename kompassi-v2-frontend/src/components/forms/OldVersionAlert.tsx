import Link from "next/link";
import { Alert } from "react-bootstrap";
import { ResponseRevisionFragment } from "@/__generated__/graphql";
import { auth } from "@/auth";
import type { Translations } from "@/translations/en";

interface Props {
  basePath: string;
  supersededBy: ResponseRevisionFragment;
  messages: Translations["Survey"]["OldVersionAlert"];
  className?: string;
}

export async function OldVersionAlert({
  basePath,
  supersededBy,
  messages: t,
  className = "",
}: Props) {
  const session = await auth();

  return (
    <Alert variant="warning" className={className}>
      <h5>{t.title}</h5>
      <p>{t.message}</p>
      <Link className="link-subtle" href={`${basePath}/${supersededBy.id}`}>
        {t.actions.returnToCurrentVersion}
      </Link>
    </Alert>
  );
}
