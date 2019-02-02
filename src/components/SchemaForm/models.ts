export type FieldType = 'Input' | 'TextArea';

interface BaseField {
  type: FieldType;
  name: string;
  title: string;
  helpText?: string;
  required?: boolean;
}


export interface Input extends BaseField {
  type: 'Input';
}


export interface TextArea extends BaseField {
  type: 'TextArea';
  rows?: number;
  cols?: number;
}

export type Field = Input | TextArea;
