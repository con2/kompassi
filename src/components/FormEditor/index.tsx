import React from 'react';
import { NamespacesConsumer } from 'react-i18next';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import FormGroup from 'reactstrap/lib/FormGroup';

import SchemaForm from '../SchemaForm';
import { Field } from '../SchemaForm/models';

import './index.css';


export default class SchemaFormEditor extends SchemaForm {
  protected renderField(field: Field) {
    const { name } = field;

    return (
      <NamespacesConsumer key={name} ns={['FormEditor']}>
        {t => (
          <div className="SchemaFormEditor-field">
            <div className="SchemaFormEditor-background">
              <FormGroup>
                <ButtonGroup className="mr-2">
                  <Button outline={true} color="primary" size="sm">{t('addFieldAbove')}…</Button>
                </ButtonGroup>
                <ButtonGroup className="mr-2">
                  <Button outline={true} color="secondary" size="sm">{t('moveUp')}…</Button>
                  <Button outline={true} color="secondary" size="sm">{t('moveDown')}…</Button>
                </ButtonGroup>
                <ButtonGroup>
                  <Button outline={true} color="secondary" size="sm">{t('editField')}…</Button>
                  <Button outline={true} color="danger" size="sm">{t('removeField')}…</Button>
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
}
