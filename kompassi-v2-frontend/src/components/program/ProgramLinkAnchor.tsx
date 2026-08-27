import Link from "next/link";

import { ProgramLinkType } from "@/__generated__/graphql";
import { publicUrl } from "@/config";

function getLinkEmoji(type: ProgramLinkType) {
  switch (type) {
    case ProgramLinkType.Calendar:
      return "📅";
    case ProgramLinkType.Signup:
      return "✍️";
    case ProgramLinkType.Feedback:
      return "📝";
    case ProgramLinkType.Recording:
      return "🎥";
    case ProgramLinkType.Remote:
      return "🌐";
    case ProgramLinkType.Reservation:
    case ProgramLinkType.Tickets:
      return "🎟️";
    case ProgramLinkType.Other:
    default:
      return "🔗";
  }
}

interface ProgramLinkFields {
  type: ProgramLinkType;
  href: string;
  title: string;
}

/// Renders a single program/schedule item link, internal links via next/link.
export default function ProgramLinkAnchor({
  link,
}: {
  link: ProgramLinkFields;
}) {
  const label = `${getLinkEmoji(link.type)} ${link.title}…`;
  return link.href.startsWith(publicUrl) ? (
    <Link href={link.href.slice(publicUrl.length)} className="link-subtle">
      {label}
    </Link>
  ) : (
    <a
      href={link.href}
      target="_blank"
      rel="noopener noreferrer"
      className="link-subtle"
    >
      {label}
    </a>
  );
}
