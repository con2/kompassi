"use client";

import { ReactNode, useCallback, useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import type { Translations } from "@/translations/en";

interface Props {
  title: string;
  label?: ReactNode;
  children?: ReactNode;
  action?(formData: FormData): void;
  messages: Translations["Modal"];
  className?: string;
}

/// Renders a button that opens a modal. Pass modal contents as children
export default function ModalButton({
  title,
  label,
  children,
  action,
  messages,
  className = "btn btn-link p-0 link-subtle",
}: Props) {
  const [isVisible, setIsVisible] = useState(false);
  const close = useCallback(() => {
    setIsVisible(false);
  }, []);

  return (
    <>
      <button
        className={className}
        onClick={() => setIsVisible(true)}
        title={label ? title : undefined}
      >
        {label ?? `${title}…`}
      </button>
      <Modal show={isVisible} onHide={close}>
        <Modal.Header closeButton>
          <Modal.Title>{title}</Modal.Title>
        </Modal.Header>

        <form action={action} onSubmit={close}>
          <Modal.Body>{children}</Modal.Body>

          <Modal.Footer>
            <Button variant="secondary" onClick={close}>
              {messages.cancel}
            </Button>
            <Button variant="primary" type="submit">
              {messages.submit}
            </Button>
          </Modal.Footer>
        </form>
      </Modal>
    </>
  );
}
