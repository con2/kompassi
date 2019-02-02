import { Translations } from '.';

const translations: Translations = {
  Common: {
    ok: 'OK',
    cancel: 'Peruuta',
  },
  Event: {
    headline: 'Aika ja paikka',
    name: 'Nimi',
  },
  Navigation: {
    logIn: 'Kirjaudu sisään',
    logOut: 'Kirjaudu ulos',
  },
  NotFound: {
    notFoundHeader: 'Sivua ei löydy',
    notFoundMessage: 'Annettu osoite ei noudata mitään tunnistettua muotoa. Ole hyvä ja tarkista osoite.',
  },
  SchemaForm: {
    submit: 'Lähetä',
  },
  FormEditor: {
    editField: 'Muokkaa kenttää',
    moveUp: 'Siirrä ylös',
    moveDown: 'Siirrä alas',
    removeField: 'Poista kenttä',
    addFieldAbove: 'Lisää kenttä ylle',
    addField: 'Lisää kenttä',
    design: 'Muokkaa',
    preview: 'Esikatsele',

    FieldTypes: {
      SingleLineText: 'Yksirivinen tekstikenttä',
      MultiLineText: 'Monirivinen tekstikenttä',
      Divider: 'Erotinviiva',
      StaticText: 'Kiinteä teksti',
      Spacer: 'Tyhjä tila',
    },

    RemoveFieldModal: {
      title: 'Vahvista kentän poisto',
      message: 'Poistetaanko kenttä?',
      yes: 'Kyllä, poista',
      no: 'Ei, peruuta',
    },
  },
};
export default translations;
