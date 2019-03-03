import i18n from 'i18next';
import BrowserLanguageDetector from 'i18next-browser-languagedetector';
import { initReactI18next } from "react-i18next";

import en from './en';
import fi from './fi';


export interface Translations {
  [index: string]: i18n.ResourceKey;
  Common: {
    ok: string;
    cancel: string;
  };
  Event: {
    name: string;
    headline: string;
  };
  Navigation: {
    logIn: string;
    logOut: string;
  };
  NotFound: {
    notFoundHeader: string;
    notFoundMessage: string;
  };
  SchemaForm: {
    submit: string;
  };
  FormEditor: {
    editField: string;
    moveUp: string;
    moveDown: string;
    removeField: string;
    addFieldAbove: string;
    addField: string;
    design: string;
    preview: string;

    FieldTypes: {
      SingleLineText: string;
      MultiLineText: string;
      Divider: string;
      StaticText: string;
      Spacer: string;
    };

    RemoveFieldModal: {
      title: string;
      message: string;
      yes: string;
      no: string;
    }
  };
}

const resources: i18n.Resource = { fi, en };


export default i18n
  .use(initReactI18next)
  .use(BrowserLanguageDetector)
  .init({
    fallbackLng: 'en',
    resources,
  });
