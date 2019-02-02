import React from 'react';

import Col from 'reactstrap/lib/Col';
import Form from 'reactstrap/lib/Form';
import FormGroup from 'reactstrap/lib/FormGroup';
import FormText from 'reactstrap/lib/FormText';
import Input from 'reactstrap/lib/Input';
import Label from 'reactstrap/lib/Label';

import { Field, Layout } from './models';


interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
  ns?: string[];
}


interface SchemaFormState { }


export default class SchemaForm extends React.PureComponent<SchemaFormProps, SchemaFormState> {
  render() {
    const { layout } = this.props;

    return (
      <Form className={layout === 'horizontal' ? 'form-horizontal' : ''}>
        {this.props.fields.map(field => <div key={field.name}>{this.renderField(field)}</div>)}
        {this.props.children}
      </Form>
    );
  }

  protected renderField(field: Field) {
    const { layout } = this.props;
    const { type, name, helpText } = field;
    const title = field.title || '';

    if (type === 'StaticText' && !title) {
      // Full-width static text
      return <p>{helpText}</p>;
    } else if (type === 'Divider') {
      return <hr/>;
    } else if (type === 'Spacer') {
      return <div className="pb-3" />;
    }

    switch (layout) {
      case 'horizontal':
        return (
          <FormGroup className="row">
            <Label for={name} className="col-md-3 col-form-label">{title}</Label>
            <Col md={9}>
              {this.renderInput(field)}
              {helpText ? <FormText>{helpText}</FormText> : null}
            </Col>
          </FormGroup>
        );
      case 'vertical':
      default:
        return (
          <FormGroup>
            <Label for={name}>{title}</Label>
            {this.renderInput(field)}
          </FormGroup>
        );
    }
  }

  protected renderInput(field: Field) {
    const readOnly = this.isReadOnly(field);

    switch (field.type) {
      case 'SingleLineText':
        return <Input name={field.name} readOnly={readOnly} />;
      case 'MultiLineText':
        return <Input name={field.name} readOnly={readOnly} type="textarea" rows={field.rows || 10} />;
      case 'StaticText':
        return <></>;
      default:
        throw new Error(`Not implemented: ${field.type}`);
    }
  }

  protected isReadOnly(field: Field) {
    return !!field.readOnly;
  }
}
