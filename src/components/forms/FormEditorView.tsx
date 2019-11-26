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
import { Form as FormType, Field, FieldType, fieldTypes, Layout } from './SchemaForm/models';

import Tabs from '../common/Tabs';
import { T, t } from '../../translations';
import slugify from '../../utils/slugify';
import { Form, Label, FormText, Col } from 'reactstrap';
import HorizontalField from './HorizontalField';

type Tab = 'design' | 'preview' | 'properties';
type Flag = 'active' | 'standalone' | 'loginRequired';
const flags: Flag[] = ['standalone', 'active', 'loginRequired'];

export type FormEditorAction = 'addFieldAbove' | 'moveUp' | 'moveDown' | 'editField' | 'removeField';

const tEditor = T(r => r.FormEditor.EditFieldForm);

const nameField: Field = {
  type: 'SingleLineText',
  name: 'name',
  title: tEditor(r => r.name.title),
  helpText: tEditor(r => r.name.helpText),
  required: true,
};

const baseFieldEditorFields: Field[] = [
  nameField,
  {
    type: 'SingleLineText',
    name: 'title',
    title: tEditor(r => r.title.title),
    helpText: tEditor(r => r.title.helpText),
    required: false,
  },
  {
    type: 'MultiLineText',
    name: 'helpText',
    title: tEditor(r => r.helpText.title),
    helpText: tEditor(r => r.helpText.helpText),
    required: false,
  },
  {
    type: 'SingleCheckbox',
    name: 'required',
    title: tEditor(r => r.required.title),
    required: false,
  },
];

const fieldEditorMapping = {
  SingleLineText: baseFieldEditorFields,
  MultiLineText: baseFieldEditorFields,
  Divider: [nameField],
  StaticText: baseFieldEditorFields,
  SingleCheckbox: baseFieldEditorFields,
  Spacer: [nameField],
};

interface FormEditorViewRouterProps {
  slug: string;
}

interface FormEditorViewState extends FormType {
  loading: boolean;
  error?: string;

  addingNewField: boolean;
  fieldBeingEdited?: Field;
  autoGenerateSlug: boolean;
  activeTab: Tab;
}

