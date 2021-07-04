import React from "react";

import Button from "react-bootstrap/Button";
import BsModal from "react-bootstrap/Modal";
import { T } from "../../translations";

type OnClose = (ok: boolean) => void;

interface ModalProps {
  // User settable props
  title?: React.ReactNode;
  okLabel?: React.ReactNode;
  cancelLabel?: React.ReactNode;
  onClose?: OnClose;
  children?: React.ReactNode;

  // Public API usable from both inside and outside this component
  open(): void;
  ok(): void;
  cancel(): void;

  // Read only public state
  isOpen: boolean;

  // XXX Hack: Internal state (no touch!)
  onCloseRef: React.MutableRefObject<OnClose | null>;
}

export function useModal(): ModalProps {
  const [isOpen, setOpen] = React.useState(false);
  const onCloseRef = React.useRef<OnClose | null>(null);

  const close = (ok = false) => {
    setOpen(false);
    if (onCloseRef.current) {
      onCloseRef.current(ok);
    }
  };

  const open = () => {
    setOpen(true);
  };

  return {
    isOpen,
    open,
    ok() {
      close(true);
    },
    cancel() {
      close(false);
    },

    onCloseRef,
  };
}

/**
 * A modal dialog managed by the `useModal` hook.
 * Always instantiate as `const modal = useModal(); <Modal {...modal}>`
 * possibly setting other props listed under "user settable props" in `ModalProps`.
 */
export function Modal(props: ModalProps) {
  const { title, isOpen, ok, cancel, children, onCloseRef, onClose } = props;
  const t = T((r) => r.Common);
  const okLabel = props.okLabel ?? t((r) => r.ok);
  const cancelLabel = props.cancelLabel ?? t((r) => r.cancel);

  // XXX Hack
  onCloseRef.current = onClose ?? null;

  return (
    <BsModal show={isOpen} onHide={cancel}>
      {title && (
        <BsModal.Header closeButton>
          <BsModal.Title>{title}</BsModal.Title>
        </BsModal.Header>
      )}
      <BsModal.Body>{children}</BsModal.Body>
      <BsModal.Footer>
        <Button variant="secondary" onClick={cancel}>
          {cancelLabel}
        </Button>
        <Button variant="primary" onClick={ok}>
          {okLabel}
        </Button>
      </BsModal.Footer>
    </BsModal>
  );
}
