import { Translations } from '.';

const translations: Translations = {
  Common: {
    ok: 'OK',
    cancel: 'Cancel',
  },
  Event: {
    headline: 'Date and venue',
    name: 'Name',
  },
  Navigation: {
    logIn: 'Log in',
    logOut: 'Log out',
  },
  NotFound: {
    notFoundHeader: 'Page not found',
    notFoundMessage: 'The address does not conform to any of the recognized address patterns. Please double-check the address.',
  },
  SchemaForm: {
    submit: 'Submit',
  },
  FormEditor: {
    editField: 'Edit field',
    moveUp: 'Move up',
    moveDown: 'Move down',
    removeField: 'Remove field',
    addFieldAbove: 'Add field above',
    addField: 'Add field',
    design: 'Design',
    preview: 'Preview',

    FieldTypes: {
      SingleLineText: 'Single line text field',
      MultiLineText: 'Multi-line text field',
      Divider: 'Divider',
      StaticText: 'Static text',
      Spacer: 'Empty space',
    },

    RemoveFieldModal: {
      title: 'Confirm field removal',
      message: 'Remove the selected field?',
      yes: 'Yes, remove',
      no: 'No, cancel',
    },
  },
};

export default translations;
