import React from 'react';
import { RouteComponentProps } from 'react-router';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';

import MainViewContainer from '../common/MainViewContainer';

import SchemaForm from './SchemaForm';
import { Field, Layout } from './SchemaForm/models';
import { T } from '../../translations';

interface FormViewRouterProps {
  slug: string;
}

interface FormViewState {
  title?: string;
  layout: Layout;
  fields: Field[];
}

export default class FormView extends React.Component<RouteComponentProps<FormViewRouterProps>, FormViewState> {
  state: FormViewState = {
    title: 'Dynaamine lomake höhöhö',
    layout: 'horizontal',
    fields: [],
  };

  render() {
    const { title, layout, fields } = this.state;
    const t = T(r => r.Common);

    return (
      <MainViewContainer>
        {title ? <h1>{title}</h1> : null}
        <SchemaForm fields={fields} layout={layout}>
          <ButtonGroup className="float-md-right">
            <Button color="primary">{t(r => r.submit)}</Button>
          </ButtonGroup>
        </SchemaForm>
      </MainViewContainer>
    );
  }
}
