import i18n from 'i18next';
import BrowserLanguageDetector from 'i18next-browser-languagedetector';
import { initReactI18next } from "react-i18next";

import en from './en';
import fi from './fi';


export type Translations = typeof en;

const resources: i18n.Resource = { fi, en };


export default i18n
  .use(initReactI18next)
  .use(BrowserLanguageDetector)
  .init({
    fallbackLng: 'en',
    resources,
  });
