import * as React from 'react';
import { NamespacesConsumer } from 'react-i18next';
import { RouteComponentProps } from 'react-router';

import Button from 'reactstrap/lib/Button';
import Form from 'reactstrap/lib/Form';
import FormGroup from 'reactstrap/lib/FormGroup';
import Input from 'reactstrap/lib/Input';
import Nav from 'reactstrap/lib/Nav';
import NavItem from 'reactstrap/lib/NavItem';
import NavLink from 'reactstrap/lib/NavLink';

import FormEditor from './FormEditor';
import MainViewContainer from './MainViewContainer';
import SchemaForm from './SchemaForm';
import { Field, Layout } from './SchemaForm/models';


type Tab = 'design' | 'preview';
const tabs: Tab[] = ['design', 'preview'];


interface FormViewRouterProps {
  formSlug: string;
}

interface FormViewState {
  title?: string;
  fields: Field[];
  layout: Layout;

  activeTab: Tab;
}


export default class FormEditorView extends React.Component<RouteComponentProps<FormViewRouterProps>, FormViewState> {
  state: FormViewState = {
    title: 'Dynaamine lomake höhöhö',
    fields: [
      {
        type: 'SingleLineText',
        name: 'singleLine',
        title: 'Single line text',
      },
      {
        type: 'MultiLineText',
        name: 'multiLine',
        title: 'Multi line text',
      },
      {
        type: 'Divider',
        name: 'divider1',
      },
      {
        type: 'StaticText',
        name: 'staticFullWidth',
        helpText: 'Full-width static text.',
      },
      {
        type: 'StaticText',
        name: 'staticWithTitle',
        title: 'Static text with title',
        helpText: 'I am a llama.',
      },
    ],
    layout: 'horizontal',
    activeTab: 'design',
  };

  render() {
    const { title, fields, activeTab, layout } = this.state;

    return (
      <NamespacesConsumer ns={['FormEditor']}>
        {t => (
          <MainViewContainer>
            <Nav tabs={true} className='mb-2'>
              {tabs.map(tab => (
                <NavItem key={tab}>
                  <NavLink
                    href='#'
                    onClick={() => this.setState({ activeTab: tab })}
                    active={this.state.activeTab === tab}
                  >
                    {t(tab)}
                  </NavLink>
                </NavItem>
              ))}
            </Nav>

            {activeTab === 'design' ? (
              <>
                <Form>
                  <FormGroup>
                    <Input bsSize="lg" name="title" placeholder="Form title" value={title} onChange={this.onTitleChange} />
                  </FormGroup>
                </Form>

                <FormEditor fields={fields} layout="horizontal">
                  <Button outline={true} color="primary" size="sm">{t('addField')}…</Button>
                </FormEditor>
              </>
            ) : (
              <>
                {title ? <h2>{title}</h2> : null}
                <SchemaForm fields={fields} layout={layout} />
              </>
            )}
          </MainViewContainer>
        )}
      </NamespacesConsumer>
    );
  }

  onTitleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const title = event.target.value;
    this.setState({ title });
  }
}
