"use client";

import { ComponentPropsWithoutRef, useCallback, useMemo, useRef } from "react";
import { useFormStatus } from "react-dom";

/// A form that submits automatically on the onChange event.
export default function AutoSubmitForm(
  props: ComponentPropsWithoutRef<"form">,
) {
  const ref = useRef<HTMLFormElement>(null);
  const onChange = useCallback(() => ref.current?.requestSubmit(), [ref]);

  const { pending } = useFormStatus();
  return <form {...props} ref={ref} onChange={onChange} />;
}
