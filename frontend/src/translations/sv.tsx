// Translators: Kirsi Västi, Calle Tengman, Santtu Pajukanta

import type { Translations } from "./en";

/// Mark untranslated English strings with this
/// Eg.
/// { foo: UNTRANSLATED("bar") }
function UNTRANSLATED<T>(wat: T): T {
  return wat;
}

/// Mark strings to be checked by a native speaker / more experienced translator with this
function UNSURE<T>(wat: T): T {
  return wat;
}

const translations: Translations = {
  Common: {
    ok: "OK",
    cancel: "Avbryt",
    submit: "Skicka",
    search: "Sök",
    somethingWentWrong:
      "Något gick fel. Det kan finnas ytterligare information i JavaScript-konsolen.",
    actions: "Funktioner",
    standardActions: {
      open: "Öppna",
      edit: "Ändra",
      delete: "Radera",
      create: "Skapa",
    },
    boolean: {
      true: "Ja",
      false: "Nej",
    },
  },
  Profile: {
    attributes: {
      displayName: {
        title: "Namn",
      },
      email: {
        title: "E-postadress",
      },
    },
    keysView: UNTRANSLATED({
      title: "Encryption keys",
      description:
        "In some cases, confidential data is encrypted in Kompassi using asymmetric encryption. " +
        "If you need to be the recipient of such confidential information, you need to have a key pair. " +
        "You can generate one below. " +
        "Generating a key pair requires your password as the private key will be encrypted with it. " +
        "In the future, we will allow advanced users to use keys stored on their own devices only, " +
        "so that the private key never leaves the device.",
      resetPasswordWarning: (
        <>
          <strong>Warning!</strong> If you forget your password and resert it,
          you will lose your encryption keys and will no longer be able to
          access data encrypted to them.
        </>
      ),
      attributes: {
        id: {
          title: "Key ID",
        },
        createdAt: {
          title: "Created at",
        },
        actions: {
          title: "Actions",
        },
        password: {
          title: "Password",
          helpText: "Enter your password to encrypt the private key.",
        },
      },
      actions: {
        generate: {
          title: "Generate key pair",
          enterPassword: "Enter your password to encrypt the private key.",
          modalActions: {
            submit: "Generate",
            cancel: "Cancel",
          },
        },
        revoke: {
          title: "Revoke key pair",
          confirmation: (formattedCreatedAt: string) => (
            <>
              Are you sure you want to revoke the key pair that was created on{" "}
              <strong>{formattedCreatedAt}</strong>? Once revoked, information
              that was encrypted with the private key will no longer be
              accessible. This action cannot be undone.
            </>
          ),
          modalActions: {
            submit: "Revoke",
            cancel: "Cancel",
          },
        },
      },
    }),
  },
  // Note that this also defines the type for the messages object that can be passed to the InterceptingRouteModal component
  Modal: {
    submit: "Skicka",
    cancel: "Avbryt",
  },
  DataTable: {
    create: "Skapa",
  },
  Event: {
    title: "Evenemang",
    headline: "Datum och plats",
    name: "Namn",
    workInProgress:
      "Kompassi v2 är ett pågående arbete. Detta är inte den färdiga förstasidan, utan snarare en demo av tabellkomponenten.",
  },
  UserMenu: {
    responses: "Enkätsvar",
    keys: UNSURE("Krypteringsnycklar"),
    signIn: "Logga in",
    signOut: "Logga ut",
  },
  NotFound: {
    notFoundHeader: "Sidan hittades inte",
    notFoundMessage:
      "Adressen överensstämmer inte med något av de kända adressmönstren. Vänligen dubbelkolla adressen.",
  },
  SchemaForm: {
    submit: "Skicka",
    warnings: {
      noFileUploaded: "Inga filer.",
    },
  },
  MainView: {
    defaultErrorMessage:
      "Något gick fel. Det kan finnas ytterligare information i JavaScript-konsolen.",
  },
  FormEditor: {
    editField: "Ändra fält",
    moveUp: "Flytta upp",
    moveDown: "Flytta ner",
    removeField: "Ta bort fält",
    addFieldAbove: "Lägg till fält ovan",
    addField: "Lägg till fält",
    save: "Spara formulär",
    cancel: "Gå tillbaka utan att spara",
    open: "Öppna formulär",
    saveFailedErrorMessage:
      "Något gick fel när formuläret sparades. Det kan finnas ytterligare information i JavaScript-konsolen.",

    tabs: {
      design: "Ändra",
      preview: "Förhandsvisning",
      properties: "Inställningar",
    },

    attributes: {
      title: {
        title: "Titel",
        helpText: "Människoläsbar titel. Visas för slutanvändaren.",
      },
      description: {
        title: "Beskrivning",
        helpText: "Visas ovanför formuläret.",
      },
      thankYouMessage: {
        title: "Tack meddelande",
        helpText:
          "Visas efter att formuläret har skickats. Om ett tackmeddelande inte är inställt visas standardmeddelandet.",
      },
    },

    editFieldForm: {
      slug: {
        title: "Tekniskt namn",
        helpText: UNSURE(
          "Maskinläsbart fältnamn. Giltiga tecken: bokstäverna A-Za-z, siffrorna 0-9, understreck _. Får inte börja med en siffra. Måste vara densamma i alla språkversioner.",
        ),
      },
      title: {
        title: "Titel",
        helpText:
          "Människligt läsbar fältetikett. Om den inte är inställd, används fältnamn som standard.",
      },
      helpText: {
        title: "Hjälptext",
        helpText: "Visas under fältet.",
      },
      required: {
        title: "Obligatoriskt",
      },
      choices: UNTRANSLATED({
        title: "Choices",
        helpText:
          'Each line should contain one choice in the form of "slug: Choice shown to the user".',
      }),
      questions: UNTRANSLATED({
        title: "Questions",
        helpText:
          'Each line should contain one question in the form of "slug: Question shown to the user".',
      }),
      encryptTo: UNTRANSLATED({
        title: "Encrypt to",
        helpText:
          "If you want to encrypt the responses to this field, enter the user names of users who should be able to decrypt the responses (one per line). These users must have a key pair generated in their profile.",
      }),
    },

    fieldTypes: {
      SingleLineText: "Textfält med en rad",
      MultiLineText: " Textfält med flera rader",
      Divider: "Separatorlinje",
      StaticText: "Statisk text",
      Spacer: "Tomt utrymme",
      SingleCheckbox: "Enkel kryssruta",
      SingleSelect: "Listrutan (ett val)",
      MultiSelect: "Listrutan (flera val)",
      RadioMatrix: "Urvalsmatris",
      FileUpload: "Skicka fil",
      NumberField: "Nummer",
      DecimalField: "Decimal",
      DateField: "Datum",
      DateTimeField: "Datum och tid",
      TimeField: "Tid",
    },

    removeFieldModal: {
      title: "Bekräfta borttagning av fält",
      message: "Ta bort det valda fältet?",
      actions: {
        submit: "Ta bort",
        cancel: "Avbryt",
      },
    },

    editFieldModal: {
      title: "Redigera fält",
      actions: {
        submit: "Spara fältet",
        cancel: "Avbryt",
      },
    },
  },

  SplashView: {
    engagement: (
      <>
        Stanna kvar medan vi återimplementerar nyckelfunktionerna i{" "}
        <strong style={{ whiteSpace: "nowrap" }}>
          Kompassi Event Management System
        </strong>{" "}
        använder modern webbteknik för bättre användarupplevelse och bättre
        anpassning för självbetjäning!
      </>
    ),
    backToKompassi: "Tillbaka till Kompassi",
  },

  EventsView: {
    title: "Evenemang",
  },

  TicketsView: {
    title: "Köp biljetter",
    forEvent: (eventName: string) => <>till {eventName}</>,
    noProducts: UNSURE({
      title: "Inga produkter tillgängliga",
      message: "Det finns inga produkter tillgängliga för köp för tillfället.",
    }),
    productsTable: {
      product: "Produkt",
      price: "Pris",
      quantity: "Antal",
    },
    contactForm: UNSURE({
      title: "Kontaktinformation",
      fields: {
        firstName: {
          title: "Förnamn",
        },
        lastName: {
          title: "Efternamn",
        },
        email: {
          title: "E-post",
          helpText:
            "Kontrollera e-postadressen noggrant! Dina biljetter skickas till denna adress.",
        },
        phone: {
          title: "Telefonnummer",
        },
      },
    }),
    purchaseButtonText: "Köp",
    acceptTermsAndConditions(url: string) {
      return (
        <>
          Jag accepterar{" "}
          <a href={url} target="_blank" rel="noopener noreferrer">
            Villkor
          </a>{" "}
          (nödvändig).
        </>
      );
    },
  },

  Program: UNSURE({
    listTitle: "Program",
    singleTitle: "Program",
    inEvent: (eventName: string) => <>i {eventName}</>,
    attributes: {
      title: "Rubrik",
      placeAndTime: "Plats och tid",
      actions: "Funktioner",
    },
    actions: {
      returnToProgramList: (eventName: string) =>
        `Tillbaka till programmet för ${eventName}`,
      addTheseToCalendar: "Lägg till dessa program i kalendern",
      addThisToCalendar: "Lägg till detta program i kalendern",
      signUpForThisProgram: "Anmäl dig till detta program",
    },
    favorites: {
      markAsFavorite: "Markera som favorit",
      unmarkAsFavorite: "Avmarkera som favorit",
      signInToAddFavorites:
        "Genom att logga in kan du markera program som favoriter, filtrera program efter favoriter och lägga till dina favoritprogram i kalendern.",
    },
    filters: {
      showOnlyFavorites: "Visa endast favoriter",
      hidePastPrograms: "Dölj förflutna program",
    },
    tabs: {
      cards: "Kort",
      table: "Tabell",
    },
    feedback: UNSURE({
      viewTitle: "Ge feedback",
      notAcceptingFeedback: "Det här programmet tar inte emot feedback.",
      fields: {
        feedback: {
          title: "Feedback",
          helpText:
            "Hur gillade du programmet? Var snäll och konstruktiv och empatisk mot programvärdarna :) Din feedback kommer att delas med programvärdarna.",
        },
        kissa: {
          title: "Vilket djur säger mjau?",
          helpText:
            "Vänligen svara för att bevisa att du inte är en robot. Tips: Katt.",
        },
      },
      actions: {
        returnToProgram: "Tillbaka till programmet",
        submit: "Skicka feedback",
      },
      anonymity: {
        title: "Koppla ditt svar till dig",
        description:
          "Om du ger feedback på programmet medan du är inloggad kommer ditt användarkonto att kopplas till din feedback. Ditt användarkonto kommer dock inte att delas med programvärdarna.",
      },
      thankYou: {
        title: "Tack för din feedback!",
        description: "Din feedback har registrerats.",
      },
    }),
  }),

  NewProgramView: {
    title: "Erbjud ett program",
    engagement: (eventName: string) => (
      <>
        Tack för ditt intresse för att erbjuda program till {eventName}! Snälla
        börja med att välja vilken typ av program du vill erbjuda nedan.
      </>
    ),
    selectThisProgramType: "Välj denna programtyp",
    backToProgramFormSelection: "Tillbaka till val av programtyp",
    forEvent: (eventName: string) => <>för {eventName}</>,
    submit: "Skicka",
  },

  Survey: {
    listTitle: "Enkäter",
    singleTitle: "Enkät",
    forEvent: (eventName: string) => <>för {eventName}</>,
    surveyTableFooter: (count: number) => (
      <>
        {count} enkät{count === 1 ? "" : "er"}.
      </>
    ),
    responseListTitle: "Svar",
    responseDetailTitle: "Svar",
    ownResponsesTitle: "Mina svar",
    showingResponses: (filteredCount: number, totalCount: number) => (
      <>
        Visar {filteredCount} svar (totalt {totalCount}).
      </>
    ),
    dimensionTableFooter: (countDimensions: number, countValues: number) => (
      <>
        Total {countDimensions} dimension{countDimensions === 1 ? "" : "er"},{" "}
        {countValues} värde{countValues === 1 ? "" : "er"}.
      </>
    ),
    summaryOf: (filteredCount: number, totalCount: number) => (
      <>
        Sammanfattning av {filteredCount} svar (totalt {totalCount}).
      </>
    ),
    theseProfileFieldsWillBeShared: UNSURE(
      "Då du skickar in denna enkät, kommer följande information att delas med enkätägaren:",
    ),
    correctInYourProfile: UNSURE((profileLink: string) => (
      <>
        Om dessa uppgifter inte är korrekta, vänligen korrigera dem i din{" "}
        <a href={profileLink} target="_blank" rel="noopener noreferrer">
          profil
        </a>{" "}
        (öppnas i ny flik).
      </>
    )),

    attributes: {
      slug: {
        title: "Tekniskt namn",
        helpText:
          "Ett maskinläsbart namn för frågan. Det tekniska namnet måste vara unikt för evenemanget. Det tekniska namnet kan inte ändras efter skapande.",
      },
      title: "Titel",
      isActive: {
        title: "Tar emot svar",
        untilFurtherNotice: "Öppet tills vidare",
        untilTime: (formattedTime) => `Öppet till ${formattedTime}`,
        openingAt: (formattedTime) => `Öppnar vid ${formattedTime}`,
        closed: "Stängt",
      },
      activeFrom: {
        title: "Öppet från",
        helpText:
          "Om detta är inställt kommer enkäten att börja acceptera svar vid denna tidpunkt.",
      },
      activeUntil: {
        title: "Stänger",
        helpText:
          "Om detta är inställt kommer enkäten att sluta acceptera svar vid denna tidpunkt.",
      },
      countResponses: "Svaren",
      languages: "Språk",
      actions: "Actions",
      anonymity: {
        secondPerson: {
          title: "Koppla ditt svar till dig",
          choices: {
            HARD: "Svaren är anonyma. Du kan inte återvända för att se eller redigera dina svar.",
            SOFT: "Om du svarar på den här enkäten medan du är inloggad kommer den att kopplas till ditt användarkonto, så att du kan återvända för att se eller redigera dina svar, men din identitet kommer inte att delas med enkätägaren.",
            NAME_AND_EMAIL:
              "Om du svarar på den här enkäten medan du är inloggad kommer den att kopplas till ditt användarkonto. Ditt namn och e-postadress kommer att delas med enkätägaren. Du kan återvända för att se eller redigera dina svar.",
          },
        },
        thirdPerson: {
          title: "Koppla svar till användare",
          choices: {
            HARD: "Svaren är anonyma. Användare kan inte återvända för att se eller redigera sina svar.",
            SOFT: "Om användaren svarar på den här enkäten medan hen är inloggad kommer deras svar att kopplas till deras användarkonto, så att de kan återvända för att se eller redigera sina svar, men deras identiteter kommer inte att delas med dig.",
            NAME_AND_EMAIL:
              "Om användaren svarar på den här enkäten medan hen är inloggad kommer deras svar att kopplas till deras användarkonto. Deras namn och e-postadresser kommer att delas med dig. De kan återvända för att se eller redigera sina svar.",
          },
        },
      },
      dimensions: "Dimensionerna",
      dimension: "Dimension",
      values: "Värden",
      value: "Värde",
      sequenceNumber: "Sekvensnummer",
      createdAt: "Sändningstid",
      createdBy: "Avsändare",
      event: "Evenemang",
      formTitle: "Enkätens titel",
      language: "Språk",
      choice: "Val",
      question: "Fråga",
      countMissingResponses: "Inget svar",
      percentageOfResponses: "Andel av svar",
      technicalDetails: "Tekniska detaljer",
      loginRequired: {
        title: "Inloggning krävs",
        helpText:
          "Om detta väljs, kräver det att du loggar in för att svara på enkäten.",
      },
      maxResponsesPerUser: {
        title: "Maximalt antal svar per användaren",
        helpText:
          "Det maximala antalet svar från en enskild användare på denna enkät. Om värdet är satt till 0 är beloppet inte begränsat. Observera att detta endast påverkar inloggade användare. För att begränsningen ska fungera måste svaret på enkäten begränsas till inloggade användare.",
      },
    },
    actions: {
      createSurvey: "Skapa en enkät",
      fillIn: {
        title: "Fyll i",
        disabledTooltip: "Stängd enkät kan inte fyllas i",
      },
      share: {
        title: "Dela",
        tooltip: "Kopiera länk till urklipp",
        success: "En länk till enkäten har kopierats till urklipp.",
      },
      viewResponses: "Visa svar",
      toggleSubscription: "Meddela mig om nya svar",
      submit: "Skicka",
      downloadAsExcel: "Ladda ner som Excel",
      returnToResponseList: "Tillbaka till listan över svar",
      returnToSurveyList: "Tillbaka till listan över enkäter",
      returnToDimensionList: "Tillbaka till dimensionslistan",
      saveDimensions: "Spara dimensioner",
      saveProperties: "Spara inställningar",
      addDimension: "Lägg till dimension",
      addDimensionValue: "Lägg till värde",
      deleteDimension: {
        title: "Radera dimension",
        cannotRemove:
          "En dimension kan inte raderas om den redan är kopplad till en enkät.",
        confirmation: (dimensionTitle: string) => (
          <>
            Radera dimension <strong>{dimensionTitle}</strong> med alla val?
          </>
        ),
        modalActions: {
          submit: "Radera",
          cancel: "Avbryt",
        },
      },
      deleteDimensionValue: {
        title: "Radera val",
        cannotRemove:
          "Ett val kan inte raderas om det redan är kopplat till en enkät.",
        confirmation: (dimensionTitle: string, valueTitle: string) => (
          <>
            Radera val <strong>{dimensionTitle}</strong> från dimensionen{" "}
            <strong>{valueTitle}</strong>?
          </>
        ),
      },
      deleteSurvey: {
        title: "Radera enkät",
        cannotRemove: "En enkät som redan har fått svar kan inte raderas.",
        confirmation: (surveyTitle: string) => (
          <>
            Är du säker på att du vill ta bort enkäten{" "}
            <strong>{surveyTitle}</strong>?
          </>
        ),
        modalActions: {
          submit: "Radera",
          cancel: "Avbryt",
        },
      },
      editDimension: "Ändra dimensionen",
      editDimensionValue: "Ändra val",
      editSurvey: "Ändra",
    },
    tabs: {
      summary: "Sammanfattning",
      responses: "Svaren",
      properties: "Frågeinställningar",
      addLanguage: "Lägg till språkversion",
      texts: (languageName: string) => `Texter (${languageName})`,
      fields: (languageName: string) => `Fält (${languageName})`,
    },
    thankYou: {
      title: "Tack för dina svar!",
      defaultMessage:
        "Dina svar har registrerats. Du kan nu stänga den här fliken.",
    },
    maxResponsesPerUserReached: {
      title: "Maximalt antal svar nått",
      defaultMessage: (
        maxResponsesPerUser: number,
        countResponsesByCurrentUser: number,
      ) =>
        `Du har redan skickat ${countResponsesByCurrentUser} svar${
          countResponsesByCurrentUser === 1 ? "" : "en"
        } till denna undersökning. Det maximala antalet svar per användare är ${maxResponsesPerUser}.`,
    },
    warnings: {
      choiceNotFound:
        "Valet hittades inte. Det kan ha tagits bort efter att detta svar skickades.",
    },
    checkbox: {
      checked: "Valt",
      unchecked: "Icke valt",
    },
    addLanguageModal: {
      language: {
        title: "Språk",
        helpText: "Endast språk som stöds kan läggas till.",
      },
      copyFrom: {
        title: "Börja från språkversionen",
        helpText:
          "En ny språkversion skapas baserat på den valda språkversionen. Du kan också välja att börja med ett tomt formulär.",
      },
      actions: {
        submit: "Fortsätt",
        cancel: "Avbryt",
      },
    },
    deleteLanguageModal: {
      title: "Radera språkversionen",
      confirmation: (languageName: string) => (
        <>
          Är du säker på att du vill radera språkversionen{" "}
          <strong>{languageName}</strong>?
        </>
      ),
      modalActions: {
        submit: "Radera",
        cancel: "Avbryt",
      },
    },
    editDimensionModal: {
      editTitle: "Ändra dimensionen",
      addTitle: "Lägg till dimensionen",
      actions: {
        submit: "Spara dimensionen",
        cancel: "Avbryt",
      },
      attributes: {
        slug: {
          title: "Tekniskt namn",
          // TODO add pattern for slug and document it in helpText
          helpText:
            "Ett maskinläsbart, kort namn på en dimension. Det tekniska namnet kan inte ändras efter att dimensionen har skapats.",
        },
        localizedTitleHeader: {
          title: "Lokaliserade titlar",
          helpText:
            "Du kan ge dimensionen en titel på olika språk. Titeln behöver inte anges på alla språk som stöds: om titeln inte anges på det valda språket används standardspråket istället, och om det inte heller är inställt, det tekniska namnet.",
        },
        title: {
          fi: "Titeln på finska",
          en: "Titeln på engelska",
          sv: "Titeln på svenska",
        },
        isKeyDimension: {
          title: "Nyckeldimension",
          helpText: "Val för nyckeldimensionerna visas i svarslistan.",
        },
        isMultiValue: {
          title: "Flera val",
          helpText: "Om markerad kan flera värden väljas för denna dimension.",
        },
        isShownToRespondent: {
          title: "Visas för respondenten",
          helpText:
            "Om detta är valt kommer värdena för denna dimension att visas för respondenten i den individuella svarsvyn i deras profil. Om den här dimensionen dessutom är en nyckeldimension kommer den att visas i profilsvarslistan.",
        },
      },
    },
    editValueModal: {
      editTitle: "Ändra val",
      addTitle: "Lägg till val",
      actions: {
        submit: "Spara val",
        cancel: "Avbryt",
      },
      attributes: {
        slug: {
          title: "Tekniskt namn",
          // TODO add pattern for slug and document it in helpText
          helpText:
            "Ett maskinläsbart, kort namn på en dimension. Det tekniska namnet kan inte ändras efter att dimensionen har skapats.",
        },
        color: UNSURE({
          title: "Färg",
          helpText:
            "Färgen på värdet i svarslistan. Använd ljusa färger: de kommer att ljusas upp eller mörkas efter behov.",
        }),
        isInitial: UNTRANSLATED({
          title: "Initial value",
          helpText: "If set, this value will be applied to all new responses.",
        }),
        localizedTitleHeader: {
          title: "Titel lokaliserad",
          helpText:
            "Du kan ge dimensionen en titel på olika språk. Titeln behöver inte anges på alla språk som stöds: om titeln inte anges på det valda språket används standardspråket istället, och om det inte heller är inställt, det tekniska namnet.",
        },
        title: {
          fi: "Titeln på finska",
          en: "Titeln på engelska",
          sv: "Titeln på svenska",
        },
      },
    },
    createSurveyModal: {
      title: "Skapa ny enkät",
      actions: {
        submit: "Skapa",
        cancel: "Avbryt",
      },
    },
    editSurveyPage: {
      title: "Ändra enkät",
      actions: {
        submit: "Spara fält",
      },
    },
  },

  SignInRequired: {
    metadata: {
      title: "Inloggning krävs – Kompassi",
    },
    title: "Inloggning krävs",
    message: "Du måste logga in för att visa den här sidan.",
    signIn: "Logga in",
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
      fi: "finska",
      en: "engelska",
      sv: "svenska",
    },
    // NOTE: value always in target language
    switchTo: {
      fi: "Suomeksi",
      en: "In English",
      sv: "På svenska",
    },
  },
};

export default translations;
