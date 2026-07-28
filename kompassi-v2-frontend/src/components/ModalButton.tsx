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
  /// When set (and no `action` is given), the modal gets a primary button with this
  /// label that just closes the modal, instead of the plain "cancel"-only close
  /// button. Use for modals whose content is a client-side widget that is already
  /// live-synced to state elsewhere (eg. an outer form via a `form` attribute) and so
  /// has no separate submit step of its own - the button just confirms "I'm done
  /// selecting", it does not discard anything on close either way.
  confirmLabel?: string;
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
  confirmLabel,
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
                  <Button
                    variant={confirmLabel ? "primary" : "outline-primary"}
                    onClick={close}
                  >
                    {confirmLabel ?? messages.cancel}
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
