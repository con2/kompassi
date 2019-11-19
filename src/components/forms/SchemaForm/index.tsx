import React, { FormEvent, ChangeEvent } from 'react';

import Col from 'reactstrap/lib/Col';
import Form from 'reactstrap/lib/Form';
import FormGroup from 'reactstrap/lib/FormGroup';
import FormText from 'reactstrap/lib/FormText';
import Input from 'reactstrap/lib/Input';
import Label from 'reactstrap/lib/Label';

import { Field, Layout } from './models';
import HorizontalField from '../HorizontalField';

interface SchemaFormProps {
  fields: Field[];
  layout?: Layout;
  ns?: string[];

  // TODO Stricter typings
  /* eslint-disable @typescript-eslint/no-explicit-any */
  value?: any;
  onChange?(values: any): void;
  onSubmit?(values: any): void;
  /* eslint-enable @typescript-eslint/no-explicit-any */
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

    switch (type) {
      case 'SingleCheckbox':
        return (
          <FormGroup check={true}>
            <Label check={true} className={required ? 'font-weight-bold' : ''}>
              {this.renderInput(field, fieldValue)} {title}
              <FormText>{helpText}</FormText>
            </Label>
          </FormGroup>
        );
      default:
        switch (layout) {
          case 'horizontal':
            return (
              <HorizontalField name={name} title={title} helpText={helpText} required={required}>
                {this.renderInput(field, fieldValue)}
              </HorizontalField>
            );
          case 'vertical':
          default:
            return (
              <FormGroup>
                <Label for={name} className={required ? 'font-weight-bold' : ''}>
                  {title}
                </Label>
                {this.renderInput(field, fieldValue)}
                <FormText>{helpText}</FormText>
              </FormGroup>
            );
        }
    }
  }

  protected renderInput(field: Field, value: any) {
    const readOnly = this.isReadOnly(field);

    switch (field.type) {
      case 'SingleLineText':
        return <Input id={field.name} name={field.name} readOnly={readOnly} onChange={this.handleTextFieldChange} value={value} />;
      case 'MultiLineText':
        return (
          <Input
            type="textarea"
            id={field.name}
            name={field.name}
            readOnly={readOnly}
            onChange={this.handleTextFieldChange}
            rows={field.rows || 10}
            value={value}
          />
        );
      case 'SingleCheckbox':
        return (
          <Input
            type="checkbox"
            id={field.name}
            name={field.name}
            disabled={readOnly}
            onChange={this.handleCheckboxChange}
            value={value}
          />
        );
      case 'StaticText':
        return <></>;
      default:
        throw new Error(`Not implemented: ${field.type}`);
    }
  }

  protected handleTextFieldChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value: fieldValue } = event.currentTarget;
    const { value, onChange } = this.props;

    const newValue = Object.assign({}, value, { [name]: fieldValue });

    if (onChange) {
      onChange(newValue);
    }
  };

  protected handleCheckboxChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name } = event.currentTarget;
    const checked: boolean = event.currentTarget.checked;
    const { value, onChange } = this.props;

    const newValue = Object.assign({}, value, { [name]: checked });

    if (onChange) {
      onChange(newValue);
    }
  };

  protected handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    const { onSubmit, value } = this.props;
    if (onSubmit) {
      onSubmit(value);
    }
  };

  protected isReadOnly(field: Field) {
    return !!field.readOnly;
  }
}

export default class SchemaForm extends BaseSchemaForm<{}> {}
