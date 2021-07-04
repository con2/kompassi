import React from "react";

import Button from "react-bootstrap/Button";
import BsModal from "react-bootstrap/Modal";
import { T } from "../../translations";

type Resolve = (result: boolean) => void;

interface ModalProps {
  title?: React.ReactNode;
  okLabel?: React.ReactNode;
  cancelLabel?: React.ReactNode;
  isOpen: boolean;
  open(): void;
  ok(): void;
  cancel(): void;
  execute(): Promise<boolean>;
  children?: React.ReactNode;

  // INTERNAL STATE, NICHT GEFINGERPOKEN BEI DUMMKOPFEN
  resolve: Resolve | null;
}

export function useModal(defaults?: Partial<ModalProps>): ModalProps {
  const [isOpen, setOpen] = React.useState(false);
  const [resolve, setResolve] = React.useState<Resolve | null>(null);

  const close = (ok = false) => {
    if (resolve) {
      resolve(ok);
      setResolve(null);
    }
    setOpen(false);
  };

  const open = () => {
    setOpen(true);
  };

  return {
    ...defaults,
    isOpen,
    resolve,
    open,
    ok() {
      close(true);
    },
    cancel() {
      close(false);
    },
    async execute(): Promise<boolean> {
      if (isOpen) {
        throw new Error("Modal.execute called while already open");
      }

      open();

      return new Promise<boolean>((_resolve) => {
        // Extra layer of callable because if useState.set argument is a callable,
        // React will call it with the current value :))) FUCKING REACT MAGIC
        setResolve(() => _resolve);
      });
    },
  };
}

export function Modal(props: ModalProps) {
  const { title, isOpen, ok, cancel, children } = props;
  const t = T((r) => r.Common);
  const okLabel = props.okLabel ?? t((r) => r.ok);
  const cancelLabel = props.cancelLabel ?? t((r) => r.cancel);

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
