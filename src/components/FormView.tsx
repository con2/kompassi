import React from 'react';
import { NamespacesConsumer } from 'react-i18next';
import { RouteComponentProps } from 'react-router';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';

import MainViewContainer from './MainViewContainer';
import SchemaForm from './SchemaForm';
import { Field, Layout } from './SchemaForm/models';


interface FormViewRouterProps {
  formSlug: string;
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

    return (
      // TODO wrong namespace
      <NamespacesConsumer ns={['SchemaForm']}>
        {t => (
          <MainViewContainer>
            {title ? <h1>{title}</h1> : null}
            <SchemaForm fields={fields} layout={layout}>
              <ButtonGroup className="float-md-right">
                <Button color="primary">{t('submit')}</Button>
              </ButtonGroup>
            </SchemaForm>
          </MainViewContainer>
        )}
      </NamespacesConsumer>
    );
  }
}
