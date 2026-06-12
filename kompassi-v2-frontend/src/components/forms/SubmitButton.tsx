"use client";

import { useCallback, type ReactNode } from "react";
import { useFormStatus } from "react-dom";

interface SubmitButtonProps {
  children?: ReactNode;
  disabled?: boolean;
  className?: string;
  name?: string;
  value?: string;
  confirmationMessage?: string;
}

export default function SubmitButton({
  children,
  disabled,
  name,
  value,
  className = "btn btn-primary",
  confirmationMessage,
}: SubmitButtonProps) {
  const { pending } = useFormStatus();
  const onClick = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (confirmationMessage && !confirm(confirmationMessage)) {
        event.preventDefault();
      }
    },
    [confirmationMessage],
  );

  return (
    <button
      type="submit"
      name={name}
      value={value}
      className={className}
      disabled={disabled || pending}
      onClick={confirmationMessage ? onClick : undefined}
    >
      {pending && (
        <span
          className="spinner-border spinner-border-sm me-2"
          role="status"
          aria-hidden="true"
        />
      )}
      {children}
    </button>
  );
}
