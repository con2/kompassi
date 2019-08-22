import * as React from 'react';
import { RouteComponentProps } from 'react-router';
import { LinkContainer } from 'react-router-bootstrap';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import FormGroup from 'reactstrap/lib/FormGroup';
import Input from 'reactstrap/lib/Input';
import ListGroup from 'reactstrap/lib/ListGroup';
import ListGroupItem from 'reactstrap/lib/ListGroupItem';

import MainViewContainer from '../common/MainViewContainer';
import ManagedModal from '../common/ManagedModal';
import SessionContext from '../common/SessionContext';
import Session from '../common/SessionContext/Session';

import FormEditor from './FormEditor';
import SchemaForm from './SchemaForm';
import { Field, FieldType, fieldTypes, Layout } from './SchemaForm/models';

import Tabs from '../common/Tabs';
import { T } from '../../translations';

type Tab = 'design' | 'preview' | 'properties';

export type FormEditorAction = 'addFieldAbove' | 'moveUp' | 'moveDown' | 'editField' | 'removeField';

interface FormEditorViewRouterProps {
  slug: string;
}

interface FormEditorViewState {
  loading: boolean;
  error?: string;

  title: string;
  fields: Field[];
  layout: Layout;

  activeTab: Tab;
  addingNewField: boolean;
  fieldBeingEdited?: Field;
}

function initState(loading = true): FormEditorViewState {
  return {
    loading,
    title: '',
    fields: [],
    layout: 'horizontal',
    activeTab: 'design',
    addingNewField: false,
  };
}

class AddFieldModal extends ManagedModal<FieldType> {}
class EditFieldModal extends ManagedModal<Field> {}
class RemoveFieldModal extends ManagedModal<null> {}

export default class FormEditorView extends React.Component<RouteComponentProps<FormEditorViewRouterProps>, FormEditorViewState> {
  static contextType = SessionContext;
  context!: Session;

  titleForm?: HTMLFormElement;

  state: FormEditorViewState = initState();

  addFieldModal: AddFieldModal | null = null;
  editFieldModal: EditFieldModal | null = null;
  removeFieldModal: RemoveFieldModal | null = null;

  async componentDidMount() {
    const { slug } = this.props.match.params;

    if (slug === 'new') {
      this.setState(initState(false));
    } else {
      try {
        const { title, fields } = await this.context.get(`forms/${slug}`);
        this.setState({ loading: false, title, fields });
      } catch (err) {
        this.setState({ loading: false, error: err.message });
      }
    }
  }

  render() {
    const { loading, error, title, fields, activeTab, layout, addingNewField } = this.state;
    const t = T(r => r.FormEditor);
    const tRoot = T(r => r);

    return (
      <MainViewContainer loading={loading} error={error}>
        <ButtonGroup className="float-md-right">
          <LinkContainer to="/forms" exact={true}>
            <Button color="danger" outline={true} size="sm">
              {t(r => r.cancel)}
            </Button>
          </LinkContainer>
          <Button color="primary" size="sm" onClick={this.save}>
            {t(r => r.save)}
          </Button>
        </ButtonGroup>

        <Tabs t={t}>
          {{
            design: (
              <>
                <form ref={(form: HTMLFormElement) => (this.titleForm = form)}>
                  <FormGroup>
                    <Input
                      bsSize="lg"
                      name="title"
                      placeholder={t(r => r.titlePlaceholder)}
                      value={title}
                      onChange={this.onTitleChange}
                      required={true}
                    />
                  </FormGroup>
                </form>

                <FormEditor fields={fields} layout="horizontal" onAction={this.onFormEditorAction}>
                  <Button outline={true} color="primary" size="sm" onClick={this.addField}>
                    {t(r => r.addField)}…
                  </Button>
                </FormEditor>
              </>
            ),
            preview: (
              <div style={{ display: activeTab === 'preview' ? '' : 'none' }}>
                {title ? <h2>{title}</h2> : null}
                <SchemaForm fields={fields} layout={layout} />
              </div>
            ),
          }}
        </Tabs>

        <AddFieldModal
          title={t(r => r.addField)}
          ref={ref => {
            this.addFieldModal = ref;
          }}
          footer={
            <ButtonGroup className="float-right">
              <Button color="danger" outline={true} onClick={() => this.addFieldModal!.cancel()}>
                {tRoot(r => r.Common.cancel)}
              </Button>
            </ButtonGroup>
          }
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
                {t(r => r.FieldTypes[fieldType])}
              </ListGroupItem>
            ))}
          </ListGroup>
        </AddFieldModal>

        <EditFieldModal
          title={addingNewField ? t(r => r.addField) : t(r => r.editField)}
          ref={ref => {
            this.editFieldModal = ref;
          }}
        >
          <p>Edit field</p>
        </EditFieldModal>

        <RemoveFieldModal
          ref={ref => {
            this.removeFieldModal = ref;
          }}
          title={t(r => r.RemoveFieldModal.title)}
          footer={
            <ButtonGroup className="float-right">
              <Button color="danger" onClick={() => this.removeFieldModal!.ok()}>
                {t(r => r.RemoveFieldModal.yes)}
              </Button>
              <Button color="secondary" outline={true} onClick={() => this.removeFieldModal!.cancel()}>
                {t(r => r.RemoveFieldModal.no)}
              </Button>
            </ButtonGroup>
          }
        >
          <p>{t(r => r.RemoveFieldModal.message)}</p>
        </RemoveFieldModal>
      </MainViewContainer>
    );
  }

  onTitleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const title = event.target.value;
    this.setState({ title });
  };

  onFormEditorAction = (action: FormEditorAction, fieldName: string) => {
    switch (action) {
      case 'addFieldAbove':
        return this.addFieldAbove(fieldName);
      case 'removeField':
        return this.removeField(fieldName);
      case 'moveUp':
        return this.moveUp(fieldName);
      case 'moveDown':
        return this.moveDown(fieldName);
    }
  };

  protected async addFieldAbove(fieldName: string) {
    const { fields } = this.state;
    const index = fields.findIndex(field => field.name === fieldName);

    if (index < 0) {
      throw new Error(`asked to addFieldAbove nonexistent ${fieldName}`);
    }

    const result = await this.getNewField();

    if (!result.ok) {
      return;
    }

    const newFields = fields
      .slice(0, index)
      .concat([result.payload!])
      .concat(fields.slice(index));

    this.setState({ fields: newFields });
  }

  protected addField = async () => {
    const result = await this.getNewField();

    if (!result.ok) {
      return;
    }

    const fields = this.state.fields.concat([result.payload!]);

    this.setState({ fields });
  };

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
  };

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
    const newFields = fields
      .slice(0, index)
      .concat([fields[index + 1], fields[index]])
      .concat(fields.slice(index + 2));
    this.setState({ fields: newFields });
  }

  protected save = async () => {
    const { slug } = this.props.match.params;

    if (!this.titleForm!.reportValidity()) {
      this.setState({ activeTab: 'design' });
      setTimeout(() => this.titleForm!.reportValidity(), 0);
      return;
    }

    if (slug === 'new') {
      await this.context.post('forms', this.serializeForm());
    } else {
      await this.context.put(`forms/${slug}`, this.serializeForm());
    }
  };

  protected serializeForm() {
    const { title, fields } = this.state;
    return { title, fields };
  }
}
