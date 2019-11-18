import React, { FormEvent, ChangeEvent } from 'react';

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

  // TODO Stricter typings
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  value?: any;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onChange?(values: any): void;
}

export class BaseSchemaForm<OwnProps> extends React.PureComponent<SchemaFormProps & OwnProps, {}> {
  render() {
    const { layout, fields, children } = this.props;

    return (
      <Form className={layout === 'horizontal' ? 'form-horizontal' : ''}>
        {fields.map(field => (
          <div key={field.name}>{this.renderField(field)}</div>
        ))}
        {children}
      </Form>
    );
  }

  protected renderField(field: Field) {
    const { layout, value } = this.props;
    const { type, name, helpText, required } = field;
    const title = field.title || '';
    const fieldValue = value ? value[field.name] || '' : '';

    if (type === 'StaticText' && !title) {
      // Full-width static text
      return <p>{helpText}</p>;
    } else if (type === 'Divider') {
      return <hr />;
    } else if (type === 'Spacer') {
      return <div className="pb-3" />;
    }

    switch (layout) {
      case 'horizontal':
        const className = required ? 'col-md-3 col-form-label font-weight-bold' : 'col-md-3 col-form-label';
        return (
          <FormGroup className="row">
            <Label for={name} className={className}>
              {title}
            </Label>
            <Col md={9}>
              {this.renderInput(field, fieldValue)}
              {helpText ? <FormText>{helpText}</FormText> : null}
            </Col>
          </FormGroup>
        );
      case 'vertical':
      default:
        return (
          <FormGroup>
            <Label for={name} className={required ? 'font-weight-bold' : ''}>
              {title}
            </Label>
            {this.renderInput(field, fieldValue)}
          </FormGroup>
        );
    }
  }

  protected renderInput(field: Field, value: string) {
    const readOnly = this.isReadOnly(field);

    switch (field.type) {
      case 'SingleLineText':
        return <Input id={field.name} name={field.name} readOnly={readOnly} onChange={this.handleChange} value={value} />;
      case 'MultiLineText':
        return (
          <Input
            id={field.name}
            name={field.name}
            readOnly={readOnly}
            onChange={this.handleChange}
            type="textarea"
            rows={field.rows || 10}
            value={value}
          />
        );
      case 'StaticText':
        return <></>;
      default:
        throw new Error(`Not implemented: ${field.type}`);
    }
  }

  protected handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const name = event.currentTarget.name;
    const fieldValue = event.currentTarget.value;

    const value = Object.assign({}, this.props.value, { [name]: fieldValue });

    if (this.props.onChange) {
      this.props.onChange(value);
    }
  };

  protected isReadOnly(field: Field) {
    return !!field.readOnly;
  }
}

export default class SchemaForm extends BaseSchemaForm<{}> {}
