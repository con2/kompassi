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
  Modal: {
    submit: "Submit",
    cancel: "Cancel",
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
    warnings: {
      noFileUploaded: "Ei tiedostoja.",
    },
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

    tabs: {
      design: "Muokkaa",
      preview: "Esikatsele",
      properties: "Asetukset",
    },

    editFieldForm: {
      slug: {
        title: "Tekninen nimi",
        helpText:
          "Kentän tekninen nimi. Ei näytetä loppukäyttäjälle. Sallitut merkit: kirjaimet A-Za-z, numerot 0-9 ja viiva -. Ei saa alkaa numerolla.",
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
      choices: {
        title: "Vaihtoehdot",
        helpText: "arvo=teksti -pareja, yksi per rivi",
      },
    },

    formPropertiesForm: {
      title: {
        title: "Otsikko",
        helpText: "Ihmisluettava otsikko. Näytetään loppukäyttäjälle.",
      },
      description: {
        title: "Kuvaus",
        helpText: "Näytetään lomakkeen yläpuolella.",
      },
      thankYouMessage: {
        title: "Kiitosviesti",
        helpText:
          "Näytetään lomakkeen lähetyksen jälkeen. Mikäli kiitosviestiä ei ole asetettu, näytetään oletusviesti.",
      },
    },

    fieldTypes: {
      SingleLineText: "Yksirivinen tekstikenttä",
      MultiLineText: "Monirivinen tekstikenttä",
      Divider: "Erotinviiva",
      StaticText: "Kiinteä teksti",
      Spacer: "Tyhjä tila",
      SingleCheckbox: "Yksittäinen rasti ruutuun -kenttä",
      SingleSelect: "Alasvetovalikko (yksi valinta)",
      MultiSelect: "Alasvetovalikko (useita valintoja)",
      RadioMatrix: "Valintamatriisi",
      FileUpload: "Tiedoston lähetys",
      NumberField: "Numero",
      DecimalField: "Desimaaliluku",
    },

    removeFieldModal: {
      title: "Vahvista kentän poisto",
      message: "Poistetaanko kenttä?",
      actions: {
        submit: "Poista",
        cancel: "Peruuta",
      },
    },

    editFieldModal: {
      title: "Muokkaa kenttää",
      actions: {
        submit: "Tallenna",
        cancel: "Peruuta",
      },
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
    ownResponsesTitle: "Omat kyselyvastaukset",
    showingResponses: (filteredCount: number, totalCount: number) => (
      <>
        Näytetään {filteredCount} vastaus{filteredCount === 1 ? "" : "ta"}{" "}
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
      slug: {
        title: "Tekninen nimi",
        helpText:
          "Koneellisesti luettava nimi kyselylle. Teknisen nimen täytyy olla uniikki tapahtuman sisällä. Teknistä nimeä ei voi muuttaa luomisen jälkeen.",
      },
      title: "Otsikko",
      isActive: {
        title: "Avoinna vastauksille",
        untilFurtherNotice: "Avoinna toistaiseksi",
        untilTime: (time: Date) => `Avoinna ${time.toLocaleString()} asti`,
        openingAt: (time: Date) => `Avautuu ${time.toLocaleString()}`,
        closed: "Suljettu",
      },
      activeFrom: {
        title: "Avautumisaika",
        helpText:
          "Jos tämä on asetettu, kysely alkaa ottaa vastaan vastauksia tähän aikaan.",
      },
      activeUntil: {
        title: "Sulkeutumisaika",
        helpText:
          "Jos tämä on asetettu, kysely lakkaa ottamasta vastaan vastauksia tähän aikaan.",
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
      sequenceNumber: "Järjestysnumero",
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
      loginRequired: {
        title: "Sisäänkirjautuminen vaaditaan",
        helpText:
          "Jos tämä on valittuna, kyselyyn vastaaminen vaatii sisäänkirjautumisen.",
      },
      maxResponsesPerUser: {
        title: "Käyttäjän vastausten maksimimäärä",
        helpText:
          "Yksittäisen käyttäjän vastausten maksimimäärä tähän kyselyyn. Jos arvoksi on asetettu 0, määrää ei rajoiteta. Huomaathan, että tämä vaikuttaa ainoastaan sisäänkirjautuneisiin käyttäjiin. Jotta rajoitus toimisi, kyselyyn vastaaminen tulee olla rajoitettu sisäänkirjautuneille käyttäjille.",
      },
    },
    actions: {
      createSurvey: "Luo kysely",
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
      submit: "Lähetä",
      downloadAsExcel: "Lataa Excel-tiedostona",
      returnToResponseList: "Palaa vastauslistaukseen",
      returnToSurveyList: "Palaa kyselylistaukseen",
      returnToDimensionList: "Palaa dimensiolistaukseen",
      saveDimensions: "Tallenna dimensiot",
      saveProperties: "Tallenna asetukset",
      addDimension: "Lisää dimensio",
      addDimensionValue: "Lisää arvo",
      deleteDimension: {
        title: "Poista dimensio",
        cannotRemove:
          "Dimensiota ei voi poistaa, jos se on jo liitetty kyselyvastaukseen.",
        confirmation: (dimensionTitle: string) => (
          <>
            Poista dimensio <strong>{dimensionTitle}</strong> kaikkine
            arvoineen?
          </>
        ),
        modalActions: {
          submit: "Poista",
          cancel: "Peruuta",
        },
      },
      deleteDimensionValue: {
        title: "Poista arvo",
        cannotRemove:
          "Arvoa ei voi poistaa, jos se on jo liitetty kyselyvastaukseen.",
        confirmation: (dimensionTitle: string, valueTitle: string) => (
          <>
            Poista arvo <strong>{dimensionTitle}</strong>
            dimensionsta <strong>{valueTitle}</strong>?
          </>
        ),
      },
      deleteSurvey: {
        title: "Poista kysely",
        cannotRemove: "Kyselyä, joka on jo saanut vastauksia, ei voi poistaa.",
        confirmation: (surveyTitle: string) => (
          <>
            Haluatko varmasti poistaa kyselyn <strong>{surveyTitle}</strong>?
          </>
        ),
        modalActions: {
          submit: "Poista",
          cancel: "Peruuta",
        },
      },
      editDimension: "Muokkaa dimensiota",
      editDimensionValue: "Muokkaa arvoa",
      editSurvey: "Muokkaa",
    },
    tabs: {
      summary: "Yhteenveto",
      responses: "Vastaukset",
      properties: "Kyselyn asetukset",
      addLanguage: "Lisää kieliversio",
      languageVersion: (languageName: string) => `Kieliversio: ${languageName}`,
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
    addLanguageModal: {
      language: {
        title: "Kieli",
        helpText: "Vain tuettuja kieliä voi lisätä.",
      },
      copyFrom: {
        title: "Alusta kieliversiosta",
        helpText:
          "Uusi kieliversio luodaan valitun kieliversion pohjalta. Voit myös valita lähteä liikkeelle tyhjällä lomakkeella.",
      },
      actions: {
        submit: "Jatka",
        cancel: "Peruuta",
      },
    },
    editDimensionModal: {
      editTitle: "Muokkaa dimensiota",
      addTitle: "Lisää dimensio",
      actions: {
        submit: "Tallenna dimensio",
        cancel: "Peruuta",
      },
      attributes: {
        slug: {
          title: "Tekninen nimi",
          // TODO add pattern for slug and document it in helpText
          helpText:
            "Koneluettava, lyhyt nimi dimensiolle. Teknistä nimeä ei voi muuttaa dimension luomisen jälkeen.",
        },
        localizedTitleHeader: {
          title: "Otsikko lokalisoituna",
          helpText:
            "Dimensiolle voi antaa otsikon eri kielillä. Otsikkoa ei tarvitse antaa kaikilla tuetuilla kielillä: jos otsikkoa ei ole annettu valitulla kielellä, käytetään tilalla oletuskieltä, ja jos sitäkään ei ole asetettu, teknistä nimeä.",
        },
        title: {
          fi: "Otsikko suomeksi",
          en: "Otsikko englanniksi",
          sv: "Otsikko ruotsiksi",
        },
        isKeyDimension: {
          title: "Avaindimensio",
          helpText: "Avaindimensioiden arvot näytetään vastauslistassa.",
        },
        isMultiValue: {
          title: "Moniarvoinen",
          helpText:
            "Jos tämä on valittuna, tähän dimensioon voidaan valita useita arvoja.",
        },
        isShownToRespondent: {
          title: "Näytetään vastaajalle",
          helpText:
            "Jos tämä on valittuna, tämän dimension arvot näytetään vastaajalle yksittäisen vastauksen näkymässä hänen profiilissaan. Lisäksi, jos tämä dimensio on myös avaindimensio, se näytetään profiilin vastauslistassa.",
        },
      },
    },
    editValueModal: {
      editTitle: "Muokkaa arvoa",
      addTitle: "Lisää arvo",
      actions: {
        submit: "Tallenna arvo",
        cancel: "Peruuta",
      },
      attributes: {
        slug: {
          title: "Tekninen nimi",
          // TODO add pattern for slug and document it in helpText
          helpText:
            "Koneluettava, lyhyt nimi arvolle. Teknistä nimeä ei voi muuttaa dimension luomisen jälkeen.",
        },
        localizedTitleHeader: {
          title: "Otsikko lokalisoituna",
          helpText:
            "Arvolle voi antaa otsikon eri kielillä. Otsikkoa ei tarvitse antaa kaikilla tuetuilla kielillä: jos otsikkoa ei ole annettu valitulla kielellä, käytetään tilalla oletuskieltä, ja jos sitäkään ei ole asetettu, teknistä nimeä.",
        },
        title: {
          fi: "Otsikko suomeksi",
          en: "Otsikko englanniksi",
          sv: "Otsikko ruotsiksi",
        },
      },
    },
    createSurveyModal: {
      title: "Luo uusi kysely",
      actions: {
        submit: "Luo kysely",
        cancel: "Peruuta",
      },
    },
    editSurveyPage: {
      title: "Muokkaa kyselyä",
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

  LanguageSwitcher: {
    supportedLanguages: {
      fi: "suomi",
      en: "englanti",
    },
    // NOTE: value always in target language
    switchTo: {
      fi: "suomeksi",
      en: "In English",
    },
  },
};

export default translations;
