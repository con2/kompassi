import React from 'react';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import FormGroup from 'reactstrap/lib/FormGroup';

import { FormEditorAction } from '../FormEditorView';
import { BaseSchemaForm } from '../SchemaForm';
import { Field } from '../SchemaForm/models';
import { T } from '../../../translations';

import './index.css';

interface FormEditorOwnProps {
  onAction(action: FormEditorAction, fieldName: string): void;
}

interface ActionProps extends FormEditorOwnProps {
  action: FormEditorAction;
  color: string;
  children: React.ReactNode;
  fieldName: string;
  disabled?: boolean;
}

const Action: React.FC<ActionProps> = ({ action, color, children, fieldName, disabled, onAction }) => (
  <Button key={action} outline={true} color={color} size="sm" disabled={!!disabled} onClick={() => onAction(action, fieldName)}>
    {children}
  </Button>
);

export default class FormEditor extends BaseSchemaForm<FormEditorOwnProps> {
  protected renderField(field: Field) {
    const { onAction } = this.props;
    const { name } = field;
    const t = T(r => r.FormEditor);

    return (
      <div className="FormEditor-field">
        <div className="FormEditor-background">
          <FormGroup>
            <ButtonGroup className="mr-2">
              <Action onAction={onAction} action="addFieldAbove" color="primary" fieldName={name}>
                {t(r => r.addFieldAbove)}…
              </Action>
            </ButtonGroup>
            <ButtonGroup className="mr-2">
              <Action onAction={onAction} action="moveUp" color="secondary" fieldName={name} disabled={!this.canMoveUp(name)}>
                {t(r => r.moveUp)}…
              </Action>
              <Action onAction={onAction} action="moveDown" color="secondary" fieldName={name} disabled={!this.canMoveDown(name)}>
                {t(r => r.moveDown)}…
              </Action>
            </ButtonGroup>
            <ButtonGroup>
              <Action onAction={onAction} action="editField" color="secondary" fieldName={name}>
                {t(r => r.editField)}…
              </Action>
              <Action onAction={onAction} action="removeField" color="danger" fieldName={name}>
                {t(r => r.removeField)}…
              </Action>
            </ButtonGroup>
          </FormGroup>
          {super.renderField(field)}
        </div>
      </div>
    );
  }

  protected isReadOnly(field: Field) {
    return true;
  }

  protected canMoveDown(fieldName: string) {
    const { fields } = this.props;
    return fieldName !== fields[fields.length - 1].name;
  }

  protected canMoveUp(fieldName: string) {
    const { fields } = this.props;
    return fieldName !== fields[0].name;
  }
}
