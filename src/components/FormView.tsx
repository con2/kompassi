import * as React from 'react';
import { RouteComponentProps } from 'react-router';

import MainViewContainer from './MainViewContainer';
import SchemaForm from './SchemaForm';
import { Field } from './SchemaForm/models';



interface FormViewRouterProps {
  formSlug: string;
}

interface FormViewState {
  title?: string;
  introductionText?: string;
  fields: Field[];
}


export default class FormView extends React.Component<RouteComponentProps<FormViewRouterProps>, FormViewState> {
  state: FormViewState = {
    title: 'Dynaamine lomake höhöhö',
    introductionText: 'Lorem ipsum höhöhö sit amet.\n\nWith paragraphs!',
    fields: [
      {
        type: 'Input',
        name: 'foo',
        title: 'Foo',
      },
      {
        type: 'TextArea',
        name: 'bar',
        title: 'Bar',
      },
    ],
  };

  render() {
    const { title, fields, introductionText } = this.state;

    return (
      <MainViewContainer>
        {title ? <h1>{title}</h1> : null}
        {introductionText ? introductionText.split('\n\n').map((paragraph, index) => <p key={index}>{paragraph}</p>) : null}

        <SchemaForm fields={fields} layout="horizontal" />
      </MainViewContainer>
    );
  }
}
