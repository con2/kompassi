import React from 'react';
import { FormGroup, Label, Col, FormText } from 'reactstrap';

interface HorizontalFieldProps {
  name: string;
  title: string;
  required?: boolean;
  helpText?: string;
}

const HorizontalField: React.FC<HorizontalFieldProps> = ({ name, title, helpText, required, children }) => {
  const className = required ? 'col-md-3 col-form-label font-weight-bold' : 'col-md-3 col-form-label';

  return (
    <FormGroup className="row">
      <Label for={name} className={className}>
        {title}
      </Label>
      <Col md={9}>
        {children}
        {helpText ? <FormText>{helpText}</FormText> : null}
      </Col>
    </FormGroup>
  );
};

export default HorizontalField;
