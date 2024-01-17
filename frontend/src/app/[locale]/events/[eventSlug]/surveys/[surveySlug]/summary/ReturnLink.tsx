"use client";

import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";

interface Props {
  messages: {
    returnToResponseList: string;
    returnToSurveyList: string;
  };
}

export function ReturnLink({ messages }: Props) {
  const searchParams = useSearchParams();
  const params = useParams();
  const comeFrom = searchParams.get("from");
  const { eventSlug, surveySlug } = params;

  let message: string;
  let href: string;

  if (comeFrom === "responses") {
    message = messages.returnToResponseList;
    href = `/events/${eventSlug}/surveys/${surveySlug}/responses`;
  } else if (comeFrom === "surveys") {
    href = `/events/${eventSlug}/surveys`;
    message = messages.returnToSurveyList;
  } else {
    // TODO: when we have single survey admin view, default to that
    return <></>;
  }

  return (
    <Link className="link-subtle" href={href}>
      &lt; {message}
    </Link>
  );
}
