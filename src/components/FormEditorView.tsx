import * as React from 'react';
import { NamespacesConsumer } from 'react-i18next';
import { RouteComponentProps } from 'react-router';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import Form from 'reactstrap/lib/Form';
import FormGroup from 'reactstrap/lib/FormGroup';
import Input from 'reactstrap/lib/Input';
import ListGroup from 'reactstrap/lib/ListGroup';
import ListGroupItem from 'reactstrap/lib/ListGroupItem';
import Nav from 'reactstrap/lib/Nav';
import NavItem from 'reactstrap/lib/NavItem';
import NavLink from 'reactstrap/lib/NavLink';

import FormEditor from './FormEditor';
import MainViewContainer from './MainViewContainer';
import ManagedModal from './ManagedModal';
import SchemaForm from './SchemaForm';
import { Field, FieldType, fieldTypes, Layout } from './SchemaForm/models';


type Tab = 'design' | 'preview';
const tabs: Tab[] = ['design', 'preview'];


export type FormEditorAction = 'addFieldAbove' | 'moveUp' | 'moveDown' | 'editField' | 'removeField';


interface FormViewRouterProps {
  formSlug: string;
}

interface FormViewState {
  title?: string;
  fields: Field[];
  layout: Layout;

  activeTab: Tab;
  addingNewField: boolean;
  fieldBeingEdited: Field;
}


class AddFieldModal extends ManagedModal<FieldType> {}
class EditFieldModal extends ManagedModal<Field> {}


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
    addingNewField: false,
    fieldBeingEdited: { type: 'Divider', name: '' },
  };

  addFieldModal: AddFieldModal | null = null;
  editFieldModal: EditFieldModal | null = null;
  removeFieldModal: ManagedModal<{}> | null = null;

  render() {
    const { title, fields, activeTab, layout, addingNewField } = this.state;

    return (
      <NamespacesConsumer ns={['FormEditor', 'Common']}>
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

                <FormEditor fields={fields} layout="horizontal" onAction={this.onFormEditorAction}>
                  <Button outline={true} color="primary" size="sm" onClick={this.addField}>{t('addField')}…</Button>
                </FormEditor>
              </>
            ) : (
              <>
                {title ? <h2>{title}</h2> : null}
                <SchemaForm fields={fields} layout={layout} />
              </>
            )}

            <AddFieldModal
              title={t('addField')}
              ref={(ref) => { this.addFieldModal = ref; }}
              footer={(
                <ButtonGroup className="float-right">
                  <Button color="danger" outline={true} onClick={() => this.addFieldModal!.cancel()}>{t('Common:cancel')}</Button>
                </ButtonGroup>
              )}
            >
              <ListGroup>
                {fieldTypes.map(fieldType => (
                  <ListGroupItem
                    tag="button"
                    action={true}
                    key={fieldType}
                    onClick={() => this.addFieldModal!.ok(fieldType)}
                    style={{ cursor: 'pointer' }}
                  >
                    {t(`FieldTypes.${fieldType}`)}
                  </ListGroupItem>
                ))}
              </ListGroup>
            </AddFieldModal>

            <EditFieldModal title={addingNewField ? t('addField') : t('editField')} ref={(ref) => { this.editFieldModal = ref; }}>
              <p>Edit field</p>
            </EditFieldModal>

            <ManagedModal
              ref={ref => { this.removeFieldModal = ref; }}
              title={t('RemoveFieldModal.title')}
              footer={(
                <ButtonGroup className="float-right">
                  <Button color="danger" onClick={() => this.removeFieldModal!.ok()}>
                    {t('RemoveFieldModal.yes')}
                  </Button>
                  <Button color="secondary" outline={true} onClick={() => this.removeFieldModal!.cancel()}>
                    {t('RemoveFieldModal.no')}
                  </Button>
                </ButtonGroup>
              )}
            >
              <p>{t('RemoveFieldModal.message')}</p>
            </ManagedModal>
          </MainViewContainer>
        )}
      </NamespacesConsumer>
    );
  }

  onTitleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const title = event.target.value;
    this.setState({ title });
  }

  onFormEditorAction = (action: FormEditorAction, fieldName: string) => {
    switch(action) {
      case 'addFieldAbove':
        return this.addFieldAbove(fieldName);
      case 'removeField':
        return this.removeField(fieldName);
      case 'moveUp':
        return this.moveUp(fieldName);
      case 'moveDown':
        return this.moveDown(fieldName);
    }
  }

  protected async addFieldAbove(fieldName: string) {
    const { fields } = this.state;
    const index = fields.findIndex(field => field.name === fieldName);

    if (index < 0) {
      throw new Error(`asked to addFieldAbove nonexistent ${fieldName}`);
    }

    const result = await this.getNewField();

    if (result.ok) {
      const newFields = fields.slice(0, index)
        .concat(result.payload!)
        .concat(fields.slice(index));

      this.setState({ fields: newFields });
    }
  }

  protected addField = async () => {
    const { fields } = this.state;
    const fieldTypeSelectionResult = await this.addFieldModal!.open();

    if (!fieldTypeSelectionResult.ok) {
      return;
    }

    const newFieldEditResult = await this.editFieldModal!.open();
  }

  protected async getNewField() {
    const result = await this.addFieldModal!.open();

    if (!result.ok) {
      return { ok: false };
    }

    const newField = {
      type: result.payload!,
      name: '',
    } as Field;

    this.setState({ fieldBeingEdited: newField });

    return this.editFieldModal!.open();
  }

  protected removeField = async (fieldName: string) => {
    const { fields } = this.state;
    const index = fields.findIndex(field => field.name === fieldName);

    if (index < 0) {
      throw new Error(`asked to remove nonexistent ${fieldName}`);
    }

    const result = await this.removeFieldModal!.open();

    if (result.ok) {
      const newFields = fields.slice(0, index).concat(fields.slice(index + 1));
      this.setState({ fields: newFields });
    }
  }

  protected moveUp(fieldName: string) {
    const index = this.state.fields.findIndex(field => field.name === fieldName);
    this.swapWithNextField(index - 1);
  }

  protected moveDown(fieldName: string) {
    const index = this.state.fields.findIndex(field => field.name === fieldName);
    this.swapWithNextField(index);
  }

  protected swapWithNextField(index: number) {
    const { fields } = this.state;
    const newFields = fields.slice(0, index)
      .concat([fields[index + 1], fields[index]])
      .concat(fields.slice(index + 2));
    this.setState({ fields: newFields });
  }
}
