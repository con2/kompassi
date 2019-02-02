import React from 'react';
import { NamespacesConsumer } from 'react-i18next';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import FormGroup from 'reactstrap/lib/FormGroup';

import { FormEditorAction } from '../FormEditorView';
import { BaseSchemaForm } from '../SchemaForm';
import { Field } from '../SchemaForm/models';
import './index.css';


interface FormEditorOwnProps {
  onAction(action: FormEditorAction, fieldName: string): void;
}


export default class FormEditor extends BaseSchemaForm<FormEditorOwnProps> {
  protected Action = ({ action, color, children, fieldName, disabled }: {
    action: FormEditorAction,
    color: string,
    children: React.ReactNode,
    fieldName: string,
    disabled?: boolean,
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
  )

  protected renderField(field: Field) {
    const { name } = field;

    return (
      <NamespacesConsumer key={name} ns={['FormEditor']}>
        {t => (
          <div className="FormEditor-field">
            <div className="FormEditor-background">
              <FormGroup>
                <ButtonGroup className="mr-2">
                  <this.Action action="addFieldAbove" color="primary" fieldName={name}>{t('addFieldAbove')}…</this.Action>
                </ButtonGroup>
                <ButtonGroup className="mr-2">
                  <this.Action
                    action="moveUp"
                    color="secondary"
                    fieldName={name}
                    disabled={!this.canMoveUp(name)}
                  >
                    {t('moveUp')}…
                  </this.Action>
                  <this.Action
                    action="moveDown"
                    color="secondary"
                    fieldName={name}
                    disabled={!this.canMoveDown(name)}
                  >
                    {t('moveDown')}…
                  </this.Action>
                </ButtonGroup>
                <ButtonGroup>
                  <this.Action action="editField" color="secondary" fieldName={name}>{t('editField')}…</this.Action>
                  <this.Action action="removeField" color="danger" fieldName={name}>{t('removeField')}…</this.Action>
                </ButtonGroup>
              </FormGroup>
              {super.renderField(field)}
            </div>
          </div>
        )}
      </NamespacesConsumer>
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
