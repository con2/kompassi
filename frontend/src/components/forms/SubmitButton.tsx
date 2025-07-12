"use client";

import type { ReactNode } from "react";
import { useFormStatus } from "react-dom";

interface SubmitButtonProps {
  children?: ReactNode;
  disabled?: boolean;
  className?: string;
}

export default function SubmitButton({
  children,
  disabled,
  className = "btn btn-primary",
}: SubmitButtonProps) {
  const { pending } = useFormStatus();

  return (
    <button type="submit" className={className} disabled={disabled || pending}>
      {children}
    </button>
  );
}
