"use client";

import { ComponentPropsWithoutRef, useCallback, useRef } from "react";

/// A form that submits automatically on the onChange event.
export default function AutoSubmitForm(
  props: ComponentPropsWithoutRef<"form">,
) {
  const ref = useRef<HTMLFormElement>(null);
  const onChange = useCallback(() => void ref.current?.requestSubmit(), [ref]);

  return <form {...props} ref={ref} onChange={onChange} />;
}
