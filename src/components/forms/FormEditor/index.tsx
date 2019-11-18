import React from 'react';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import FormGroup from 'reactstrap/lib/FormGroup';

import { FormEditorAction } from '../FormEditorView';
import { BaseSchemaForm } from '../SchemaForm';
import { Field, FieldType } from '../SchemaForm/models';
import { T } from '../../../translations';

import './index.css';

interface FormEditorOwnProps {
  onAction(action: FormEditorAction, fieldName: string): void;
}

export default class FormEditor extends BaseSchemaForm<FormEditorOwnProps> {
  protected Action = ({
    action,
    color,
    children,
    fieldName,
    disabled,
  }: {
    action: FormEditorAction;
    color: string;
    children: React.ReactNode;
    fieldName: string;
    disabled?: boolean;
  }) => (
    <Button
      key={action}
      outline={true}
      color={color}
      size="sm"
      disabled={!!disabled}
      onClick={() => this.props.onAction(action, fieldName)}
    >
      {children}
    </Button>
  );

  protected renderField(field: Field) {
    const { name } = field;
    const t = T(r => r.FormEditor);

    return (
      <div className="FormEditor-field">
        <div className="FormEditor-background">
          <FormGroup>
            <ButtonGroup className="mr-2">
              <this.Action action="addFieldAbove" color="primary" fieldName={name}>
                {t(r => r.addFieldAbove)}…
              </this.Action>
            </ButtonGroup>
            <ButtonGroup className="mr-2">
              <this.Action action="moveUp" color="secondary" fieldName={name} disabled={!this.canMoveUp(name)}>
                {t(r => r.moveUp)}…
              </this.Action>
              <this.Action action="moveDown" color="secondary" fieldName={name} disabled={!this.canMoveDown(name)}>
                {t(r => r.moveDown)}…
              </this.Action>
            </ButtonGroup>
            <ButtonGroup>
              <this.Action action="editField" color="secondary" fieldName={name}>
                {t(r => r.editField)}…
              </this.Action>
              <this.Action action="removeField" color="danger" fieldName={name}>
                {t(r => r.removeField)}…
              </this.Action>
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
