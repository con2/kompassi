export type FieldType = 'SingleLineText' | 'MultiLineText' | 'Divider' | 'StaticText' | 'Spacer';


interface BaseField {
  type: FieldType;
  name: string;
  title?: string;
  helpText?: string;
  required?: boolean;
  readOnly?: boolean;
}


export interface SingleLineText extends BaseField {
  type: 'SingleLineText';
}


export interface MultiLineText extends BaseField {
  type: 'MultiLineText';
  rows?: number;
}


export interface Divider extends BaseField {
  type: 'Divider';
}

export interface Spacer extends BaseField {
  type: 'Spacer';
}


export interface StaticText extends BaseField {
  type: 'StaticText';
}


export interface SingleLineText extends BaseField {
  type: 'SingleLineText';
}

export type Field = SingleLineText | MultiLineText | Divider | Spacer | StaticText;

export type Layout = 'horizontal' | 'vertical'; // TODO: inline
