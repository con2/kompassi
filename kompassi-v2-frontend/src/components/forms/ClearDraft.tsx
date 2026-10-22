"use client";

import { useEffect } from "react";
import { clearDraft } from "./formDraft";

interface Props {
  draftKey: string;
}

/// Rendered on the page a successful submission redirects to, because the
/// submitting page cannot know whether its server action succeeded.
export default function ClearDraft({ draftKey }: Props) {
  useEffect(() => clearDraft(draftKey), [draftKey]);
  return null;
}
