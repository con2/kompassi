import i18n from 'i18next';
import BrowserLanguageDetector from 'i18next-browser-languagedetector';

import en from './en';
import fi from './fi';


export interface Translations {
  [index: string]: i18n.ResourceKey;
  Navigation: {
    logIn: string;
    logOut: string;
  };
}

const resources: i18n.Resource = { fi, en };


export default i18n
  .use(BrowserLanguageDetector)
  .init({
    fallbackLng: 'en',
    resources,
  });
