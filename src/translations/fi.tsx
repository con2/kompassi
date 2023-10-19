import type { Translations } from "./en";

const translations: Translations = {
  AccommodationOnboardingView: {
    title: "Majoituksen sisäänkirjaus",
  },
  Common: {
    ok: "OK",
    cancel: "Peruuta",
    submit: "Lähetä",
    search: "Haku",
    somethingWentWrong:
      "Jokin meni pieleen. JavaScript-konsolissa voi olla lisätietoja.",
    actions: "Toiminnot",
    standardActions: {
      open: "Avaa",
      edit: "Muokkaa",
      delete: "Poista",
      create: "Uusi",
    },
    formFields: {
      firstName: {
        title: "Etunimi",
      },
      lastName: {
        title: "Sukunimi",
      },
      email: {
        title: "Sähköpostiosoite",
      },
      phone: {
        title: "Puhelinnumero",
      },
    },
  },
  DataTable: {
    create: "Luo uusi",
  },
  Event: {
    title: "Tapahtumat",
    headline: "Aika ja paikka",
    name: "Nimi",
    workInProgress:
      "Kompassi v2 on työn alla. Tämä ei ole vielä valmis etusivu, vaan taulukkokomponentin demo.",
  },
  Navigation: {
    forms: "Lomakkeet",
    logIn: "Kirjaudu sisään",
    logOut: "Kirjaudu ulos",
  },
  NotFound: {
    notFoundHeader: "Sivua ei löydy",
    notFoundMessage:
      "Annettu osoite ei noudata mitään tunnistettua muotoa. Ole hyvä ja tarkista osoite.",
  },
  SchemaForm: {
    submit: "Lähetä",
  },
  Forms: {
    heading: "Lomakkeet",
    title: "Otsikko",
    slug: "Tekninen nimi",
    create: "Uusi lomake",
  },
  FormResponses: {
    heading: "Lomakkeiden vastaukset",
    form: "Lomake",
    user: "Käyttäjä",
  },
  MainView: {
    defaultErrorMessage:
      "Jokin meni pieleen. JavaScript-konsolissa voi olla lisätietoja.",
  },
  FormEditor: {
    editField: "Muokkaa kenttää",
    moveUp: "Siirrä ylös",
    moveDown: "Siirrä alas",
    removeField: "Poista kenttä",
    addFieldAbove: "Lisää kenttä ylle",
    addField: "Lisää kenttä",
    save: "Tallenna lomake",
    cancel: "Palaa tallentamatta",
    open: "Avaa lomake",
    saveFailedErrorMessage:
      "Jokin meni pieleen lomaketta tallennettaessa. JavaScript-konsolissa voi olla lisätietoja.",

    Tabs: {
      design: "Muokkaa",
      preview: "Esikatsele",
      properties: "Asetukset",
    },

    FormPropertiesForm: {
      flags: {
        title: "Toiminta",
      },
      title: {
        title: "Lomakkeen otsikko",
        helpText:
          "Ihmisen luettava lomakkeen otsikko. Ei välttämättä näytetä lomakkeiden kaikkien käyttötarkoitusten yhteydessä.",
      },
      slug: {
        title: "Tekninen nimi",
        helpText:
          "Lomakkeen tekninen nimi. Tulee osaksi lomakkeen osoitetta. Sallitut merkit: kirjaimet A-Za-z, numerot 0-9 ja alaviiva _. Ei saa alkaa numerolla.",
      },
      layout: {
        title: "Asettelu",
        helpText:
          "Tässä valittu asettelu ei välttämättä ole käytössä kaikkien käyttötarkoitusten yhteydessä (esim. ahtaassa tilassa asettelu voi olla pakotettu vaakasuuntaiseksi).",
        choices: {
          horizontal: "Vaakasuuntainen",
          vertical: "Pystysuuntainen",
        },
      },
      standalone: {
        title: "Itsenäinen lomake",
        helpText:
          "Itsenäisen lomakkeen voi täyttää yleiskäyttöisen lomakenäkymän kautta. Ei-itsenäisen lomakkeen voi täyttää vain toiseen käyttötapaukseen upotettuna.",
      },
      active: {
        title: "Aktiivinen",
        helpText:
          "Ei-aktiivisia lomakkeita ei voi täyttää. Tämä koskee ainoastaan itsenäisiä lomakkeita; ei-itsenäisen lomakkeen aktiivisuuden ratkaisee käyttötapaus, johon lomake on upotettu.",
      },
      loginRequired: {
        title: "Vaatii sisäänkirjautumisen",
        helpText: "Koskee ainoastaan itsenäisiä lomakkeita.",
      },
    },

    EditFieldForm: {
      name: {
        title: "Tekninen nimi",
        helpText:
          "Kentän tekninen nimi. Ei näytetä loppukäyttäjälle. Sallitut merkit: kirjaimet A-Za-z, numerot 0-9 ja alaviiva _. Ei saa alkaa numerolla.",
      },
      title: {
        title: "Otsikko",
        helpText:
          "Ihmisluettava otsikko. Näytetään loppukäyttäjälle. Mikäli otsikkoa ei ole asetettu, sen tilalla näytetään kentän tekninen nimi.",
      },
      helpText: {
        title: "Ohjeteksti",
        helpText: "Näytetään kentän alla.",
      },
      required: {
        title: "Pakollinen",
      },
      options: {
        title: "Vaihtoehdot",
        helpText: "arvo=teksti -pareja, yksi per rivi",
      },
    },

    FieldTypes: {
      SingleLineText: "Yksirivinen tekstikenttä",
      MultiLineText: "Monirivinen tekstikenttä",
      Divider: "Erotinviiva",
      StaticText: "Kiinteä teksti",
      Spacer: "Tyhjä tila",
      SingleCheckbox: "Yksittäinen rasti ruutuun -kenttä",
      SingleSelect: "Alasvetovalikko (yksi valinta)",
    },

    RemoveFieldModal: {
      title: "Vahvista kentän poisto",
      message: "Poistetaanko kenttä?",
      yes: "Kyllä, poista",
      no: "Ei, peruuta",
    },
  },

  SplashView: {
    engagement: (
      <>
        Toteutamme parhaillaan{" "}
        <strong>Kompassi-tapahtumanhallintajärjestelmän</strong>{" "}
        avaintoiminnallisuutta uudelleen moderneilla web-teknologioilla
        voidaksemme tarjota paremman käyttökokemuksen ja mukautettavuuden.
      </>
    ),
    backToKompassi: "Takaisin Kompassiin",
  },

  EventsView: {
    title: "Tapahtumat",
  },


  TicketsView: {
    title: "Osta lippuja",
    productsTable: {
      product: "Tuote",
      price: "Hinta",
      quantity: "Lukumäärä",
    },
    contactForm: {
      title: "Yhteystiedot",
    },
    purchaseButtonText: "Osta",
    acceptTermsAndConditions(url: string) {
      return (<>Hyväksyn <a href={url} target="_blank" rel="noopener noreferrer">lipunmyynnin ehdot</a> (pakollinen).</>);
    },
  },

  Brand: {
    appName: (
      <>
        Kompassi<sup>v2 BETA</sup>
      </>
    ),
  },

  // Do not translate
  LanguageSelection: {
    // NOTE: quality of life hack only until we have a third language
    currentLanguage: {
      nameInCurrentLanguage: "suomeksi",
      code: "fi",
    },
    otherLanguage: {
      nameInOtherLanguage: "In English",
      code: "en",
    },
  },
};

export default translations;
