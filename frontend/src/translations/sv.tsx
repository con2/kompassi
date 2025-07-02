// Translators: Kirsi Västi, Calle Tengman, Santtu Pajukanta

import { ReactNode, JSX } from "react";
import en, { Translations } from "./en";

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
      close: "Stäng",
    },
    boolean: {
      true: "Ja",
      false: "Nej",
    },
  },
  Profile: UNTRANSLATED(en.Profile),
  TransferConsentForm: UNTRANSLATED(en.TransferConsentForm),
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
    tickets: "Biljetter",
    responses: "Enkätsvar",
    keys: UNSURE("Krypteringsnycklar"),
    program: "Program",
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

    editFieldForm: UNTRANSLATED(en.FormEditor.editFieldForm),

    fieldTypes: {
      SingleLineText: "Textfält med en rad",
      MultiLineText: "Textfält med flera rader",
      Divider: "Separatorlinje",
      StaticText: "Statisk text",
      Spacer: "Tomt utrymme",
      SingleCheckbox: "Enkel kryssruta",
      DimensionSingleCheckbox: "Enkel kryssruta för en dimension",
      SingleSelect: "Listrutan (ett val)",
      DimensionSingleSelect: "Listrutan (ett val från en dimension)",
      MultiSelect: "Listrutan (flera val)",
      DimensionMultiSelect: "Listrutan (flera val från en dimension)",
      RadioMatrix: "Urvalsmatris",
      FileUpload: "Skicka fil",
      NumberField: "Nummer",
      DecimalField: "Decimal",
      DateField: "Datum",
      DateTimeField: "Datum och tid",
      TimeField: "Tid",
      MultiItemField: UNSURE("Fält med flera poster"),
    },
    advancedFieldTypes: UNTRANSLATED(en.FormEditor.advancedFieldTypes),

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

  Tickets: UNTRANSLATED(en.Tickets),

  Program: UNSURE({
    listTitle: "Program",
    adminListTitle: UNTRANSLATED("Program items"),
    singleTitle: "Program",
    ownListTitle: "Mina program",
    inEvent: (eventName: string) => <>i {eventName}</>,
    tableFooter: (numPrograms: number) => `${numPrograms} program.`,
    attributes: {
      slug: {
        title: "Tekniskt namn",
        helpText: UNTRANSLATED(en.Program.attributes.slug.helpText),
      },
      event: "Evenemang",
      title: "Rubrik",
      actions: "Funktioner",
      description: "Beskrivning",
      state: {
        title: "Status",
        choices: {
          new: "Ny",
          accepted: "Godkänd",
        },
      },
      programOffer: {
        title: "Programerbjudande",
        message: "Det här programmet har skapats från ett programerbjudande:",
      },
      programHosts: UNTRANSLATED(en.Program.attributes.programHosts),
      scheduleItems: {
        title: "Programtider",
      },
    },
    actions: {
      ...UNTRANSLATED(en.Program.actions),
      returnToProgramList: (eventName: string) =>
        `Tillbaka till programmet för ${eventName}`,
      returnToProgramAdminList: (eventName: string) =>
        `Tillbaka till programmet för ${eventName}`,
      addTheseToCalendar: "Lägg till dessa program i kalendern",
      addThisToCalendar: "Lägg till detta program i kalendern",
      signUpForThisProgram: "Anmäl dig till detta program",
    },
    messages: UNTRANSLATED(en.Program.messages),
    errors: {
      failedToCreate: "Programmet kunde inte skapas.",
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

    adminDetailTabs: UNTRANSLATED(en.Program.adminDetailTabs),
    profile: UNTRANSLATED(en.Program.profile),
    ProgramForm: UNTRANSLATED(en.Program.ProgramForm),
    ProgramOffer: UNTRANSLATED(en.Program.ProgramOffer),
    ProgramHost: UNTRANSLATED(en.Program.ProgramHost),
    ScheduleItem: UNTRANSLATED(en.Program.ScheduleItem),

    admin: {
      title: "Program admin",
    },
  }),

  Dimension: {
    listTitle: "Dimensioner",
  },

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
    tableFooter: (count: number) => (
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
    attributes: {
      slug: {
        title: "Tekniskt namn",
        helpText: UNTRANSLATED(en.Survey.attributes.slug.helpText),
      },
      title: "Titel",
      isActive: {
        title: "Tar emot svar",
        untilFurtherNotice: "Öppet tills vidare",
        untilTime: (formattedTime) => `Öppet till ${formattedTime}`,
        openingAt: (formattedTime) => `Öppnar vid ${formattedTime}`,
        closed: "Stängt",
        adminOverride: UNTRANSLATED(
          en.Survey.attributes.isActive.adminOverride,
        ),
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
      responsesEditableUntil: UNTRANSLATED(
        en.Survey.attributes.responsesEditableUntil,
      ),
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
            FULL_PROFILE:
              "Om du svarar på den här enkäten medan du är inloggad kommer den att kopplas till ditt användarkonto. Din fullständiga profilinformation kommer att delas med enkätägaren. Du kan återvända för att se eller redigera dina svar.",
          },
        },
        thirdPerson: {
          title: "Koppla svar till användare",
          choices: {
            HARD: "Svaren är anonyma. Användare kan inte återvända för att se eller redigera sina svar.",
            SOFT: "Om användaren svarar på den här enkäten medan hen är inloggad kommer deras svar att kopplas till deras användarkonto, så att de kan återvända för att se eller redigera sina svar, men deras identiteter kommer inte att delas med dig.",
            NAME_AND_EMAIL:
              "Om användaren svarar på den här enkäten medan hen är inloggad kommer deras svar att kopplas till deras användarkonto. Deras namn och e-postadresser kommer att delas med dig. De kan återvända för att se eller redigera sina svar.",
            FULL_PROFILE:
              "Om användaren svarar på den här enkäten medan hen är inloggad kommer deras svar att kopplas till deras användarkonto. Deras fullständiga profilinformation kommer att delas med dig. De kan återvända för att se eller redigera sina svar.",
          },
        },
        admin: UNTRANSLATED(en.Survey.attributes.anonymity.admin),
      },
      dimensions: "Dimensionerna",
      dimension: "Dimension",
      dimensionDefaults: UNTRANSLATED(en.Survey.attributes.dimensionDefaults),
      values: "Värden",
      value: "Värde",
      sequenceNumber: "Sekvensnummer",
      versionHistory: "Versionshistorik",
      currentVersionCreatedAt: "Den aktuella versionen skapades",
      currentVersionCreatedBy: "Den aktuella versionen skapades av",
      originalCreatedAt: "Sändningstid",
      originalCreatedBy: "Avsändare",
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
      protectResponses: {
        title: "Skydda svar",
        helpText: UNSURE("Om detta väljs, kan svar inte raderas."),
      },
      maxResponsesPerUser: {
        title: "Maximalt antal svar per användaren",
        helpText:
          "Det maximala antalet svar från en enskild användare på denna enkät. Om värdet är satt till 0 är beloppet inte begränsat. Observera att detta endast påverkar inloggade användare. För att begränsningen ska fungera måste svaret på enkäten begränsas till inloggade användare.",
      },
      alsoAvailableInThisLanguage: UNSURE(
        (
          LanguageLink: ({ children }: { children: ReactNode }) => JSX.Element,
        ) => (
          <>
            Den här blanketten finns också{" "}
            <LanguageLink>på svenska</LanguageLink>.
          </>
        ),
      ),
      cloneFrom: UNTRANSLATED(en.Survey.attributes.cloneFrom),
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
      viewResponse: {
        title: "Visa svaret",
        label: "Visa",
      },
      viewResponses: "Visa svar",
      toggleSubscription: "Meddela mig om nya svar",
      submit: "Skicka",
      deleteVisibleResponses: UNSURE({
        title: "Radera svar",
        confirmation: (countResponses: number) => (
          <>
            Är du säker på att du vill radera de{" "}
            <strong>{countResponses}</strong> svaren som syns?
          </>
        ),
        noResponsesToDelete: "Inga svar att radera.",
        responsesProtected: UNTRANSLATED(
          "The responses to this survey are protected. To remove, disable response protection from query settings first.",
        ),
        cannotDelete: "De här svaren kan inte raderas.",
        modalActions: {
          submit: "Radera svar",
          cancel: "Avbryt utan att radera",
        },
      }),
      deleteResponse: UNSURE({
        title: "Radera svaret",
        confirmation: "Är du säker på att du vill radera det här svaret?",
        cannotDelete: "Det här svaret kan inte raderas.",
        modalActions: {
          submit: "Radera svaret",
          cancel: "Avbryt utan att radera",
        },
      }),
      editResponse: UNTRANSLATED(en.Survey.actions.editResponse),
      exportDropdown: {
        dropdownHeader: "Ladda ner svar",
        excel: "Ladda ner som Excel",
        zip: "Ladda ner med bilagor (zip)",
      },
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
      editDimensions: "Ändra dimensioner och val",
      editDimension: "Ändra dimensionen",
      editDimensionValue: "Ändra val",
      editSurvey: "Ändra",
      viewProfile: UNTRANSLATED(en.Survey.actions.viewProfile),
    },
    errors: UNTRANSLATED(en.Survey.errors),
    messages: UNTRANSLATED(en.Survey.messages),
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
    specialPurposeSurvey: UNTRANSLATED(en.Survey.specialPurposeSurvey),
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
    editDimensionModal: UNTRANSLATED(en.Survey.editDimensionModal),
    editValueModal: UNTRANSLATED(en.Survey.editValueModal),
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
    ResponseHistory: UNTRANSLATED(en.Survey.ResponseHistory),
    OldVersionAlert: UNTRANSLATED(en.Survey.OldVersionAlert),
  },

  Involvement: UNTRANSLATED(en.Involvement),
  Invitation: UNTRANSLATED(en.Invitation),

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
