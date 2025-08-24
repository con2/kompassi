"use client";

import { ReactNode, MouseEvent, useCallback, useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import type { Translations } from "@/translations/en";
import { createPortal } from "react-dom";

interface Props {
  title: string;
  label?: ReactNode;
  labelTitle?: string;
  children?: ReactNode;
  action?(formData: FormData): void;
  messages: Translations["Modal"];
  disabled?: boolean;
  className?: string;
  submitButtonVariant?: "primary" | "danger" | "success";
}

/// Renders a button that opens a modal. Pass modal contents as children
export default function ModalButton({
  title,
  label,
  labelTitle,
  children,
  action,
  messages,
  disabled,
  className = "btn btn-link p-0 link-subtle",
  submitButtonVariant = "primary",
}: Props) {
  const [isVisible, setIsVisible] = useState(false);
  const close = useCallback(() => {
    setIsVisible(false);
  }, []);
  const open = useCallback((_event: MouseEvent<HTMLButtonElement>) => {
    setIsVisible(true);
  }, []);

  /// TODO Change manual button to React Bootstrap one.
  /// Add a tooltip to the button if it is disabled to tell us why.
  return (
    <>
      <button
        type="button"
        className={className}
        onClick={open}
        title={labelTitle ?? title}
        disabled={disabled}
      >
        {label ?? `${title}…`}
      </button>
      {!disabled &&
        typeof document !== "undefined" &&
        createPortal(
          <Modal show={isVisible} onHide={close} size="lg">
            <Modal.Header closeButton>
              <Modal.Title>{title}</Modal.Title>
            </Modal.Header>

            {action ? (
              <form action={action} onSubmit={close}>
                <Modal.Body>{children}</Modal.Body>

                <Modal.Footer>
                  <Button variant="outline-secondary" onClick={close}>
                    {messages.cancel}
                  </Button>
                  <Button variant={submitButtonVariant} type="submit">
                    {messages.submit}
                  </Button>
                </Modal.Footer>
              </form>
            ) : (
              <>
                <Modal.Body>{children}</Modal.Body>
                <Modal.Footer>
                  <Button variant="outline-primary" onClick={close}>
                    {messages.cancel}
                  </Button>
                </Modal.Footer>
              </>
            )}
          </Modal>,
          document.body,
        )}
    </>
  );
}
