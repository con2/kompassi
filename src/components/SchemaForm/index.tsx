import React from 'react';
import { NamespacesConsumer } from 'react-i18next';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import Col from 'reactstrap/lib/Col';
import Form from 'reactstrap/lib/Form';
import FormGroup from 'reactstrap/lib/FormGroup';
import Input from 'reactstrap/lib/Input';
import Label from 'reactstrap/lib/Label';

import { Field, FieldType } from './models';


interface SchemaFormProps {
  fields: Field[];
  layout?: 'vertical' | 'horizontal';
  ns?: string[];
}


interface SchemaFormState { }


export default class SchemaForm extends React.PureComponent<SchemaFormProps, SchemaFormState> {
  static defaultNamespace = 'SchemaForm';

  render() {
    const { layout } = this.props;
    const ns = (this.props.ns || []).concat(['SchemaForm']);

    return (
      <NamespacesConsumer ns={ns}>
        {t => (
          <Form className={layout === 'horizontal' ? 'form-horizontal' : ''}>
            {this.props.fields.map(this.renderField)}

            <ButtonGroup className="float-md-right">
              <Button color="primary">{t('submit')}</Button>
            </ButtonGroup>
          </Form>
        )}
      </NamespacesConsumer>
    );
  }

  renderField = (field: Field) => {
    const { layout } = this.props;
    const { name, title, helpText } = field;

    switch (layout) {
      case 'horizontal':
        return (
          <FormGroup key={name} className="row">
            <Label for={name} className="col-md-3 col-form-label">{title}</Label>
            <Col md={9}>{this.renderInput(field)}</Col>
          </FormGroup>
        );
      case 'vertical':
      default:
        return (
          <FormGroup key={name} className="row">
            <Label for={name}>{title}</Label>
            {this.renderInput(field)}
          </FormGroup>
        );
    }
  }

  renderInput = (field: Field) => {
    switch (field.type) {
      case 'Input':
        return <Input name={field.name} />;
      case 'TextArea':
        return <Input type="textarea" name={field.name} rows={field.rows || 10} />;
    }
  }
}
