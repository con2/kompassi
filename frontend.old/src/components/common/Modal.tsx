import React from "react";

import Button from "react-bootstrap/Button";
import BsModal from "react-bootstrap/Modal";
import { T } from "../../translations";

type Callback = () => void | boolean;

interface ModalProps {
  // User settable props
  title?: React.ReactNode;
  okLabel?: React.ReactNode;
  cancelLabel?: React.ReactNode;

  // called on OK before close
  onSubmit?: Callback;

  // called on OK and cancel (after submit() on OK)
  // if submit and close disagree on whether to close or not, result is undefined :)
  onClose?: Callback;

  children?: React.ReactNode;

  // Public API usable from both inside and outside this component
  open(): void;
  submit(): void;
  close(): void;

  // Read only public state (pass isOpen: true to useModal if you want it to be open from the go)
  isOpen: boolean;

  // XXX Hack: Internal state (no touch!)
  onSubmitRef: React.MutableRefObject<Callback | null>;
  onCloseRef: React.MutableRefObject<Callback | null>;
}

/** This hook manages the state required to run a Modal. */
export function useModal({
  isOpen: isInitiallyOpen,
}: {
  isOpen?: boolean;
} = {}): ModalProps {
  const [isOpen, setOpen] = React.useState(isInitiallyOpen ?? false);
  const onSubmitRef = React.useRef<Callback | null>(null);
  const onCloseRef = React.useRef<Callback | null>(null);

  const submit = () => {
    if (!isOpen) {
      return;
    }

    if (onSubmitRef.current) {
      if (onSubmitRef.current() === false) {
        return;
      }
    }

    close();
  };

  const close = () => {
    if (!isOpen) {
      return;
    }

    if (onCloseRef.current) {
      if (onCloseRef.current() === false) {
        return;
      }
    }

    setOpen(false);
  };

  const open = () => {
    setOpen(true);
  };

  return {
    isOpen,
    open,
    submit,
    close,

    onSubmitRef,
    onCloseRef,
  };
}

/**
 * A modal dialog managed by the `useModal` hook.
 * Always instantiate as `const modal = useModal(); <Modal {...modal}>`
 * possibly setting other props listed under "user settable props" in `ModalProps`.
 */
export function Modal(props: ModalProps) {
  const {
    title,
    isOpen,
    submit: ok,
    close: hide,
    children,
    onSubmitRef,
    onSubmit,
    onCloseRef,
    onClose,
  } = props;
  const t = T((r) => r.Common);
  const okLabel = props.okLabel ?? t((r) => r.ok);
  const cancelLabel = props.cancelLabel ?? t((r) => r.cancel);

  // XXX Hack
  onSubmitRef.current = onSubmit ?? null;
  onCloseRef.current = onClose ?? null;

  return (
    <BsModal show={isOpen} onHide={hide}>
      {title && (
        <BsModal.Header closeButton>
          <BsModal.Title>{title}</BsModal.Title>
        </BsModal.Header>
      )}
      <BsModal.Body>{children}</BsModal.Body>
      <BsModal.Footer>
        <Button variant="secondary" onClick={hide}>
          {cancelLabel}
        </Button>
        <Button variant="primary" onClick={ok}>
          {okLabel}
        </Button>
      </BsModal.Footer>
    </BsModal>
  );
}
