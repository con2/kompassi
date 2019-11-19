import React from 'react';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import BsModal from 'reactstrap/lib/Modal';
import ModalBody from 'reactstrap/lib/ModalBody';
import ModalFooter from 'reactstrap/lib/ModalFooter';
import ModalHeader from 'reactstrap/lib/ModalHeader';
import { TranslationFunction, T } from '../../translations';

export interface ModalResult<PayloadType> {
  ok: boolean;
  payload?: PayloadType;
}

interface ModalProps {
  title?: string;
  footer?: React.ReactNode;
  t?: TranslationFunction<any>;
}

interface ModalState {
  isOpen: boolean;
}

export default class ManagedModal<PayloadType> extends React.PureComponent<ModalProps, ModalState> {
  state: ModalState = {
    isOpen: false,
  };

  private resolve?: (result: ModalResult<PayloadType>) => void;

  render() {
    const { isOpen } = this.state;
    const { title, footer } = this.props;
    const t = this.props.t || T(r => r.Common);

    return (
      <BsModal isOpen={isOpen} toggle={this.cancel}>
        {title ? <ModalHeader toggle={this.cancel}>{title}</ModalHeader> : null}
        <ModalBody>{this.props.children}</ModalBody>
        <ModalFooter>
          {footer || (
            <ButtonGroup className="float-right">
              <Button color="success" onClick={() => this.ok()}>
                {t(r => r.ok)}
              </Button>
              <Button color="danger" outline={true} onClick={() => this.cancel()}>
                {t(r => r.cancel)}
              </Button>
            </ButtonGroup>
          )}
        </ModalFooter>
      </BsModal>
    );
  }

  open = () => {
    return new Promise<ModalResult<PayloadType>>((resolve, reject) => {
      this.resolve = resolve;
      this.setState({ isOpen: true });
    });
  };

  ok = (payload?: PayloadType) => {
    this.setState({ isOpen: false });
    this.resolve!({ ok: true, payload });
    this.resolve = undefined;
  };

  cancel = () => {
    this.setState({ isOpen: false });
    this.resolve!({ ok: false });
    this.resolve = undefined;
  };
}
