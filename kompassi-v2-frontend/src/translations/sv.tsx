// Translators: Kirsi Västi, Calle Tengman, Luka Pajukanta, Claude Sonnet 4.6

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
      save: "Spara",
      open: "Öppna",
      edit: "Ändra",
      delete: "Radera",
      create: "Skapa",
      close: "Stäng",
    },
  },
  Profile: {
    singleTitle: "Profil",
    attributes: {
      displayName: "Namn",
      firstName: "Förnamn",
      lastName: "Efternamn",
      nick: "Smeknamn",
      phoneNumber: "Telefonnummer",
      email: "E-postadress",
      discordHandle: "Discord-användarnamn",
    },
    advancedAttributes: {
      displayName: { title: "Namn" },
      firstName: { title: "Förnamn" },
      lastName: { title: "Efternamn" },
      nick: { title: "Smeknamn" },
      phoneNumber: { title: "Telefonnummer" },
      email: { title: "E-postadress" },
      discordHandle: { title: "Discord-användarnamn" },
    },
    keysView: {
      title: "Krypteringsnycklar",
      description:
        "I vissa fall krypteras konfidentiell data i Kompassi med asymmetrisk kryptering. " +
        "Om du behöver vara mottagare av sådan konfidentiell information måste du ha ett nyckelpar. " +
        "Du kan generera ett nedan. " +
        "Generering av ett nyckelpar kräver ditt lösenord eftersom den privata nyckeln krypteras med det. " +
        "I framtiden kommer vi att tillåta avancerade användare att använda nycklar som lagras enbart på deras egna enheter, " +
        "så att den privata nyckeln aldrig lämnar enheten.",
      resetPasswordWarning: (
        <>
          <strong>Varning!</strong> Om du glömmer ditt lösenord och återställer
          det förlorar du dina krypteringsnycklar och kan inte längre komma åt
          data som krypterats till dem.
        </>
      ),
      attributes: {
        id: { title: "Nyckel-ID" },
        createdAt: { title: "Skapad" },
        actions: { title: "Funktioner" },
        password: {
          title: "Lösenord",
          helpText: "Ange ditt lösenord för att kryptera den privata nyckeln.",
        },
      },
      actions: {
        generate: {
          title: "Generera nyckelpar",
          enterPassword:
            "Ange ditt lösenord för att kryptera den privata nyckeln.",
          modalActions: {
            submit: "Generera",
            cancel: "Avbryt",
          },
        },
        revoke: {
          title: "Återkalla nyckelpar",
          confirmation: (formattedCreatedAt: string) => (
            <>
              Är du säker på att du vill återkalla nyckelparet som skapades{" "}
              <strong>{formattedCreatedAt}</strong>? När det har återkallats
              kommer information som krypterades med den privata nyckeln inte
              längre att vara tillgänglig. Denna åtgärd kan inte ångras.
            </>
          ),
          modalActions: {
            submit: "Återkalla",
            cancel: "Avbryt",
          },
        },
      },
    },
  },
  TransferConsentForm: {
    title: "Överföring av personuppgifter",
    message: (
      <>
        När du fyller i det här formuläret överförs dina personuppgifter enligt
        beskrivningen nedan. Personuppgifter du anger i formuläret nedan
        behandlas även av mottagaren.
      </>
    ),
    messageAlreadyAccepted: (
      <>
        När du fyllde i det här formuläret överfördes dina personuppgifter
        enligt beskrivningen nedan. Personuppgifter du angav i formuläret
        behandlades även av mottagaren.
      </>
    ),
    consentCheckBox:
      "Jag godkänner överföringen och behandlingen av mina personuppgifter enligt ovan.",
    consentAlreadyGivenAt: (formattedDate: ReactNode) => (
      <>
        Du har godkänt överföringen och behandlingen av dina personuppgifter
        enligt ovan den {formattedDate}.
      </>
    ),
    privacyPolicy: "Integritetspolicy",
    privacyPolicyMissing: "Integritetspolicy saknas",
    actions: {
      editProfile: {
        message: "Om du hittar fel, rätta dem i din profil.",
        link: "Ändra profil",
      },
    },
    sourceRegistry: "Källa för personuppgifter",
    targetRegistry: "Mottagare av personuppgifter",
    dataToBeTransferred: "Personuppgifter som överförs",
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
    tickets: "Biljetter",
    responses: "Enkätsvar",
    keys: "Krypteringsnycklar",
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
      dateOutOfRange:
        "Det valda datumet är utanför evenemangets datumintervall.",
    },
    boolean: {
      true: "Ja",
      false: "Nej",
    },
    checkbox: {
      checked: "Valt",
      unchecked: "Icke valt",
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
        helpText:
          "Maskinläsbart fältnamn. Giltiga tecken: gemener a-z, siffror 0-9, understreck _. Får inte börja med en siffra. Det tekniska namnet måste vara detsamma i alla språkversioner.",
      },
      title: {
        title: "Titel",
        helpText:
          "Människoläsbar fältetikett. Om den inte anges används fältnamnet.",
      },
      helpText: {
        title: "Hjälptext",
        helpText: "Visas under fältet.",
      },
      required: {
        title: "Obligatoriskt",
      },
      choices: {
        title: "Val",
        helpText:
          'Varje rad måste innehålla ett val i formatet "rad-slug: Val som visas för användaren". Sluggen kan innehålla gemener a-z, siffror och bindestreck (-). Varje rad måste ha en unik slug.',
      },
      questions: {
        title: "Frågor",
        helpText:
          'Varje rad måste innehålla en fråga i formatet "rad-slug: Text som visas för användaren". Sluggen kan innehålla gemener a-z, siffror och bindestreck (-). Varje rad måste ha en unik slug.',
      },
      dimension: {
        title: "Dimension",
        helpText: "Vilken dimension ska fältet hämta sina val från?",
      },
      encryptTo: {
        title: "Kryptera till",
        helpText:
          "Om du vill kryptera svaren till detta fält, ange användarnamnen på användare som ska kunna dekryptera svaren (ett per rad). Dessa användare måste ha ett nyckelpar genererat i sin profil.",
      },
    },

    fieldTypes: {
      SingleLineText: "Textfält med en rad",
      MultiLineText: "Textfält med flera rader",
      Divider: "Separatorlinje",
      StaticText: "Statisk text",
      Spacer: "Tomt utrymme",
      SingleCheckbox: "Enkel kryssruta",
      Tristate: "Tristate (ja/nej/inte angiven)",
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
      MultiItemField: "Fält med flera poster",
    },
    advancedFieldTypes: {
      SingleSelect: {
        promoteFieldToDimension: {
          title: "Konvertera till ett dimensionsfält",
          modalActions: {
            submit: "Fortsätt med konverteringen",
            cancel: "Avbryt utan att konvertera",
          },
          existingDimension: (
            <>
              <p>
                Är du säker på att du vill konvertera detta fält till ett
                dimensionsfält?
              </p>
              <p>
                Om du fortsätter vidtas följande åtgärder i{" "}
                <strong>alla språkversioner</strong> av denna enkät:
              </p>
              <ol>
                <li>
                  Nya val, om sådana finns, läggs till i den befintliga
                  dimensionen med samma tekniska namn. Översättningar för dem
                  extraheras från alla befintliga språkversioner och kombineras
                  efter deras tekniska namn.
                </li>
                <li>
                  Detta fält ersätts av ett dimensionsvalsfält som hämtar sina
                  val från den nämnda dimensionen. Övriga fältattribut behålls.
                </li>
                <li>
                  Varje svar där detta fält har besvarats får svaren på detta
                  fält angivna som dimensionsvärden på det svaret.
                </li>
              </ol>
              <p>Detta kan inte ångras.</p>
            </>
          ),
          newDimension: (
            <>
              <p>
                Är du säker på att du vill konvertera detta fält till ett
                dimensionsfält?
              </p>
              <p>
                Om du fortsätter vidtas följande åtgärder i{" "}
                <strong>alla språkversioner</strong> av denna enkät:
              </p>
              <ol>
                <li>
                  En ny dimension skapas med samma tekniska namn som detta fält.
                  Val och deras översättningar extraheras från alla befintliga
                  språkversioner och kombineras efter deras tekniska namn.
                </li>
                <li>
                  Detta fält ersätts av ett dimensionsvalsfält som hämtar sina
                  val från den nämnda dimensionen. Övriga fältattribut behålls.
                </li>
                <li>
                  Varje svar där detta fält har besvarats får svaren på detta
                  fält angivna som dimensionsvärden på det svaret.
                </li>
              </ol>
              <p>Detta kan inte ångras.</p>
            </>
          ),
        },
      },
      DimensionSingleSelect: {
        description: (
          <>
            Den här fälttypen visar ett envalsfält med en lista av val som
            definieras av en dimension. När respondenten väljer ett värde för
            detta fält anges det dimensionsvärdet på svaret.
          </>
        ),
      },
      DimensionMultiSelect: {
        description: (
          <>
            Den här fälttypen visar ett flervalsfält med en lista av val som
            definieras av en dimension. När respondenten väljer värden för detta
            fält anges dessa dimensionsvärden på svaret.
          </>
        ),
      },
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

  Tickets: {
    title: "Köp biljetter",
    forEvent: (eventName: string) => <>för {eventName}</>,
    returnToTicketsPage: "Tillbaka till biljettsidan",
    Product: {
      listTitle: "Produkter",
      noProducts: {
        title: "Inga produkter tillgängliga",
        message: "Det finns inga produkter tillgängliga för köp just nu.",
      },
      actions: {
        editProduct: "Ändra produkt",
        newProduct: {
          title: "Ny produkt",
          modalActions: {
            submit: "Skapa produkt",
            cancel: "Avbryt",
          },
        },
        saveProduct: "Spara produkt",
        unpublishAllProducts: "Avpublicera alla produkter",
        viewOldVersion: {
          title: "Gammal version av produkt",
          label: "Visa gammal version",
          modalActions: {
            submit: "",
            cancel: "Stäng",
          },
        },
        deleteProduct: {
          title: "Radera produkt",
          confirmation: (productName: string) => (
            <>
              Är du säker på att du vill radera produkten{" "}
              <strong>{productName}</strong>? Åtgärden kan inte ångras.
            </>
          ),
          modalActions: {
            submit: "Radera",
            cancel: "Avbryt",
          },
          cannotDelete:
            "Den här produkten kan inte raderas eftersom den har sålts.",
        },
      },
      clientAttributes: {
        product: "Produkt",
        title: "Titel",
        createdAt: "Skapad",
        unitPrice: {
          title: "Styckpris",
          helpText: "Pris per enhet i euro.",
        },
        quantity: {
          title: "Antal",
          quantityForProduct: "Antal för produkt",
          unit: "st",
          placeholder: "Antal",
        },
        total: "Totalt",
        description: {
          title: "Beskrivning",
          helpText: "Titel och beskrivning visas för kunden på biljettsidan.",
        },
        maxPerOrder: {
          title: "Maximalt antal per beställning",
          helpText: "Högst detta antal säljs i en beställning.",
        },
        eticketsPerProduct: {
          title: "Antal e-biljetter per produkt",
          helpText:
            "Antal e-biljettkoder som genereras för varje såld produktenhet. Om 0 genereras inga e-biljetter.",
        },
        availableFrom: {
          title: "Tillgänglig från",
          helpText:
            "För att produkten ska bli tillgänglig måste detta fält vara inställt och den angivna tiden ha passerat.",
        },
        availableUntil: {
          title: "Tillgänglig till",
          helpText:
            "Om detta är inställt är produkten inte längre tillgänglig efter denna tid.",
        },
        countPaid: "Betald",
        countReserved: {
          title: "Såld",
          description:
            "Inkluderar förutom betalda beställningar även bekräftade men ännu obetalda beställningar.",
        },
        countUnpaid: "Obetald",
        countAvailable: "Kvar",
        countTotal: "Totalt",
        actions: "Funktioner",
        totalReserved: "Totalt såld",
        totalPaid: "Totalt betald",
        revisions: {
          title: "Revisioner av denna produkt",
          description:
            "Om en produkt ändras efter att ha sålts skapas en ny revision som ersätter produkten i butiken. Att ändra tillgänglighetsschema eller kvoter skapar ingen ny revision.",
          current: "Aktuell",
        },
        quotas: {
          title: "Kvoter",
          helpText:
            "Kvoter avgör hur många enheter av en produkt som får säljas. En produkt kan använda flera kvoter; den knappaste kvoten avgör tillgängligheten. Du kan redigera och skapa kvoter på fliken Kvoter.",
        },
        selectedQuotas: "Valda kvoter",
        soldOut: "Slutsåld",
        isAvailable: "Tillgänglighetsschema",
        vatPercentage: {
          title: "Momssats",
          helpText:
            "Den momssats som gäller för denna produkt. Priserna inkluderar moms.",
        },
        vatIncluded: (rate: string) => `inkl. ${rate}% moms`,
        vatBreakdown: "Momsspecifikation",
        dragToReorder: "Dra för att sortera om",
        newProductQuota: {
          title: "Kvot",
          helpText:
            "Du kan skapa en kvot med produktens namn här. Om du vill hoppa över det och ange kvoter senare kan du lämna detta tomt. En produkt måste vara kopplad till minst en kvot för att bli tillgänglig.",
        },
      },
      serverAttributes: {
        isAvailable: {
          untilFurtherNotice: "Tillgänglig tills vidare",
          untilTime: (formattedTime: string) =>
            `Tillgänglig till ${formattedTime}`,
          openingAt: (formattedTime: string) =>
            `Blir tillgänglig ${formattedTime}`,
          notAvailable: "Inte tillgänglig",
        },
      },
    },
    Quota: {
      listTitle: "Kvoter",
      singleTitle: "Kvot",
      actions: {
        newQuota: {
          title: "Ny kvot",
          modalActions: {
            submit: "Skapa kvot",
            cancel: "Avbryt",
          },
        },
        editQuota: "Ändra kvot",
        saveQuota: "Spara kvot",
        deleteQuota: {
          title: "Radera kvot",
          confirmation: (quotaName: string) => (
            <>
              Är du säker på att du vill radera kvoten{" "}
              <strong>{quotaName}</strong>? Åtgärden kan inte ångras.
            </>
          ),
          modalActions: {
            submit: "Radera",
            cancel: "Avbryt",
          },
          cannotDelete:
            "Den här kvoten kan inte raderas eftersom den är kopplad till produkter. Ta bort kopplingen till alla produkter innan du raderar.",
        },
      },
      attributes: {
        name: "Namn",
        countTotal: {
          title: "Kvot",
          helpTextNew:
            "Hur många enheter av produkter som använder denna kvot får säljas totalt.",
          helpText: (countReserved: number) =>
            `Hur många enheter av produkter som använder denna kvot får säljas totalt. För närvarande är ${countReserved} enheter sålda; kvoten kan inte sänkas under det.`,
        },
        totalReserved: "Totalt såld",
        products: {
          title: "Produkter som använder denna kvot",
          helpText:
            "En produkt kan använda flera kvoter; den knappaste kvoten avgör tillgängligheten.",
        },
      },
    },
    Order: {
      listTitle: "Beställningar",
      singleTitle: (orderNumber: string, paymentStatus: string) =>
        `Beställning ${orderNumber} (${paymentStatus})`,
      contactForm: {
        title: "Kontaktinformation",
      },
      profileMessage: (
        ProfileLink: ({ children }: { children: ReactNode }) => JSX.Element,
      ) => (
        <>
          Om du har ett användarkonto med e-postadressen du använde för
          beställningen kan du också se dina beställningar och ladda ner
          e-biljetter från din <ProfileLink>profil</ProfileLink>.
        </>
      ),
      profileMessages: {
        confirmationEmailSent: (
          <>
            Ett bekräftelsemail har skickats till din e-postadress. Kontrollera
            din inkorg och följ anvisningarna för att bekräfta din e-postadress.
          </>
        ),
        cancelled: <>Din beställning har avbokats.</>,
        emailConfirmationFailed: (
          <>E-postbekräftelse misslyckades. Försök igen senare.</>
        ),
      },
      showingOrders: (numOrdersShown: number, numTotalOrders: number) => (
        <>
          Visar {numOrdersShown} beställning
          {numOrdersShown === 1 ? "" : "ar"} (totalt {numTotalOrders}).
        </>
      ),
      noFiltersApplied: (
        ForceLink: ({ children }: { children: ReactNode }) => JSX.Element,
        numOrders: number,
      ) => (
        <>
          Ofiltrerad lista med {numOrders} beställning
          {numOrders === 1 ? "" : "ar"} dold. Avgränsa sökningen eller{" "}
          <ForceLink>använd Kraften</ForceLink>.
        </>
      ),
      attributes: {
        orderNumberAbbr: "Best. #",
        orderNumberFull: "Beställningsnummer",
        createdAt: "Beställningsdatum",
        eventName: "Evenemang",
        totalPrice: "Totalpris",
        actions: "Funktioner",
        totalOrders: (numOrders: number) => (
          <>
            Totalt {numOrders} beställning{numOrders === 1 ? "" : "ar"}.
          </>
        ),
        firstName: { title: "Förnamn" },
        lastName: { title: "Efternamn" },
        displayName: { title: "Kundnamn" },
        email: {
          title: "E-postadress",
          helpText:
            "Kontrollera e-postadressen noggrant! Dina biljetter skickas till denna adress.",
        },
        phone: { title: "Telefonnummer" },
        acceptTermsAndConditions: {
          title: "Användarvillkor godkända",
          checkboxLabel(url: string) {
            return (
              <>
                Jag godkänner{" "}
                <a href={url} target="_blank" rel="noopener noreferrer">
                  användarvillkoren
                </a>{" "}
                (obligatoriskt).
              </>
            );
          },
        },
        language: {
          title: "Språk",
          helpText: (
            <>
              Kvitto och e-biljetter skickas till den angivna e-postadressen på
              detta språk.
            </>
          ),
        },
        provider: {
          title: "Betalningsleverantör",
          choices: {
            NONE: "Ingen (nollsumma eller manuell)",
            PAYTRAIL: "Paytrail",
            STRIPE: "Stripe",
          },
        },
        status: {
          title: "Status",
          choices: {
            NOT_STARTED: {
              title: "Din beställning väntar på betalning",
              shortTitle: "Ej påbörjad",
              message:
                "Din beställning är bekräftad och produkterna är reserverade åt dig, men vi har ännu inte mottagit din betalning. Använd knappen nedan för att betala så snart som möjligt. Obetalda beställningar avbokas så småningom.",
            },
            PENDING: {
              title: "Din beställning väntar på betalning",
              shortTitle: "Väntar på betalning",
              message:
                "Din beställning är bekräftad och produkterna är reserverade åt dig, men vi har ännu inte mottagit din betalning. Använd knappen nedan för att betala så snart som möjligt. Obetalda beställningar avbokas så småningom.",
            },
            FAILED: {
              title: "Betalningen misslyckades",
              shortTitle: "Betalningen misslyckades",
              message:
                "Betalningen för din beställning misslyckades eller avbröts. Försök igen. Obetalda beställningar avbokas så småningom.",
            },
            PAID: {
              title: "Din beställning är klar!",
              shortTitle: "Betald",
              message:
                "Din beställning är betald. Du får snart ett bekräftelsemail. Om det finns e-biljetter bifogas de i mailet.",
            },
            CANCELLED: {
              title: "Din beställning har avbokats",
              shortTitle: "Avbokad",
              message:
                "Din beställning har avbokats. Om det fanns e-biljetter i beställningen har de ogiltigförklarats. Om du tror att detta är ett fel, kontakta evenemangsarrangören.",
            },
            REFUND_REQUESTED: {
              title: "Din beställning har återbetalats",
              shortTitle: "Återbetalning begärd",
              message:
                "Din beställning har återbetalats. Om det fanns e-biljetter i beställningen har de ogiltigförklarats. Om du tror att detta är ett fel, kontakta evenemangsarrangören.",
            },
            REFUND_FAILED: {
              title: "Din beställning har återbetalats",
              shortTitle: "Återbetalning misslyckades",
              message:
                "Din beställning har återbetalats. Om det fanns e-biljetter i beställningen har de ogiltigförklarats. Om du tror att detta är ett fel, kontakta evenemangsarrangören.",
            },
            REFUNDED: {
              title: "Din beställning har återbetalats",
              shortTitle: "Återbetald",
              message:
                "Din beställning har återbetalats. Om det fanns e-biljetter i beställningen har de ogiltigförklarats. Om du tror att detta är ett fel, kontakta evenemangsarrangören.",
            },
          },
        },
        products: "Produkter",
      },
      errors: {
        NOT_ENOUGH_TICKETS: {
          title: "Inte tillräckligt med biljetter",
          message:
            "En eller flera av produkterna du försökte köpa är inte längre tillgängliga i den mängd du begärde.",
        },
        INVALID_ORDER: {
          title: "Ogiltig beställning",
          message:
            "Uppgifterna du angav på beställningssidan godkändes inte. Kontrollera din beställning och försök igen.",
        },
        NO_PRODUCTS_SELECTED: {
          title: "Inga produkter valda",
          message: "Välj minst en produkt att köpa.",
        },
        UNKNOWN_ERROR: {
          title: "Fel vid behandling av beställning",
          message:
            "Ett fel uppstod vid behandlingen av din beställning. Försök igen senare.",
        },
        ORDER_NOT_FOUND: {
          title: "Beställningen hittades inte",
          message:
            "Beställningen du försöker visa finns inte eller är inte kopplad till ditt användarkonto.",
          actions: {
            returnToOrderList: "Tillbaka till beställningslistan",
            returnToTicketsPage: "Tillbaka till biljettsidan",
          },
        },
      },
      actions: {
        purchase: "Bekräfta beställning och gå till betalning",
        pay: "Betala beställning",
        viewTickets: "E-biljetter",
        viewOrderPage: "Beställningssida",
        newOrder: {
          label: "Ny beställning",
          title: "Skapa en ny beställning via administratörsgränssnittet",
          message: (
            <>
              <p>
                Här kan du skapa en ny beställning. Läs dessa anvisningar
                noggrant för att undvika misstag som kan vara synliga för kunden
                och kosta pengar {":)"}
              </p>
              <p>
                Som administratör kan du välja produkter oavsett om de är
                offentligt tillgängliga just nu. Produktens attribut{" "}
                <em>Maximalt antal per beställning</em> gäller inte.
              </p>
              <p>
                Du kan dock inte överskrida kvoterna för produkterna, dvs. det
                måste finnas tillräckligt lager för de produkter du väljer.
                Beställningar gjorda på detta sätt förbrukar kvoter precis som
                kundbeställningar via det offentliga gränssnittet.
              </p>
              <p>
                Beställningen skapas i obetalt tillstånd om priset inte är noll.
                Du kan sedan antingen hämta en länk att ge kunden för betalning
                via betalningsleverantören, eller markera beställningen som
                betald manuellt.
              </p>
              <p>
                <strong>OBS:</strong> När beställningen har betalats skickas ett
                kvitto och e-biljetter till e-postadressen kopplad till
                beställningen. Även om biljetterna inte ska levereras direkt via
                e-post till kunden, använd en riktig, fungerande e-postadress
                (t.ex. din egen) för att undvika att skada Kompassis rykte som
                e-postavsändare med onödiga studsningar.
              </p>
              <p>
                Beställningar skapade via detta gränssnitt loggas i
                granskningsloggen som kan användas för att utreda eventuella
                oegentligheter.
              </p>
            </>
          ),
          actions: {
            submit: "Skapa beställning",
          },
          errors: {
            noProducts: (
              ProductsLink: ({
                children,
              }: {
                children: ReactNode;
              }) => ReactNode,
            ) => (
              <>
                <h4>Inga produkter</h4>
                <p>
                  Det finns inga produkter för detta evenemang. Skapa produkter
                  i <ProductsLink>produktadministrationen</ProductsLink>.
                </p>
              </>
            ),
          },
        },
        search: "Sök beställningar",
        ownerCancel: {
          title: "Avboka beställning",
          label: "Avboka",
          message: (
            <>
              <p>Är du säker på att du vill avboka din beställning?</p>
              <p>Alla reserverade biljetter frigörs.</p>
              <p>
                Denna åtgärd kan inte ångras. Kontakta kundtjänst om du har
                frågor.
              </p>
            </>
          ),
          modalActions: {
            submit: "Avboka beställning",
            cancel: "Stäng utan att avboka",
          },
        },
        saveContactInformation: "Spara kontaktinformation",
        resendOrderConfirmation: {
          title: "Skicka om orderbekräftelse",
          message: (emailAddress: string) => (
            <>
              <p>
                Är du säker på att du vill skicka om orderbekräftelsen (inkl.
                e-biljetter, om det finns sådana) till kunden?
              </p>
              <p>
                Bekräftelsen skickas till följande adress:{" "}
                <strong>{emailAddress}</strong>
              </p>
              <p>
                <strong>OBS:</strong> Om du ändrar e-postadressen, kom ihåg att
                spara kontaktinformationen innan du skickar om bekräftelsen.
              </p>
            </>
          ),
          modalActions: {
            submit: "Skicka om",
            cancel: "Stäng utan att skicka om",
          },
        },
        cancelAndRefund: {
          title: "Avboka beställning och återbetala",
          label: "Återbetala",
          message: (
            <>
              <p>Är du säker på att du vill</p>
              <ol>
                <li>markera beställningen som avbokad,</li>
                <li>ogiltigförklara eventuella e-biljetter,</li>
                <li>begära att betalningsleverantören återbetalar?</li>
              </ol>
              <p>
                Vid lyckad återbetalning skickas ett återbetalningsmeddelande
                till kunden.
              </p>
              <p>
                <strong>OBS:</strong> Återbetalningen kan misslyckas om det inte
                finns tillräckliga medel insatta hos betalningsleverantören. I
                så fall behöver du föra över medel och försöka igen, eller
                genomföra återbetalningen på annat sätt.
              </p>
            </>
          ),
          modalActions: {
            submit: "Avboka beställning och begär återbetalning",
            cancel: "Stäng utan att avboka",
          },
        },
        refundCancelledOrder: {
          title: "Återbetala",
          message: (
            <>
              <p>
                Är du säker på att du vill begära att betalningsleverantören
                återbetalar?
              </p>
              <p>
                Vid lyckad återbetalning skickas ett återbetalningsmeddelande
                till kunden.
              </p>
              <p>
                <strong>OBS:</strong> Återbetalningen kan misslyckas om det inte
                finns tillräckliga medel insatta hos betalningsleverantören. I
                så fall behöver du föra över medel och försöka igen, eller
                genomföra återbetalningen på annat sätt.
              </p>
            </>
          ),
          modalActions: {
            submit: "Begär återbetalning",
            cancel: "Stäng utan att återbetala",
          },
        },
        cancelWithoutRefunding: {
          title: "Avboka utan återbetalning",
          label: "Avboka",
          message: (
            <>
              <p>Är du säker på att du vill</p>
              <ol>
                <li>markera beställningen som avbokad, och</li>
                <li>ogiltigförklara eventuella e-biljetter?</li>
              </ol>
              <p>
                <strong>OBS:</strong> Ingen automatisk återbetalning görs. Om
                betalningen behöver återbetalas helt eller delvis måste du göra
                det via betalningsleverantörens handelspanel eller använda
                funktionen &quot;Avboka och återbetala&quot;.
              </p>
              <p>
                <strong>OBS:</strong> Inget avbokningsmeddelande skickas till
                kunden. Du ansvarar för all kommunikation med kunden som krävs
                angående denna avbokning.
              </p>
            </>
          ),
          modalActions: {
            submit: "Avboka beställning utan återbetalning",
            cancel: "Stäng utan att avboka",
          },
        },
        retryRefund: {
          title: "Försök återbetalning igen",
          message: (
            <>
              <p>
                Är du säker på att du vill göra en ny begäran till
                betalningsleverantören om återbetalning?
              </p>
              <p>
                Vid lyckad återbetalning skickas ett återbetalningsmeddelande
                till kunden.
              </p>
              <p>
                <strong>OBS:</strong> Återbetalningen kan misslyckas om det inte
                finns tillräckliga medel insatta hos betalningsleverantören. I
                så fall behöver du föra över medel och försöka igen, eller
                genomföra återbetalningen på annat sätt.
              </p>
            </>
          ),
          modalActions: {
            submit: "Försök återbetalning igen",
            cancel: "Stäng utan att återbetala",
          },
        },
        refundManually: {
          title: "Återbetala manuellt",
          message: (
            <>
              <p>
                Är du säker på att du vill markera denna beställning som
                manuellt återbetald?
              </p>
              <p>
                <strong>OBS:</strong> Ingen ytterligare automatisk återbetalning
                kommer att försökas. Det är helt upp till dig att se till att
                kunden får tillbaka sina pengar.
              </p>
              <p>
                Ett meddelande skickas till kunden om att beställningen har
                avbokats och återbetalats.
              </p>
            </>
          ),
          modalActions: {
            submit: "Markera som manuellt återbetald",
            cancel: "Stäng utan att markera",
          },
        },
        markAsPaid: {
          title: "Markera som betald",
          message: (
            <>
              <p>
                Är du säker på att du vill markera denna beställning som betald?
              </p>
              <p>
                Ett kvitto skickas till kunden. Om beställningen innehåller
                e-biljetter bifogas de i kvittot.
              </p>
            </>
          ),
          modalActions: {
            submit: "Markera som betald",
            cancel: "Stäng utan att markera",
          },
        },
      },
    },
    PaymentStamp: {
      listTitle: "Betalningsstämplar",
      attributes: {
        createdAt: "Tidsstämpel",
        correlationId: "Korrelations-ID",
        type: {
          title: "Typ",
          choices: {
            ZERO_PRICE: "Nollpris",
            CREATE_PAYMENT_REQUEST: "Skapa betalning – Begäran",
            CREATE_PAYMENT_SUCCESS: "Skapa betalning – OK",
            CREATE_PAYMENT_FAILURE: "Skapa betalning – Misslyckades",
            PAYMENT_REDIRECT: "Betalningsomdirigering",
            PAYMENT_CALLBACK: "Betalningsåterkoppling",
            CANCEL_WITHOUT_REFUND: "Avboka utan återbetalning",
            CREATE_REFUND_REQUEST: "Skapa återbetalning – Begäran",
            CREATE_REFUND_SUCCESS: "Skapa återbetalning – OK",
            CREATE_REFUND_FAILURE: "Skapa återbetalning – Misslyckades",
            REFUND_CALLBACK: "Återbetalningsåterkoppling",
            MANUAL_REFUND: "Manuell återbetalning",
          },
        },
      },
      actions: {
        view: {
          title: "Visa betalningsstämpel",
          message: (
            <p>
              Betalningsstämplar innehåller teknisk information om
              betalningsprocessen. Dessa kan användas för att felsöka
              misslyckade betalningar med betalningsleverantören.
            </p>
          ),
          modalActions: {
            cancel: "Stäng",
            submit: "Det finns ingen skicka-knapp :)",
          },
        },
      },
    },
    Receipt: {
      listTitle: "Kvitton",
      attributes: {
        id: "Korrelations-ID",
        createdAt: "Skickat",
        type: {
          title: "Typ",
          choices: {
            PAID: "Orderbekräftelse",
            CANCELLED: "Avbokningsmeddelande",
            REFUNDED: "Återbetalningsmeddelande",
          },
        },
        status: {
          title: "Status",
          choices: {
            REQUESTED: "Begärd",
            PROCESSING: "Behandlas",
            FAILURE: "Misslyckades",
            SUCCESS: "Skickat",
          },
        },
      },
    },
    Code: {
      listTitle: "E-biljettkoder",
      attributes: {
        code: "Kod",
        literateCode: "Läsbar kod",
        usedOn: "Använd",
        productText: "Produkt",
        status: {
          title: "Status",
          choices: {
            UNUSED: "Oanvänd",
            USED: "Använd",
            MANUAL_INTERVENTION_REQUIRED: "Återkallad",
            BEYOND_LOGIC: "Bortom logiken",
          },
        },
      },
    },
    profile: {
      title: "Biljettbeställningar",
      message:
        "Här kan du se dina biljettbeställningar från 2025 och framåt. Du kan betala obetalda beställningar och ladda ner e-biljetter här.",
      haveUnlinkedOrders: {
        title: "Bekräfta din e-postadress för att se fler beställningar",
        message:
          "Det finns biljettbeställningar kopplade till din e-postadress som inte är länkade till ditt användarkonto. Bekräfta din e-postadress för att se dessa beställningar.",
      },
      actions: {
        confirmEmail: {
          title: "Bekräfta e-postadress",
          description:
            "Ett mail skickas till e-postadressen på ditt användarkonto. Följ anvisningarna i mailet för att bekräfta din e-postadress och se resten av dina beställningar.",
          modalActions: {
            submit: "Skicka bekräftelsemail",
            cancel: "Avbryt",
          },
        },
      },
      noOrders:
        "Det finns inga beställningar kopplade till ditt användarkonto att visa.",
    },
    admin: {
      title: "Biljettbutik – administration",
      tabs: {
        orders: "Beställningar",
        products: "Produkter",
        quotas: "Kvoter",
        reports: "Rapporter",
        ticketControl: "Biljettkontroll",
        webShop: "Webbshop",
      },
      messages: {
        orderCreated: (
          <>
            Beställningen skapades. Kom ihåg att markera den som betald om det
            behövs, eller skicka länken till beställningssidan till kunden för
            betalning via betalningsleverantören.
          </>
        ),
        failedToCreateOrder: (
          <>
            Skapandet av beställningen misslyckades. Försök igen eller kontakta
            support.
          </>
        ),
      },
    },
  },

  Program: {
    listTitle: "Program",
    adminListTitle: "Programpunkter",
    singleTitle: "Programpunkt",
    inEvent: (eventName: string) => <>i {eventName}</>,
    tableFooter: (numPrograms: number) =>
      `${numPrograms} programpunkt${numPrograms === 1 ? "" : "er"}.`,
    attributes: {
      slug: {
        title: "Tekniskt namn",
        helpText:
          "Maskinläsbart namn på programpunkten. Måste vara unikt inom evenemanget. Kan inte ändras efter att det skapats. Kan innehålla gemener, siffror och bindestreck (-). Ingår i URL:en: <code>/EVENEMANG-SLUG/programs/PROGRAM-SLUG</code> (t.ex. <code>/tracon2025/programs/opening-ceremony</code>).",
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
        message:
          "Den här programpunkten har skapats från följande programerbjudande:",
      },
      programHosts: {
        title: "Programvärdar",
      },
      scheduleItems: {
        title: "Schemapunkter",
      },
      dimensions: "Programpunktens dimensioner",
      annotations: "Ytterligare information",
      cancelled: {
        title: "Inställd",
        message: "Den här programpunkten har ställts in.",
      },
    },
    actions: {
      returnToProgramList: (eventName: string) =>
        `Tillbaka till programschemat för ${eventName}`,
      returnToProgramAdminList: (eventName: string) =>
        `Tillbaka till programpunktslistan för ${eventName}`,
      addTheseToCalendar: "Lägg till dessa programpunkter i kalendern",
      addThisToCalendar: "Lägg till denna programpunkt i kalendern",
      signUpForThisProgram: "Anmäl dig till denna programpunkt",
      preview: "Förhandsgranska schema",
      preferences: "Inställningar",
      create: {
        title: "Skapa programpunkt",
        modalActions: {
          submit: "Skapa",
          cancel: "Avbryt",
        },
      },
      cancel: {
        title: "Ställ in eller ta bort en programpunkt",
        label: "Ställ in eller ta bort",
        message: (
          <>
            <p>Vill du avvisa eller ställa in programpunkten?</p>
            <p>
              Markera programpunkten som <strong>inställd</strong> för att
              behålla den i evenemangets program, synligt markerad som inställd.
              Denna åtgärd kan ångras.
            </p>
            <p>
              Du kan också <strong>ställa in och dölja</strong> programpunkten
              för att behålla ett internt register men dölja den från det
              offentliga programmet. Denna åtgärd kan ångras.
            </p>
            <p>
              Om du av någon anledning behöver <strong>radera</strong>{" "}
              programpunkten helt kan du göra det här. Överväg att ställa in den
              istället. Denna åtgärd kan inte ångras.
            </p>
            <p>
              Om den här programpunkten skapades från ett programerbjudande får
              du bestämma erbjudandets öde i nästa steg.
            </p>
          </>
        ),
        modalActions: {
          submit: "Fortsätt",
          cancel: "Stäng utan att avvisa eller ställa in",
        },
        attributes: {
          resolution: {
            title: "Åtgärd",
            choices: {
              CANCEL: "Markera programpunkten som inställd",
              CANCEL_AND_HIDE:
                "Markera programpunkten som inställd och dölj från allmänheten (synlighetsfunktionen är inte implementerad ännu)",
              DELETE: "Radera programpunkten helt",
            },
          },
        },
      },
      delete: {
        title: "Radera inställd programpunkt",
        label: "Radera",
        message: (
          <>
            <p>
              Är du säker på att du vill radera denna inställda programpunkt?
              Åtgärden kan inte ångras.
            </p>
            <p>
              Om programpunkten skapades från ett programerbjudande får du
              bestämma erbjudandets öde i nästa steg.
            </p>
          </>
        ),
        modalActions: {
          submit: "Radera",
          cancel: "Stäng utan att radera",
        },
      },
      restore: {
        title: "Återställ inställd programpunkt",
        label: "Återställ",
        message: (
          <>
            <p>
              Är du säker på att du vill återställa denna inställda programpunkt
              till aktivt tillstånd?
            </p>
          </>
        ),
        modalActions: {
          submit: "Återställ",
          cancel: "Stäng utan att återställa",
        },
      },
      exportAsExcel: {
        title: "Ladda ner som Excel",
        scheduleItems: "Schemapunkter",
        programItems: "Programpunkter",
      },
    },
    messages: {
      failedToCreateProgram: "Det gick inte att skapa programpunkten.",
      programRestored: "Programpunkten återställd.",
      programCancelled: "Programpunkten markerad som inställd.",
      programCancelledAndHidden:
        "Programpunkten markerad som inställd och dold.",
      programDeleted: "Programpunkten raderad.",
      offerCancelled: "Programerbjudandet inställt.",
      offerRejected: "Programerbjudandet avvisat.",
      offerDeleted: "Programerbjudandet raderat.",
      spawnCancelled: (
        <p>
          En programpunkt skapad från detta programerbjudande ställdes in. Nu är
          erbjudandets öde i dina händer. Du kan lämna det som det är, markera
          det som inställt eller avvisat, eller ta bort det helt. Välj klokt.
        </p>
      ),
      spawnDeleted: (
        <p>
          En programpunkt skapad från detta programerbjudande raderades. Nu är
          erbjudandets öde i dina händer. Du kan lämna det som det är, markera
          det som inställt eller avvisat, eller ta bort det helt. Välj klokt.
        </p>
      ),
      hostDeleted: "Programvärden togs bort från programpunkten.",
      hostUpdated: "Programvärden uppdaterad.",
      invitationSent: "Inbjudan till programvärd skickad.",
      invitationResent: "Inbjudan till programvärd skickad igen.",
      invitationRevoked: "Inbjudan till programvärd återkallad.",
      scheduleItemCreated: "Schemapunkt skapad.",
      scheduleItemUpdated: "Schemapunkt uppdaterad.",
      scheduleItemRemoved: "Schemapunkt borttagen.",
    },
    favorites: {
      markAsFavorite: "Markera som favorit",
      unmarkAsFavorite: "Avmarkera som favorit",
      signInToAddFavorites:
        "Genom att logga in kan du markera programpunkter som favoriter, filtrera vyn för att visa bara favoriter och lägga till favoritprogrampunkter i din kalender.",
    },
    scheduleNotPublic:
      "Programschemat för detta evenemang har inte publicerats ännu.",
    filters: {
      showOnlyFavorites: "Visa endast favoriter",
      hidePastPrograms: "Dölj förflutna programpunkter",
    },
    tabs: {
      cards: "Kort",
      table: "Tabell",
    },
    feedback: {
      viewTitle: "Ge feedback",
      notAcceptingFeedback: "Den här programpunkten tar inte emot feedback.",
      fields: {
        feedback: {
          title: "Feedback",
          helpText:
            "Hur tyckte du om programpunkten? Var konstruktiv och empatisk mot programvärdarna :) Din feedback delas med programvärdarna.",
        },
        kissa: {
          title: "Vilket djur säger mjau?",
          helpText: "Svara för att bevisa att du inte är en robot. Tips: Katt.",
        },
      },
      actions: {
        returnToProgram: "Tillbaka till programpunkten",
        submit: "Skicka feedback",
      },
      anonymity: {
        title: "Koppla ditt svar till dig",
        description:
          "Om du ger feedback medan du är inloggad kopplas ditt användarkonto till din feedback. Ditt användarkonto delas dock inte med programvärdarna.",
      },
      thankYou: {
        title: "Tack för din feedback!",
        description: "Din feedback har registrerats.",
      },
    },

    adminDetailTabs: {
      basicInfo: "Grundinformation",
      scheduleItems: "Schema",
      programHosts: "Programvärdar",
      dimensions: "Dimensioner",
      annotations: "Anteckningar",
      preview: "Förhandsvisning",
    },

    profile: {
      title: "Programpunkter och programerbjudanden",
      programItems: {
        listTitle: "Programpunkter du är värd för",
        description: (
          <>
            Här ser du programpunkter där du är listad som programvärd och som
            har accepterats till evenemangets program.
          </>
        ),
        tableFooter: (numPrograms: number) =>
          numPrograms === 1 ? (
            <>En programpunkt.</>
          ) : (
            <>{numPrograms} programpunkter.</>
          ),
      },
      programOffers: {
        listTitle: "Öppna programerbjudanden",
        description: (
          <>
            Dessa programerbjudanden du har skickat har ännu inte accepterats
            eller avvisats.
          </>
        ),
        tableFooter: (count: number) =>
          count === 1 ? (
            <>Ett programerbjudande.</>
          ) : (
            <>{count} programerbjudanden.</>
          ),
      },
      empty: (
        <>
          Du har inga programpunkter eller öppna programerbjudanden. Om du
          anmäler dig som programvärd vid ett evenemang som använder Kompassi
          för att hantera sitt program hittar du dina erbjudanden och
          programpunkter här.
        </>
      ),
      allProgramOffers: (
        <>
          Alla programerbjudanden du har skickat, inklusive de som redan
          behandlats, hittar du här:
        </>
      ),
    },

    ProgramForm: {
      singleTitle: "Programformulär",
      listTitle: "Formulär",
      tableFooter: (numForms: number) => `${numForms} formulär.`,
      programFormForEvent: (eventName: string) => (
        <>Programformulär för {eventName}</>
      ),
      attributes: {
        slug: {
          title: "Tekniskt namn",
          helpText: (
            <>
              Maskinläsbart namn på programformuläret. Måste vara unikt inom
              evenemanget. Kan inte ändras efter att det skapats. Kan innehålla
              gemener, siffror och bindestreck (-). Ingår i URL:en:{" "}
              <code>/evenemang-slug/formulär-slug</code> (t.ex.{" "}
              <code>/tracon2025/offer-program</code>).
            </>
          ),
        },
        purpose: {
          title: "Syfte",
          shortTitle: "Syfte",
          helpText: (
            <>
              Programformulär kan användas för olika syften, t.ex. för att samla
              in programerbjudanden eller ta emot inbjudningar till
              programvärdar. Kan inte ändras efter att det skapats.
            </>
          ),
          choices: {
            DEFAULT: {
              title: "Programerbjudande",
              shortTitle: "Erbjudande",
            },
            INVITE: {
              title: "Inbjudan till programvärd",
              shortTitle: "Inbjudan",
            },
          },
        },
        programDimensionDefaults: {
          title: "Standarddimensioner för programpunkter",
          description: (
            <>
              Dessa dimensionsvärden anges som standard för programerbjudanden
              och programpunkter skapade från dem.
            </>
          ),
        },
        involvementDimensionDefaults: {
          title: "Standarddimensioner för programvärdar",
          description: (
            <>
              Dessa dimensionsvärden anges som standard för programvärdar vid
              godkännande.
            </>
          ),
        },
      },
      actions: {
        viewOffers: "Visa erbjudanden",
        createOfferForm: {
          title: "Skapa programformulär",
          modalActions: {
            submit: "Skapa",
            cancel: "Avbryt",
          },
        },
        deleteProgramForm: {
          title: "Ta bort programformulär",
          cannotRemove:
            "Ett programformulär som har programerbjudanden kan inte tas bort.",
          confirmation: (surveyTitle: string) => (
            <>
              Är du säker på att du vill ta bort programformuläret{" "}
              <strong>{surveyTitle}</strong>?
            </>
          ),
          modalActions: {
            submit: "Ta bort",
            cancel: "Avbryt",
          },
        },
        returnToProgramFormList: (eventName: string) =>
          `Tillbaka till listan över programformulär för ${eventName}`,
      },
    },

    ProgramOffer: {
      singleTitle: "Programerbjudande",
      listTitle: "Erbjudanden",

      attributes: {
        programs: {
          title: "Programpunkter",
          message: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                Följande programpunkt har skapats från detta programerbjudande:
              </>
            ) : (
              <>Följande programpunkter har skapats från detta erbjudande:</>
            ),
          acceptAgainWarning: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                Följande programpunkt har redan skapats från detta
                programerbjudande. Du kan acceptera erbjudandet igen, varvid
                ytterligare en programpunkt skapas. (Länken öppnas i en ny
                flik.)
              </>
            ) : (
              <>
                Följande programpunkter har redan skapats från detta
                programerbjudande. Du kan acceptera erbjudandet igen, varvid
                ytterligare en programpunkt skapas. (Länkarna öppnas i nya
                flikar.)
              </>
            ),
          dimensionsWillNotBeUpdatedOnProgramItem: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                Om du ändrar dimensionerna på detta programerbjudande
                återspeglas ändringarna inte i programpunkten skapad från
                erbjudandet. Du måste redigera programpunkten separat.
              </>
            ) : (
              <>
                Om du ändrar dimensionerna på detta programerbjudande
                återspeglas ändringarna inte i programpunkterna skapade från
                erbjudandet. Du måste redigera programpunkterna separat.
              </>
            ),
        },
      },

      actions: {
        edit: {
          title: "Redigera programerbjudande",
          label: "Redigera",
          cancel: "Avbryt redigering",
          editingOthers: (
            formattedCreatedAt: ReactNode,
            createdBy: ReactNode,
          ) => (
            <>
              Du redigerar ett programerbjudande som skickades{" "}
              {formattedCreatedAt} av <strong>{createdBy}</strong>. Dina
              ändringar träder i kraft först när du skickar formuläret.
            </>
          ),
          cannotEdit: (
            <>
              <h1>Kan inte redigera programerbjudandet</h1>
              <p>Du kan inte redigera detta programerbjudande just nu.</p>
            </>
          ),
          success: (title: string) => (
            <>
              Programerbjudandet <em>{title}</em> har uppdaterats.
            </>
          ),
        },
        accept: {
          title: "Acceptera programerbjudande",
          label: "Acceptera",
          message: (
            <>
              För att skapa en programpunkt från detta erbjudande, granska
              informationen nedan och välj <em>Acceptera</em>. Du kan ändra
              informationen senare utom det tekniska namnet.
            </>
          ),
          modalActions: {
            submit: "Acceptera",
            cancel: "Stäng utan att acceptera",
          },
        },
        cancel: {
          title: "Ställ in, avvisa eller radera programerbjudande",
          label: "Avvisa eller ställ in",
          message: (
            <>
              <p>Vill du avvisa eller ställa in programerbjudandet?</p>
              <p>
                Markera erbjudandet som <strong>inställt</strong> om
                programvärden kontaktade dig och bad om att ställa in det.
              </p>
              <p>
                Markera erbjudandet som <strong>avvisat</strong> om du valde att
                inte acceptera det i evenemangets program.
              </p>
              <p>
                Om du av någon anledning behöver <strong>radera</strong>{" "}
                erbjudandet helt kan du göra det här. Överväg ovanstående
                alternativ först.
              </p>
            </>
          ),
          modalActions: {
            submit: "Fortsätt",
            cancel: "Stäng utan att avvisa eller ställa in",
          },
          attributes: {
            resolution: {
              title: "Åtgärd",
              choices: {
                CANCEL: "Markera programerbjudandet som inställt",
                REJECT: "Avvisa programerbjudandet",
                DELETE: "Radera programerbjudandet helt",
              },
            },
          },
        },
        deleteVisibleProgramOffers: {
          title: "Radera dessa programerbjudanden",
          confirmation(count: number) {
            return (
              <div>
                <p>
                  Är du säker på att du vill radera alla {count}{" "}
                  programerbjudande{count === 1 ? "" : "n"} som visas just nu?
                  Åtgärden kan inte ångras.
                </p>
                <p>
                  <strong>OBS:</strong> Radering av programerbjudanden raderar
                  inte programpunkter skapade från dessa erbjudanden.
                </p>
              </div>
            );
          },
          modalActions: {
            submit: "Radera programerbjudanden",
            cancel: "Stäng utan att radera",
          },
        },
      },

      OldVersionAlert: {
        title: "Visar en föråldrad version av programerbjudandet",
        message:
          "Det här programerbjudandet har redigerats. Du visar en gammal version.",
        actions: {
          returnToCurrentVersion: "Gå till den aktuella versionen",
        },
      },
    },

    ProgramHost: {
      singleTitle: "Programvärd",
      listTitle: "Programvärdar",
      attributes: {
        count: (numHosts: number) => (
          <>
            Visar {numHosts} programvärd{numHosts === 1 ? "" : "ar"}.
          </>
        ),
        programItems: "Programpunkter",
        dimensions: "Programvärdens dimensioner",
        role: {
          title: "Roll",
          choices: {
            OFFERER: {
              title: "Erbjudare",
              description: "Programpunkten skapades från deras erbjudande.",
            },
            INVITED: {
              title: "Inbjuden",
              description: "De bjöds in som värd till programpunkten.",
            },
          },
        },
      },
      actions: {
        inviteProgramHost: {
          title: "Bjud in programvärd",
          attributes: {
            email: {
              title: "E-postadress",
              helpText:
                "Kontrollera e-postadressen noggrant. Inbjudan skickas till denna adress.",
            },
            survey: {
              title: "Programvärdsformulär",
              helpText:
                "När mottagaren accepterar inbjudan ombeds de fylla i detta formulär.",
            },
            language: {
              title: "Språk",
              helpText: "På vilket språk ska inbjudan skickas?",
            },
            dimensionsHeader: {
              title: "Programvärdens dimensioner",
              helpText:
                "Dessa dimensionsvärden anges som standard för programvärden när inbjudan accepteras.",
            },
          },
          message: (
            <>
              För att bjuda in en programvärd, ange deras e-postadress nedan.
              Ett mail skickas med en länk för att acceptera inbjudan. De
              behöver ett användarkonto för att göra det.
            </>
          ),
          modalActions: {
            submit: "Bjud in",
            cancel: "Avbryt",
          },
        },
        removeProgramHost: {
          title: "Ta bort programvärd",
          label: "Ta bort",
          message: (programHost: string, programItem: string) => (
            <>
              <p>
                Är du säker på att du vill ta bort programvärden{" "}
                <strong>{programHost}</strong> från programpunkten{" "}
                <strong>{programItem}</strong>?
              </p>{" "}
              <p>
                För att ångra åtgärden måste du bjuda in dem igen. De meddelas
                inte om denna åtgärd.
              </p>
            </>
          ),
          modalActions: {
            submit: "Ta bort programvärd",
            cancel: "Stäng utan att ta bort",
          },
        },
        editProgramHost: {
          title: "Redigera programvärd",
          label: "Redigera",
          modalActions: {
            submit: "Spara ändringar",
            cancel: "Stäng utan att spara",
          },
        },
        exportAsExcel: {
          title: "Ladda ner som Excel",
        },
      },
    },

    ScheduleItem: {
      singleTitle: "Schemapunkt",
      listTitle: "Schemapunkter",
      tableFooter: (numScheduleItems: number) =>
        `${numScheduleItems} schemapunkt${numScheduleItems === 1 ? "" : "er"}.`,
      attributes: {
        slug: {
          title: "Tekniskt namn",
          helpText: (
            <>
              Maskinläsbart namn på schemapunkten. Måste vara unikt bland
              evenemangets schemapunkter. Kan inte ändras efter att det skapats.
              Kan innehålla gemener, siffror och bindestreck (-). Om du
              förväntar dig att programpunkten bara har en schemapunkt är bästa
              praxis att använda programpunktens tekniska namn.
            </>
          ),
        },
        subtitle: {
          title: "Undertitel",
          helpText: (
            <>
              Om det finns flera schemapunkter kan undertiteln användas för att
              skilja dem åt. Läggs till programtiteln inom parentes. Exempel:
              För en programpunkt med titeln <em>Freedom Fighters</em> kan du ha{" "}
              <em>Freedom Fighters (Karaktärsskapande)</em>,{" "}
              <em>Freedom Fighters (Omgång 1)</em> osv., där värdet i detta fält
              är det som visas inom parentes.
            </>
          ),
          noSubtitle: "Ingen undertitel",
        },
        time: { title: "Tid" },
        startTime: { title: "Starttid" },
        duration: { title: "Längd" },
        durationMinutes: { title: "Längd i minuter" },
        location: { title: "Plats" },
        room: {
          title: "Rum",
          helpText: (
            DimensionsLink: ({
              children,
            }: {
              children: ReactNode;
            }) => ReactNode,
          ) => (
            <>
              För att ändra valen i detta fält, uppdatera värdena för
              dimensionen <code>room</code> i{" "}
              <DimensionsLink>dimensionsredigeraren</DimensionsLink> (öppnas i
              en ny flik).
            </>
          ),
        },
        freeformLocation: {
          title: "Fritext för plats",
          helpText: (
            <>
              Om Rum-fältet ovan är tomt används detta ensamt som besökarsynlig
              plats. Om Rum är angivet men detta fält är tomt används bara
              Rum-värdet. Om båda är angivna läggs detta fälts värde till
              Rum-värdet inom parentes. Exempel: Om Rum är <em>Stora salen</em>{" "}
              och detta fält är <em>Scen</em> visas <em>Stora salen (Scen)</em>.
            </>
          ),
        },
        isPublic: {
          title: "Offentlig",
          helpText: (
            <>Om avmarkerat visas inte denna schemapunkt för allmänheten.</>
          ),
          notPublic: "Den här schemapunkten är inte offentlig.",
        },
      },
      actions: {
        edit: {
          title: "Redigera schemapunkt",
          label: "Redigera",
          modalActions: {
            submit: "Spara ändringar",
            cancel: "Avbryt",
          },
        },
        add: {
          title: "Lägg till schemapunkt",
          label: "Lägg till",
          modalActions: {
            submit: "Lägg till",
            cancel: "Avbryt",
          },
        },
        remove: {
          title: "Ta bort schemapunkt",
          label: "Ta bort",
          message: (scheduleItemTitle: string) => (
            <>
              <p>
                Är du säker på att du vill ta bort schemapunkten{" "}
                <strong>{scheduleItemTitle}</strong>?
              </p>
              <p>
                Åtgärden kan inte ångras. Du måste skapa en ny schemapunkt om du
                vill lägga till den igen.
              </p>
            </>
          ),
          modalActions: {
            submit: "Ta bort schemapunkt",
            cancel: "Stäng utan att ta bort",
          },
        },
      },
    },

    admin: {
      title: "Programadministration",
    },

    preferencesAdmin: {
      title: "Programinställningar",
      attributes: {
        publicFrom: {
          title: "Schema offentligt från",
          helpText:
            "Programschemat blir offentligt synligt vid denna tidpunkt. Lämna tomt för att hålla schemat privat.",
        },
        isSchedulePublic: {
          title: "Schemat är för närvarande offentligt",
        },
      },
    },
  },

  Dimension: {
    listTitle: "Dimensioner",
  },

  Annotation: {
    singleTitle: "Anteckning",
    listTitle: "Anteckningar",
    eventAnnotationsAdmin: {
      title: "Anteckningar som används i detta evenemang",
      message: (
        <>
          <p>
            <strong>Anteckningar</strong> är <em>nyckel-värde-par</em> som ger
            ytterligare information om programpunkter och schemapunkter. De kan
            användas för olika ändamål: vissa anteckningar visas i
            programguiden, andra ger ytterligare information för Kompassi och
            andra system.
          </p>
          <p>
            Värden på anteckningar kan anges på programpunkter och schemapunkter
            baserat på svar på programformulärsfält, eller anges manuellt av
            administratörer.
          </p>
          <p>
            Här kan du definiera vilka anteckningar som är tillgängliga i detta
            evenemang och vilka programformulärsfält som undersöks för att
            bestämma värden för dem.
          </p>
        </>
      ),
      tableFooter: (numAnnotations: number, numActiveAnnotations: number) => (
        <>
          {numAnnotations} anteckning{numAnnotations === 1 ? "" : "ar"} varav{" "}
          {numActiveAnnotations} aktiva.
        </>
      ),
      actions: {
        saveWithoutRefresh: {
          title: "Spara utan att uppdatera",
          description: (
            <>
              Detta sparar ändringar i anteckningens egenskaper. Befintliga
              värden för denna anteckning lämnas oförändrade. Framtida
              programformulärssvar kommer dock att behandlas enligt de
              formulärsfält som definierats här.
            </>
          ),
        },
        saveAndRefresh: {
          title: "Spara och uppdatera",
          description: (
            <>
              Detta sparar ändringar i anteckningens egenskaper och uppdaterar
              dess värden i alla programpunkter och schemapunkter. Tidigare
              värden skrivs över.
            </>
          ),
          confirmationMessage:
            "Är du säker på att du vill spara och uppdatera denna anteckning? Befintliga värden skrivs över.",
        },
        createAnnotation: {
          title: "Skapa anteckning",
          toBeImplemented: (
            <>
              Hantering av evenemangsspecifika anteckningar implementeras i
              framtida evenemang.
            </>
          ),
        },
      },
    },
    attributes: {
      slug: {
        title: "Tekniskt namn",
        helpText: (
          <>
            Består av ett <em>namnområde</em> och ett <em>basnamn</em>,
            separerade med kolon (:). Båda delarna kan innehålla gemener,
            versaler och siffror med <em>camelCase</em>-namngivning. Namnområdet
            används för att skilja anteckningar från olika källor, t.ex.
            evenemangsarrangören, programvärdar eller systemet. Basnamnet
            används för att skilja olika anteckningar inom samma namnområde.
            Till exempel kan <code>konsti:maxParticipants</code> vara en
            anteckning som anger maximalt antal deltagare för en programpunkt
            när anmälan hanteras via Konsti.
          </>
        ),
      },
      title: { title: "Titel" },
      description: { title: "Beskrivning" },
      isActive: {
        title: "Aktiv",
        checkboxLabel: (annotationSlug: string) => (
          <>
            Använd anteckningen <code>{annotationSlug}</code> i detta evenemang
          </>
        ),
        description: (
          <>
            Om avmarkerat används inte denna anteckning för program i detta
            evenemang. Redan angivna värden försvinner inte men visas inte i
            programguiden och deras värden extraheras inte från
            programformulärsfält.
          </>
        ),
      },
      isInternal: { title: "Intern" },
      isShownInDetail: { title: "Visas i programguiden" },
      formFields: {
        title: "Programformulärsfält",
        description: (
          <>
            Tekniska namn på programformulärsfält vars värden extraheras för
            denna anteckning. Ett per rad, i ordning: det första fältet med ett
            icke-tomt värde av lämplig typ används.
          </>
        ),
      },
      properties: { title: "Egenskaper" },
      actions: { title: "Funktioner" },
    },
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
        helpText: (
          <>
            Maskinläsbart namn på enkäten. Måste vara unikt inom evenemanget.
            Kan inte ändras efter att det skapats. Kan innehålla gemener,
            siffror och bindestreck (-). Ingår i URL:en:{" "}
            <code>/evenemang-slug/formulär-slug</code> (t.ex.{" "}
            <code>/tracon2025/offer-program</code>).
          </>
        ),
      },
      title: "Titel",
      isActive: {
        title: "Tar emot svar",
        untilFurtherNotice: "Öppet tills vidare",
        untilTime: (formattedTime) => `Öppet till ${formattedTime}`,
        openingAt: (formattedTime) => `Öppnar vid ${formattedTime}`,
        closed: "Stängt",
        adminOverride: {
          title: "Den här enkäten är inte aktiv",
          message: (
            <>
              Den här enkäten är för närvarande inte öppen för svar. Du kan se
              den här sidan tack vare dina administratörsbehörigheter. Användare
              utan administratörsbehörighet ser bara ett meddelande om att
              enkäten inte är aktiv.
            </>
          ),
        },
      },
      activeFrom: {
        title: "Öppet från",
        helpText:
          "Om detta är inställt börjar enkäten ta emot svar vid denna tidpunkt.",
      },
      activeUntil: {
        title: "Stänger",
        helpText:
          "Om detta är inställt slutar enkäten ta emot svar vid denna tidpunkt.",
      },
      responsesEditableUntil: {
        title: "Svar redigerbara till",
        helpText: (
          <>
            Om inställt kan användare redigera sina svar fram till denna
            tidpunkt. Därefter låses svaren och kan inte redigeras. Om inte
            inställt kan svar inte redigeras efter att de skickats. (Du kan
            också ange <em>Lås objektet från redigering</em> på ett
            dimensionsvärde för att låsa svar som tilldelas det värdet.)
          </>
        ),
      },
      countResponses: "Svar",
      languages: "Språk",
      actions: "Funktioner",
      anonymity: {
        secondPerson: {
          title: "Koppla ditt svar till dig",
          choices: {
            HARD: "Svaren är anonyma. Du kan inte återvända för att se eller redigera dina svar.",
            SOFT: "Om du svarar på den här enkäten medan du är inloggad kopplas den till ditt användarkonto så att du kan återvända för att se eller redigera dina svar, men din identitet delas inte med enkätägaren.",
            NAME_AND_EMAIL:
              "Om du svarar på den här enkäten medan du är inloggad kopplas den till ditt användarkonto. Ditt namn och din e-postadress delas med enkätägaren. Du kan återvända för att se eller redigera dina svar.",
            FULL_PROFILE:
              "Om du svarar på den här enkäten medan du är inloggad kopplas den till ditt användarkonto. Din fullständiga profilinformation delas med enkätägaren. Du kan återvända för att se eller redigera dina svar.",
          },
        },
        thirdPerson: {
          title: "Koppla svar till användare",
          choices: {
            HARD: "Svaren är anonyma. Användare kan inte återvända för att se eller redigera sina svar.",
            SOFT: "Om användaren svarar på den här enkäten medan hen är inloggad kopplas svaret till deras användarkonto så att de kan återvända för att se eller redigera sina svar, men deras identiteter delas inte med dig.",
            NAME_AND_EMAIL:
              "Om användaren svarar på den här enkäten medan hen är inloggad kopplas svaret till deras användarkonto. Deras namn och e-postadresser delas med dig. De kan återvända för att se eller redigera sina svar.",
            FULL_PROFILE:
              "Om användaren svarar på den här enkäten medan hen är inloggad kopplas svaret till deras användarkonto. Deras fullständiga profilinformation delas med dig. De kan återvända för att se eller redigera sina svar.",
          },
        },
        admin: {
          title: "Koppla svar till användare",
          helpText: "OBS: Detta kan inte ändras efter att enkäten har skapats!",
          choices: {
            HARD: "Hårt anonym",
            SOFT: "Mjukt anonym",
            NAME_AND_EMAIL: "Namn och e-post",
            FULL_PROFILE: "Fullständig profil",
          },
        },
      },
      dimensions: "Dimensioner",
      dimension: "Dimension",
      dimensionDefaults: {
        title: "Standarddimensioner",
        description: (
          <>Dessa dimensionsvärden anges som standard för nya svar.</>
        ),
        technicalDimensionsCannotBeChanged:
          "Värden för tekniska dimensioner kan inte ändras.",
      },
      values: "Värden",
      value: "Värde",
      sequenceNumber: "Sekvensnummer",
      versionHistory: "Versionshistorik",
      currentVersionCreatedAt: "Den aktuella versionen skapades",
      currentVersionCreatedBy: "Den aktuella versionen skapades av",
      originalCreatedAt: "Inlämnad",
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
          "Om markerat kan enkäten bara fyllas i av inloggade användare.",
      },
      protectResponses: {
        title: "Skydda svar",
        helpText: "Om markerat kan svar på denna enkät inte raderas.",
      },
      maxResponsesPerUser: {
        title: "Maximalt antal svar per användare",
        helpText:
          "Det maximala antalet svar en enskild användare kan skicka till denna enkät. Om värdet är 0 finns ingen begränsning. Observera att detta endast gäller inloggade användare. Välj också Inloggning krävs för att begränsningen ska fungera.",
      },
      alsoAvailableInThisLanguage: (
        LanguageLink: ({ children }: { children: ReactNode }) => JSX.Element,
      ) => (
        <>
          Det här formuläret finns också <LanguageLink>på svenska</LanguageLink>
          .
        </>
      ),
      cloneFrom: {
        title: "Klona från",
        helpText: (
          <>
            Om valt skapas det nya formuläret som en kopia av ett befintligt.
            Svar kopieras inte.
          </>
        ),
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
      viewResponse: {
        title: "Visa svaret",
        label: "Visa",
      },
      viewResponses: "Visa svar",
      toggleSubscription: "Meddela mig om nya svar",
      submit: "Skicka",
      deleteVisibleResponses: {
        title: "Radera svar",
        confirmation: (countResponses: number) => (
          <>
            Är du säker på att du vill radera de{" "}
            <strong>{countResponses}</strong> svaren som visas?
          </>
        ),
        noResponsesToDelete: "Inga svar att radera.",
        responsesProtected:
          "Svaren på den här enkäten är skyddade. För att ta bort dem, avaktivera svarsskyddet i enkätinställningarna först.",
        cannotDelete: "De här svaren kan inte raderas.",
        modalActions: {
          submit: "Radera svar",
          cancel: "Avbryt utan att radera",
        },
      },
      deleteResponse: {
        title: "Radera svaret",
        label: "Radera",
        confirmation: "Är du säker på att du vill radera det här svaret?",
        cannotDelete: "Det här svaret kan inte raderas.",
        modalActions: {
          submit: "Radera svaret",
          cancel: "Avbryt utan att radera",
        },
      },
      editResponse: {
        title: "Redigera svar",
        label: "Redigera",
        cancel: "Avbryt redigering",
        editingOwn: (formattedCreatedAt: ReactNode) => (
          <>
            Du redigerar ett svar som du skickade {formattedCreatedAt}. Dina
            ändringar träder i kraft först när du skickar formuläret.
          </>
        ),
        editingOthers: (
          formattedCreatedAt: ReactNode,
          createdBy: ReactNode,
        ) => (
          <>
            Du redigerar ett svar som skickades {formattedCreatedAt} av{" "}
            <strong>{createdBy}</strong>. Dina ändringar träder i kraft först
            när du skickar formuläret.
          </>
        ),
        cannotEdit: (
          <>
            <h1>Kan inte redigera svaret</h1>
            <p>Du kan inte redigera det här svaret just nu.</p>
          </>
        ),
      },
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
          "Ett val kan inte raderas om det redan är kopplat till ett svar.",
        confirmation: (dimensionTitle: string, valueTitle: string) => (
          <>
            Radera värdet <strong>{valueTitle}</strong> från dimensionen{" "}
            <strong>{dimensionTitle}</strong>?
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
      viewProfile: {
        title: "Visa användarprofil",
        modalActions: {
          submit: "Den här modalen har ingen skicka-knapp :)",
          cancel: "Stäng",
        },
      },
    },
    errors: {
      noLanguageVersions: {
        title: "Inga språkversioner",
        message: (
          <>
            Den här enkäten har inga språkversioner. Den kan inte fyllas i
            förrän enkätägaren lägger till minst en språkversion.
          </>
        ),
      },
      surveyNotActive: {
        title: "Enkäten är inte aktiv",
        message: <>Den här enkäten är för närvarande inte öppen för svar.</>,
      },
    },
    messages: {
      responseEdited: "Svaret har uppdaterats.",
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
    specialPurposeSurvey: {
      title: "Enkät för särskilt ändamål",
      defaultMessage: (
        <>
          Den här enkäten är avsedd för ett särskilt ändamål och kan inte fyllas
          i via det offentliga gränssnittet.
        </>
      ),
    },
    warnings: {
      choiceNotFound:
        "Valet hittades inte. Det kan ha tagits bort efter att detta svar skickades.",
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
      editTitle: "Redigera dimension",
      addTitle: "Lägg till dimension",
      actions: {
        submit: "Spara dimension",
        cancel: "Avbryt",
      },
      attributes: {
        slug: {
          title: "Tekniskt namn",
          helpText: (
            <>
              Maskinläsbart, kort namn för dimensionen. Kan inte ändras efter
              att det skapats. Kan innehålla gemener, siffror och bindestreck
              (-). Ingår i URL:ens frågeparametrar: <code>dimension=värde</code>{" "}
              (t.ex. <code>program-type=panel</code>).
            </>
          ),
        },
        localizedTitleHeader: {
          title: "Lokaliserade titlar",
          helpText:
            "Dimensionens titel på olika språk. Titeln behöver inte anges på alla språk: om titeln saknas på det valda språket används standardspråket, och därefter det tekniska namnet.",
        },
        behaviourFlagsHeader: {
          title: "Beteende",
          helpText:
            "Dessa inställningar ändrar hur dimensionen fungerar i olika vyer. I de flesta fall kan du lämna dessa på sina standardvärden.",
        },
        title: {
          fi: "Titel på finska",
          en: "Titel på engelska",
          sv: "Titel på svenska",
        },
        isKeyDimension: {
          title: "Nyckeldimension",
          helpText: "Värden för nyckeldimensioner visas i svarslistan.",
        },
        isMultiValue: {
          title: "Flervärde",
          helpText: "Om markerat kan flera värden väljas för denna dimension.",
        },
        isPublic: {
          title: "Offentlig",
          helpText:
            "Om markerat kan värden för denna dimension visas för icke-administratörer.",
        },
        isListFilter: {
          title: "Listfilter",
          helpText:
            "Om markerat visas denna dimension som ett rullgardinsfilter i listvyer.",
        },
        isShownInDetail: {
          title: "Visas i detaljvyer",
          helpText:
            "Om markerat visas värden för denna dimension i detaljvyer för enskilda objekt.",
        },
        isNegativeSelection: {
          title: "Negativt urval",
          helpText:
            "Om markerat föreslår det för gränssnittet att vid filtrering ska alla värden av denna dimension vara markerade som standard och användaren troligen avmarkerar de de inte vill ha. Ger bara mening med flervärdes-dimensioner.",
        },
        valueOrdering: {
          title: "Värdesortering",
          helpText: "I vilken ordning presenteras värdena?",
          choices: {
            MANUAL: "Manuell (dra för att sortera)",
            TITLE: "Titel (lokaliserad)",
            SLUG: "Tekniskt namn",
          },
        },
      },
    },
    editValueModal: {
      editTitle: "Redigera värde",
      addTitle: "Lägg till värde",
      actions: {
        submit: "Spara värde",
        cancel: "Avbryt",
      },
      attributes: {
        slug: {
          title: "Tekniskt namn",
          helpText: (
            <>
              Maskinläsbart, kort namn för dimensionsvärdet. Kan inte ändras
              efter att det skapats. Kan innehålla gemener, siffror och
              bindestreck (-). Ingår i URL:ens frågeparametrar:{" "}
              <code>dimension=värde</code> (t.ex.{" "}
              <code>program-type=panel</code>).
            </>
          ),
        },
        color: {
          title: "Färg",
          helpText:
            "Värdes färg i svarslistan. Använd klara färger – de ljusas eller mörkläggs efter behov.",
        },
        localizedTitleHeader: {
          title: "Lokaliserade titlar",
          helpText:
            "Värdes titel på olika språk. Titeln behöver inte anges på alla språk: om titeln saknas på det valda språket används standardspråket, och därefter det tekniska namnet.",
        },
        isSubjectLocked: {
          title: "Lås objektet från redigering",
          helpText:
            "Om angivet kan de objekt detta värde tilldelats inte längre redigeras av den som skickade dem.",
        },
        title: {
          fi: "Titel på finska",
          en: "Titel på engelska",
          sv: "Titel på svenska",
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
    ResponseHistory: {
      title: "Gamla versioner",
      message:
        "Det här svaret har redigerats. Detta är den senaste versionen. Du kan visa de gamla versionerna här.",
    },
    OldVersionAlert: {
      title: "Visar en föråldrad version av svaret",
      message: "Det här svaret har redigerats. Du visar en gammal version.",
      actions: {
        returnToCurrentVersion: "Gå till den aktuella versionen",
      },
    },
  },

  Involvement: {
    adminTitle: "Hantering av personuppgifter",
    listTitle: "Katalog",
    forEvent(eventName: string) {
      return <>för {eventName}</>;
    },
    attributes: {
      involvement: {
        title: "Inblandning",
        involvementInThisEvent: "Inblandning i detta evenemang",
      },
      count: (numPeople: number, numInvolvements: number) => (
        <>
          Visar {numPeople} {numPeople === 1 ? "person" : "personer"} med{" "}
          {numInvolvements} inblandning{numInvolvements === 1 ? "" : "ar"}.
        </>
      ),
      title: {
        title: "Titel",
        missing: "Ingen titel",
      },
      type: {
        title: "Typ",
        choices: {
          COMBINED_PERKS: "Kombinerade förmåner",
          PROGRAM_HOST: "Programpunkt",
          PROGRAM_OFFER: "Programerbjudande",
          SURVEY_RESPONSE: "Enkätsvar",
          LEGACY_SIGNUP: "Volontär (V1)",
        },
      },
      isActive: {
        title: "Tillstånd",
        choices: {
          active: "Aktiv",
          inactive: "Inaktiv",
        },
      },
      combinedPerks: {
        title: "Kombinerade förmåner",
        message: (
          <>
            En person kan få förmåner från flera källor. Här ser du förmånerna
            sammanslagna automatiskt. En administratör kan ha åsidosatt en del
            eller alla av dem.
          </>
        ),
      },
    },
    messages: {},
    filters: {
      searchPlaceholder: "Sök på namn eller e-post",
    },
    noFiltersApplied: (
      ForceLink: ({ children }: { children: ReactNode }) => ReactNode,
    ) => (
      <>
        Ofiltrerad lista dold. Avgränsa sökningen eller{" "}
        <ForceLink>använd Kraften</ForceLink>.
      </>
    ),
  },

  Invitation: {
    listTitle: "Öppna inbjudningar",
    listDescription: (
      <>
        Dessa personer har bjudits in som programvärdar till den här
        programpunkten men har ännu inte accepterat inbjudan.
      </>
    ),
    attributes: {
      createdAt: "Skapad",
      email: "E-postadress",
      count: (numInvitations: number) =>
        numInvitations === 1 ? (
          <>En öppen inbjudan.</>
        ) : (
          <>{numInvitations} öppna inbjudningar.</>
        ),
      program: {
        title: "Programpunkt",
        editLater: "Du kan redigera programpunkten senare.",
      },
    },
    errors: {
      alreadyUsed: {
        title: "Inbjudan redan använd",
        message:
          "Den här inbjudan har redan använts. Den kan bara användas en gång.",
      },
    },
    actions: {
      revoke: {
        title: "Återkalla inbjudan",
        label: "Återkalla",
        message: (email: string) => (
          <>
            Är du säker på att du vill återkalla inbjudan skickad till{" "}
            <strong>{email}</strong>? De meddelas inte om denna åtgärd. För att
            ångra åtgärden måste du bjuda in användaren igen.
          </>
        ),
        modalActions: {
          submit: "Återkalla inbjudan",
          cancel: "Stäng utan att återkalla",
        },
      },
      resend: {
        title: "Skicka om inbjudan",
        label: "Skicka om",
        message: (email: string) => (
          <>
            Vill du skicka om inbjudan till <strong>{email}</strong>? De får ett
            nytt mail med samma innehåll som den ursprungliga inbjudan.
          </>
        ),
        modalActions: {
          submit: "Skicka om inbjudan",
          cancel: "Stäng utan att skicka om",
        },
      },
    },
  },

  Registry: {
    singleTitle: "Register",
    listTitle: "Register",
  },

  Report: {
    singleTitle: "Rapport",
    listTitle: "Rapporter",
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
