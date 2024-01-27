"use client";

import { useRouter } from "next/navigation";
import { ReactNode, useCallback } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import type { Translations } from "@/translations/en";

interface Props {
  title: ReactNode;
  children?: ReactNode;
  action?(formData: FormData): void;
  messages: Translations["Modal"];
}

// TODO make server component, split Modal stuff to separate client component
// client component calling getTranslations includes whole set of translations in bundle
export default function InterceptingRouteModal({
  title,
  children,
  action,
  messages,
}: Props) {
  const router = useRouter();
  const handleClose = useCallback(() => {
    router.back();
  }, [router]);

  return (
    <Modal show onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>

      <form action={action}>
        <Modal.Body>{children}</Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            {messages.cancel}
          </Button>
          <Button variant="primary" type="submit">
            {messages.submit}
          </Button>
        </Modal.Footer>
      </form>
    </Modal>
  );
}
