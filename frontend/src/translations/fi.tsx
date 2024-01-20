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
  UserMenu: {
    signIn: "Kirjaudu sisään",
    responses: "Kyselyvastaukset",
    signOut: "Kirjaudu ulos",
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
      return (
        <>
          Hyväksyn{" "}
          <a href={url} target="_blank" rel="noopener noreferrer">
            lipunmyynnin ehdot
          </a>{" "}
          (pakollinen).
        </>
      );
    },
  },

  NewProgrammeView: {
    title: "Tarjoa ohjelmanumeroa",
    engagement: (eventName: string) => (
      <>
        Tervetuloa tarjoamaan ohjelmaa {eventName}
        {eventName.includes(" ") ? " " : ""}-tapahtumaan! Aloita valitsemalla
        tarjottavan ohjelman tyyppi alta.
      </>
    ),
    selectThisProgramType: "Valitse tämä ohjelmatyyppi",
    backToProgramFormSelection: "Takaisin ohjelmatyypin valintaan",
    forEvent: (eventName: string) => <>tapahtumaan {eventName}</>,
    submit: "Lähetä",
  },

  Survey: {
    listTitle: "Kyselyt",
    singleTitle: "Kysely",
    forEvent: (eventName: string) => <>tapahtumalle {eventName}</>,
    surveyTableFooter: (count: number) => (
      <>
        {count} kysely{count === 1 ? "" : "ä"}.
      </>
    ),
    responseListTitle: "Kyselyvastaukset",
    responseDetailTitle: "Kyselyvastaus",
    summaryTitle: "Vastausten yhteenveto",
    ownResponsesTitle: "Omat kyselyvastaukset",
    responseTableFooter: (filteredCount: number, totalCount: number) => (
      <>
        Näytetään {filteredCount} kyselyvastaus{filteredCount === 1 ? "" : "ta"}{" "}
        (yhteensä {totalCount}).
      </>
    ),
    dimensionTableFooter: (countDimensions: number, countValues: number) => (
      <>
        Yhteensä {countDimensions} dimensio{countDimensions === 1 ? "" : "ta"},{" "}
        {countValues} arvo{countValues === 1 ? "" : "a"}.
      </>
    ),
    summaryOf: (filteredCount: number, totalCount: number) => (
      <>
        Yhteenveto {filteredCount} vastauksesta (yhteensä {totalCount}).
      </>
    ),
    attributes: {
      slug: "Tekninen nimi",
      title: "Otsikko",
      isActive: {
        title: "Avoinna vastauksille",
        untilFurtherNotice: "Avoinna toistaiseksi",
        untilTime: (time: Date) => `Avoinna ${time.toLocaleString()} asti`,
        openingAt: (time: Date) => `Avautuu ${time.toLocaleString()}`,
        closed: "Suljettu",
      },
      countResponses: "Vastauksia",
      languages: "Kielet",
      actions: "Toiminnot",
      anonymity: {
        secondPerson: {
          title: "Vastausten yhdistäminen sinuun",
          choices: {
            HARD: "Vastaukset ovat anonyymejä. Et voi palata katsomaan tai muokkaamaan vastauksiasi.",
            SOFT: "Jos vastaat tähän kyselyyn kirjautuneena, se yhdistetään käyttäjätiliisi, jotta voit palata katsomaan tai muokkaamaan vastauksiasi, mutta henkilöllisyyttäsi ei jaeta kyselyn omistajan kanssa.",
            NAME_AND_EMAIL:
              "Jos vastaat tähän kyselyyn kirjautuneena, se yhdistetään käyttäjätiliisi. Nimesi ja sähköpostiosoitteesi jaetaan kyselyn omistajan kanssa. Voit palata katsomaan tai muokkaamaan vastauksiasi.",
          },
        },
        thirdPerson: {
          title: "Vastausten yhdistäminen käyttäjään",
          choices: {
            HARD: "Vastaukset ovat anonyymejä. Käyttäjät eivät voi palata katsomaan tai muokkaamaan vastauksiaan.",
            SOFT: "Jos käyttäjä vastaa tähän kyselyyn kirjautuneena, hänen vastauksensa yhdistetään hänen käyttäjätiliinsä, jotta hän voi palata katsomaan tai muokkaamaan vastauksiaan, mutta hänen henkilöllisyyttään ei jaeta sinulle.",
            NAME_AND_EMAIL:
              "Jos käyttäjä vastaa tähän kyselyyn kirjautuneena, hänen vastauksensa yhdistetään hänen käyttäjätiliinsä. Hänen nimensä ja sähköpostiosoitteensa jaetaan sinulle. Hän voi palata katsomaan tai muokkaamaan vastauksiaan.",
          },
        },
      },
      dimensions: "Dimensiot",
      dimension: "Dimensio",
      values: "Arvot",
      value: "Arvo",
      createdAt: "Lähetysaika",
      createdBy: "Lähettäjä",
      event: "Tapahtuma",
      formTitle: "Kyselyn otsikko",
      language: "Kieli",
      choice: "Vaihtoehto",
      question: "Kysymys",
      countMissingResponses: "Ei vastausta",
      percentageOfResponses: "Osuus vastauksista",
      technicalDetails: "Tekniset tiedot",
    },
    actions: {
      fillIn: {
        title: "Täytä",
        disabledTooltip: "Suljettua kyselyä ei voi täyttää",
      },
      share: {
        title: "Jaa",
        tooltip: "Kopioi linkki leikepöydälle",
        success: "Linkki kyselyyn on kopioitu leikepöydälle.",
      },
      viewResponses: "Vastaukset",
      summary: "Yhteenveto",
      submit: "Lähetä",
      downloadAsExcel: "Lataa Excel-tiedostona",
      returnToResponseList: "Palaa vastauslistaukseen",
      returnToSurveyList: "Palaa kyselylistaukseen",
      saveDimensions: "Tallenna dimensiot",
    },
    thankYou: {
      title: "Kiitos vastauksistasi!",
      defaultMessage:
        "Vastauksesi on tallennettu. Voit nyt sulkea tämän välilehden.",
    },
    maxResponsesPerUserReached: {
      title: "Olet jo vastannut tähän kyselyyn",
      defaultMessage: (
        maxResponsesPerUser: number,
        countResponsesByCurrentUser: number,
      ) =>
        `Olet jo vastannut tähän kyselyyn${
          countResponsesByCurrentUser === 1
            ? ""
            : " " + countResponsesByCurrentUser + " kertaa"
        }. Voit vastata tähän kyselyyn enintään ${maxResponsesPerUser} ${
          maxResponsesPerUser === 1 ? "kerran" : "kertaa"
        }.`,
    },
    warnings: {
      choiceNotFound:
        "Vaihtoehtoa ei löydy. Se on voitu poistaa tämän vastauksen lähettämisen jälkeen.",
    },
    checkbox: {
      checked: "Valittu",
      unchecked: "Ei valittu",
    },
  },

  SignInRequired: {
    metadata: {
      title: "Kirjautuminen vaaditaan – Kompassi",
    },
    title: "Kirjautuminen vaaditaan",
    message: "Tämä sivu edellyttää sisäänkirjautumista.",
    signIn: "Kirjaudu sisään",
  },

  Brand: {
    appName: (
      <>
        Kompassi<sup>v2 BETA</sup>
      </>
    ),
    plainAppName: "Kompassi",
  },

  // Do not translate
  LanguageSwitcher: {
    // NOTE: value always in target language
    supportedLanguages: {
      fi: "suomeksi",
      en: "In English",
    },
  },
};

export default translations;