function initState(loading = true): FormEditorViewState {
  return {
    loading,
    addingNewField: false,
    autoGenerateSlug: true,
    activeTab: 'design',

    slug: '',
    title: '',
    fields: [],
    layout: 'horizontal',
    loginRequired: false,
    standalone: true,
    active: true,
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
        this.setState({ loading: false, autoGenerateSlug: false, title, fields, slug });
      } catch (err) {
        this.setState({ loading: false, error: err.message });
      }
    }
  }

  render() {
    const { loading, error, title, slug, fields, layout, addingNewField, fieldBeingEdited, activeTab, active, standalone } = this.state;
    const t = T(r => r.FormEditor);
    const tRoot = T(r => r);
    const isOpenButtonShown = slug !== 'new' && active && standalone;

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
          {/* TODO link button */}
          {isOpenButtonShown && (
            <Button color="success" size="sm" onClick={this.open}>
              {t(r => r.open)}…
            </Button>
          )}
        </ButtonGroup>

        <Tabs t={T(r => r.FormEditor.Tabs)} activeTab={activeTab} onChange={this.setActiveTab}>
          {{
            design: (
              <>
                <form ref={(form: HTMLFormElement) => (this.titleForm = form)}>
                  <FormGroup>
                    <Input
                      bsSize="lg"
                      name="title"
                      placeholder={t(r => r.FormPropertiesForm.title.title)}
                      value={title}
                      onChange={this.onTitleChange}
                      required={true}
                    />
                  </FormGroup>
                </form>

                <FormEditor fields={fields} layout={layout} onAction={this.onFormEditorAction}>
                  <Button outline={true} color="primary" size="sm" onClick={this.addField}>
                    {t(r => r.addField)}…
                  </Button>
                </FormEditor>
              </>
            ),
            preview: (
              <>
                {title ? <h2>{title}</h2> : null}
                <SchemaForm fields={fields} layout={layout} />
              </>
            ),
            properties: (
              <Form onSubmit={() => {}}>
                <HorizontalField
                  name="title"
                  title={t(r => r.FormPropertiesForm.title.title)}
                  helpText={t(r => r.FormPropertiesForm.title.helpText)}
                  required={true}
                >
                  <Input name="title" value={title} onChange={this.onTitleChange} required={true} />
                </HorizontalField>

                <HorizontalField
                  name="slug"
                  title={t(r => r.FormPropertiesForm.slug.title)}
                  helpText={t(r => r.FormPropertiesForm.slug.helpText)}
                >
                  <Input name="slug" value={slug} onChange={this.onSlugChange} />
                </HorizontalField>

                <HorizontalField
                  name="layout"
                  title={t(r => r.FormPropertiesForm.layout.title)}
                  helpText={t(r => r.FormPropertiesForm.layout.helpText)}
                >
                  <Input name="layout" type="select" onChange={this.onLayoutChange}>
                    <option value="horizontal">{t(r => r.FormPropertiesForm.layout.choices.horizontal)}</option>
                    <option value="vertical">{t(r => r.FormPropertiesForm.layout.choices.vertical)}</option>
                  </Input>
                </HorizontalField>

                <FormGroup className="row">
                  <Label className="col-md-3">{t(r => r.FormPropertiesForm.flags.title)}</Label>
                  <Col md={9}>
                    {flags.map(flag => (
                      <React.Fragment key={flag}>
                        <Label check={true} for={flag} className="pb-2">
                          <Input type="checkbox" id={flag} name={flag} onChange={this.handleFlagChange} checked={this.state[flag]} />
                          {t(r => r.FormPropertiesForm[flag].title)}
                          <FormText>{t(r => r.FormPropertiesForm[flag].helpText)}</FormText>
                        </Label>
                      </React.Fragment>
                    ))}
                  </Col>
                </FormGroup>
              </Form>
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
          {fieldBeingEdited && (
            <SchemaForm
              layout="horizontal"
              fields={fieldEditorMapping[fieldBeingEdited.type]}
              value={fieldBeingEdited}
              onChange={this.onFieldBeingEditedChange}
            />
          )}
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

  setActiveTab = (activeTab: Tab) => {
    this.setState({ activeTab });
  };

  onTitleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const title = event.target.value;
    const { autoGenerateSlug } = this.state;
    const slug = autoGenerateSlug ? slugify(title) : this.state.slug;

    this.setState({ title, slug });
  };

  onSlugChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const slug = event.target.value;
    this.setState({ slug, autoGenerateSlug: !slug });
  };

  onLayoutChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const layout = event.target.value;

    // cast is safe because it comes from a select that only has these options
    this.setState({ layout: layout as Layout });
  };

  onFieldBeingEditedChange = (fieldBeingEdited: Field) => {
    this.setState({ fieldBeingEdited });
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
      case 'editField':
        return this.editField(fieldName);
    }
  };

  handleFlagChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const flag: Flag = event.currentTarget.name as Flag;
    const { checked } = event.currentTarget;

    this.setState({ [flag]: checked } as any);
  };

  protected async addFieldAbove(fieldName: string) {
    const { fields } = this.state;
    const index = fields.findIndex(field => field.name === fieldName);

    if (index < 0) {
      throw new Error(`asked to addFieldAbove nonexistent ${fieldName}`);
    }

    const result = await this.getNewField();
    const { fieldBeingEdited } = this.state;

    if (!result.ok) {
      return;
    }

    const newFields = fields
      .slice(0, index)
      .concat([fieldBeingEdited!])
      .concat(fields.slice(index));

    this.setState({ fields: newFields });
  }

  protected addField = async () => {
    const result = await this.getNewField();
    const { fieldBeingEdited } = this.state;

    if (!result.ok) {
      return;
    }

    const fields = this.state.fields.concat([fieldBeingEdited!]);

    this.setState({ fields });
  };

  protected editField = async (fieldName: string) => {
    const { fields } = this.state;
    const index = fields.findIndex(field => field.name === fieldName);
    const fieldBeingEdited = fields[index];
    this.setState({ fieldBeingEdited });

    const result = await this.editFieldModal!.open();

    if (result.ok) {
      const newFields = fields
        .slice(0, index)
        .concat([this.state.fieldBeingEdited!])
        .concat(fields.slice(index + 1));
      this.setState({ fields: newFields });
    }
  };

  protected async getNewField() {
    const t = T(r => r.FormEditor);
    const result = await this.addFieldModal!.open();

    if (!result.ok) {
      return { ok: false };
    }

    const type = result.payload!;
    const name = this.makeNewFieldName(type);
    const title = t(r => r.FieldTypes[type]);

    const newField: Field = { type, name, title };

    this.setState({ fieldBeingEdited: newField });

    return this.editFieldModal!.open();
  }

  protected makeNewFieldName(type: FieldType) {
    const fields: { [key: string]: Field } = {};
    this.state.fields.forEach(field => (fields[field.name] = field));

    const baseName = type[0].toLowerCase() + type.slice(1);
    let counter = 1;
    let name = `${baseName}${counter}`;

    while (fields[name]) {
      counter += 1;
      name = `${baseName}${counter}`;
    }

    return name;
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
      setTimeout(() => this.titleForm!.reportValidity(), 0);
      return;
    }

    try {
      if (slug === 'new') {
        await this.context.post('forms', this.serializeForm());
      } else {
        await this.context.put(`forms/${slug}`, this.serializeForm());
      }
    } catch (err) {
      const error = err.message || t(r => r.FormEditor.saveFailedErrorMessage);
      this.setState({ error });
    }
  };

  protected open = async () => {
    const { slug } = this.props.match.params;
    window.open(`/forms/${slug}`);
  };

  protected serializeForm() {
    const { title, fields, slug } = this.state;
    return { title, fields, slug };
  }
}
