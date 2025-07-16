import { ReactNode, JSX } from "react";
import type { Translations } from "./en";

/// Mark untranslated English strings with this
/// Eg.
/// { foo: UNTRANSLATED("bar") }
function UNTRANSLATED<T>(wat: T): T {
  return wat;
}

const translations: Translations = {
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
      close: "Sulje",
    },
    boolean: {
      true: "Kyllä",
      false: "Ei",
    },
  },
  Profile: {
    attributes: {
      displayName: "Nimi",
      firstName: "Etunimi",
      lastName: "Sukunimi",
      nick: "Nick",
      phoneNumber: "Puhelinnumero",
      email: "Sähköpostiosoite",
      discordHandle: "Discord-tunnus",
    },
    advancedAttributes: {
      displayName: {
        title: "Nimi",
      },
      firstName: {
        title: "Etunimi",
      },
      lastName: {
        title: "Sukunimi",
      },
      nick: {
        title: "Nick",
      },
      phoneNumber: {
        title: "Puhelinnumero",
      },
      email: {
        title: "Sähköpostiosoite",
      },
      discordHandle: {
        title: "Discord-tunnus",
      },
    },
    keysView: {
      title: "Salausavaimet",
      description:
        "Kompassissa säilytettävät luottamukselliset tiedot salataan tietyissä tapauksissa epäsymmetrisellä salauksella. " +
        "Jos sinun tarvitsee toimia vastaanottajana tällaisille tiedoille, tarvitset salausavainparin. " +
        "Voit luoda sellaisen alla. " +
        "Avainparin luonti edellyttää salasanaasi, koska yksityinen avain salataan sillä. " +
        "Tulevaisuudessa mahdollistamme tehokäyttäjille omilla laitteilla säilytettävien salausavainten käytön, " +
        "jotta yksityinen avain ei koskaan poistu laitteelta.",
      resetPasswordWarning: (
        <>
          <strong>Varoitus!</strong> Jos unohdat salasanasi ja resetoit sen,
          menetät salausavaimesi ja kaikki sillä salatut tiedot.
        </>
      ),
      attributes: {
        id: {
          title: "Tunniste",
        },
        createdAt: {
          title: "Luotu",
        },
        actions: {
          title: "Toiminnot",
        },
        password: {
          title: "Salasana",
          helpText: "Syötä salasanasi yksityisen avaimen salaamista varten.",
        },
      },
      actions: {
        generate: {
          title: "Luo avainpari",
          enterPassword:
            "Syötä salasanasi yksityisen avaimen salaamista varten.",
          modalActions: {
            submit: "Luo avainpari",
            cancel: "Peruuta",
          },
        },
        revoke: {
          title: "Mitätöi avainpari",
          confirmation: (formattedCreatedAt: string) => (
            <>
              Haluatko varmasti mitätöidä avainparin, joka luotiin{" "}
              <strong>{formattedCreatedAt}</strong>? Mitätöidyllä avainparilla
              salattua tietoa ei voi enää purkaa. Tätä toimintoa ei voi perua.
            </>
          ),
          modalActions: {
            submit: "Mitätöi",
            cancel: "Peruuta",
          },
        },
      },
    },
  },
  TransferConsentForm: {
    title: "Henkilötietojen luovutus",
    message: (
      <>
        Kun täytät tämän lomakkeen, henkilötietojasi siirretään rekisteristä
        toiseen seuraavasti. Lisäksi vastaanottajan rekisteriin liitetään ne
        henkilötiedot, jotka annat tällä lomakkeella.
      </>
    ),
    messageAlreadyAccepted: (
      <>
        Kun täytit tämän lomakkeen, henkilötietojasi siirrettiin rekisteristä
        toiseen seuraavasti. Lisäksi vastaanottajan rekisteriin liitettiin ne
        henkilötiedot, jotka annoit tällä lomakkeella.
      </>
    ),
    consentCheckBox:
      "Hyväksyn henkilötietojeni luovutuksen ja käsittelyn yllä kuvatulla tavalla.",
    consentAlreadyGivenAt: (formattedDate: ReactNode) => (
      <>
        Olet hyväksynyt henkilötietojesi luovutuksen ja käsittelyn yllä
        kuvatulla tavalla {formattedDate}.
      </>
    ),
    privacyPolicy: "Tietosuojaseloste",
    privacyPolicyMissing: "Tietosuojaseloste puuttuu",
    actions: {
      editProfile: {
        message:
          "Jos huomaat virheitä tai puutteita henkilötiedoissasi, korjaathan ne profiilissasi.",
        link: "Muokkaa profiilia",
      },
    },
    sourceRegistry: "Henkilötietojen lähde",
    targetRegistry: "Henkilötietojen vastaanottaja",
    dataToBeTransferred: "Luovutettavat henkilötiedot",
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
    tickets: "Lipputilaukset",
    responses: "Kyselyvastaukset",
    keys: "Salausavaimet",
    program: "Ohjelmanumerot ja -tarjoukset",
    signIn: "Kirjaudu sisään",
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

    attributes: {
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

    editFieldForm: {
      slug: {
        title: "Tekninen nimi",
        helpText:
          "Kentän tekninen nimi. Ei näytetä loppukäyttäjälle. Sallitut merkit: pienet kirjaimet a-z (ei ääkköset åäö), numerot 0-9 ja alaviiva _. Ei saa alkaa numerolla. Kentän teknisen nimen tulee olla sama eri kieliversioissa.",
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
        helpText:
          'Kullakin rivillä tulisi olla yksi vaihtoehto muodossa "tekninen-nimi: Käyttäjälle näytettävä vaihtoehto".',
      },
      questions: {
        title: "Kysymykset",
        helpText:
          'Kullakin rivillä tulisi olla yksi kysymys muodossa "tekninen-nimi: Käyttäjälle näytettävä kysymys".',
      },
      dimension: {
        title: "Dimensio",
        helpText: "Mistä dimensiosta tämä kenttä saa vastauksensa?",
      },
      encryptTo: {
        title: "Salaa vastaukset",
        helpText:
          "Jos haluat salata vastaukset tähän kenttään, luettele tässä kentässä käyttäjänimet jotka saavat purkaa salauksen (yksi per rivi). Näillä käyttäjillä tulee olla avainpari luotuna.",
      },
    },

    fieldTypes: {
      SingleLineText: "Yksirivinen tekstikenttä",
      MultiLineText: "Monirivinen tekstikenttä",
      Divider: "Erotinviiva",
      StaticText: "Kiinteä teksti",
      Spacer: "Tyhjä tila",
      SingleCheckbox: "Yksittäinen rasti ruutuun -kenttä",
      DimensionSingleCheckbox: "Yksittäinen rasti ruutuun -kenttä (dimensio)",
      SingleSelect: "Valinta",
      DimensionSingleSelect: "Valinta (dimensio)",
      MultiSelect: "Monivalinta",
      DimensionMultiSelect: "Monivalinta (dimensio)",
      RadioMatrix: "Valintamatriisi",
      FileUpload: "Tiedoston lähetys",
      NumberField: "Numero",
      DecimalField: "Desimaaliluku",
      DateField: "Päivämäärä",
      DateTimeField: "Päivämäärä ja kellonaika",
      TimeField: "Kellonaika",
      MultiItemField: "Kasa alilomakejuttuja",
    },
    advancedFieldTypes: {
      SingleSelect: {
        promoteFieldToDimension: {
          title: "Muuta dimensiokentäksi",
          modalActions: {
            submit: "Toteuta muutos",
            cancel: "Sulje tekemättä muutosta",
          },
          existingDimension: (
            <>
              <p>Haluatko varmasti muuttaa tämän kentän dimensiokentäksi?</p>
              <p>
                Jos jatkat, seuraavat toimenpiteet toteutetaan tämän kyselyn{" "}
                <strong>kaikissa kieliversioissa</strong>:
              </p>
              <ol>
                <li>
                  Mahdolliset puuttuvat vaihtoehdot lisätään olemassa olevaan
                  dimensioon, jonka tekninen nimi on sama kuin tällä kentällä.
                  Niiden käännökset otetaan kaikista olemassa olevista
                  kieliversioista.
                </li>
                <li>
                  Tämä kenttä korvataan kentällä, joka saa vaihtoehtonsa edellä
                  mainitusta dimensioista. Kentän muut ominaisuudet pysyvät
                  ennallaan.
                </li>
                <li>
                  Kukin kyselyvastaus, jossa tähän kenttään on vastattu, saa
                  tämän kentän vastaukset kyseisen dimension arvoiksi.
                </li>
              </ol>
              <p>Tätä toimintoa ei voi perua.</p>
            </>
          ),
          newDimension: (
            <>
              <p>Haluatko varmasti muuttaa tämän kentän dimensiokentäksi?</p>
              <p>
                Jos jatkat, seuraavat toimenpiteet toteutetaan tämän kyselyn{" "}
                <strong>kaikissa kieliversioissa</strong>:
              </p>
              <ol>
                <li>
                  Kyselyyn luodaan uusi dimensio, jonka tekninen nimi on sama
                  kuin tällä kentällä. Vaihtoehdot käännöksineen otetaan
                  kaikista olemassa olevista kieliversioista ja yhdistetään
                  niiden teknisten nimien perusteella.
                </li>
                <li>
                  Tämä kenttä korvataan kentällä, joka saa vaihtoehtonsa edellä
                  mainitusta dimensioista. Kentän muut ominaisuudet pysyvät
                  ennallaan.
                </li>
                <li>
                  Kukin kyselyvastaus, jossa tähän kenttään on vastattu, saa
                  tämän kentän vastaukset kyseisen dimension arvoiksi.
                </li>
              </ol>
              <p>Tätä toimintoa ei voi perua.</p>
            </>
          ),
        },
      },
      DimensionSingleSelect: {
        description: (
          <>
            Tämä kenttätyyppi näyttää valintakentän, jonka vaihtoehtoina ovat
            dimension arvot. Kun vastaaja valitsee arvon tähän kenttään,
            vastaukselle asetetaan kyseinen dimension arvo.
          </>
        ),
      },
      DimensionMultiSelect: {
        description: (
          <>
            Tämä kenttätyyppi näyttää monivalintakentän, jonka vaihtoehtoina
            ovat dimension arvot. Kun vastaaja valitsee arvoja tähän kenttään,
            vastaukselle asetetaan kyseiset dimension arvot.
          </>
        ),
      },
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

  Tickets: {
    title: "Osta lippuja",
    forEvent: (eventName: string) => <>tapahtumaan {eventName}</>,
    returnToTicketsPage: "Palaa lippusivulle",
    Product: {
      listTitle: "Tuotteet",
      forEvent: (eventName: string) => <>tapahtumaan {eventName}</>,
      noProducts: {
        title: "Ei tuotteita saatavilla",
        message: "Yhtään tuotetta ei ole tällä hetkellä saatavilla.",
      },
      actions: {
        editProduct: "Muokkaa tuotetta",
        newProduct: {
          title: "Uusi tuote",
          modalActions: {
            submit: "Luo tuote",
            cancel: "Peruuta",
          },
        },
        saveProduct: "Tallenna tuote",
        unpublishAllProducts: "Piilota kaikki tuotteet",
        viewOldVersion: {
          title: "Tuotteen vanha versio",
          label: "Näytä vanha versio tuotteesta",
          modalActions: {
            submit: "",
            cancel: "Sulje",
          },
        },
        deleteProduct: {
          title: "Poista tuote",
          confirmation: (productName: string) => (
            <>
              Haluatko varmasti poistaa tuotteen <strong>{productName}</strong>?
              Poistamista ei voi perua.
            </>
          ),
          modalActions: {
            submit: "Poista",
            cancel: "Peruuta",
          },
          cannotDelete:
            "Tätä tuotetta ei voi poistaa, koska siihen on tehty tilauksia.",
        },
      },
      clientAttributes: {
        product: "Tuote",
        title: "Otsikko",
        createdAt: "Luotu",
        unitPrice: {
          title: "Kappalehinta",
          helpText: "Kappalehinta euroissa.",
        },
        quantity: {
          title: "Lukumäärä",
          quantityForProduct: "Lukumäärä tuotteelle",
          unit: "kpl",
          placeholder: "Lukumäärä",
        },
        total: "Yhteensä",
        description: {
          title: "Description",
          helpText:
            "Title and description will be shown to the customer on the ticket purchase page.",
        },
        maxPerOrder: {
          title: "Maksimimäärä tilausta kohden",
          helpText:
            "Maksimimäärä tätä tuotetta jonka asiakas voi yhdellä tilauksella ostaa..",
        },
        eticketsPerProduct: {
          title: "Sähköisten lippujen määrä kappaletta kohden",
          helpText:
            "Jokaista myytyä kappaletta kohden luodaan näin monta sähköistä lippua. Jos tämä on asetettu nollaan, tuotteelle ei luoda sähköisiä lippuja.",
        },
        availableFrom: {
          title: "Tulee myyntiin",
          helpText:
            "Tuote tulee myyntiin kun tämä aika on ohitettu. Jos tätä ei ole asetettu, tuote ei näy kaupassa.",
        },
        availableUntil: {
          title: "Poistuu myynnistä",
          helpText:
            "Jos tämä on asetettu, tuote poistuu myynnistä kun tämä aika on ohitettu.",
        },
        countPaid: "Maksettu",
        countReserved: {
          title: "Myyty",
          description:
            "Tässä näytetään maksettujen tilausten lisäksi vahvistetut tilaukset, joita ei ole vielä maksettu.",
        },
        countAvailable: "Jäljellä",
        countTotal: "Yhteensä",
        actions: "Toiminnot",
        totalReserved: "Myyty yhteensä",
        totalPaid: "Maksettu yhteensä",
        revisions: {
          title: "Tuotteen versiot",
          description:
            "Jos tuotetta muokataan sen jälkeen kun sitä on myyty, siitä luodaan automaattisesti uusi versio joka korvaa vanhan lippukaupassa. Tuotteen saatavuusaikataulun tai kiintiöiden muuttaminen ei luo uutta versiota.",
          current: "Tämänhetkinen",
        },
        quotas: {
          title: "Kiintiöt",
          helpText:
            "Kiintiöt määrittelevät montako kappaletta tuotetta voidaan myydä. Tuote voi käyttää useampaa kiintiötä; tällöin tuotteen saatavuuden määrittelee kiintiö jota on vähiten jäljellä. Voit muokata ja luoda uusia kiintiöitä Kiintiöt-välilehdellä.",
        },
        selectedQuotas: "Valitut kiintiöt",
        soldOut: "Loppuunmyyty",
        isAvailable: "Saatavuusaika",
        dragToReorder: "Vedä ja pudota järjestääksesi tuotteita",
        newProductQuota: {
          title: "Kiintiö",
          helpText:
            "Voit luoda tuotteelle samannimisen kiintiön asettamalla kiintiön suuruuden tässä. Jos mieluummin jätät kiintiön luomatta ja asetat tuotteen kiintiöt myöhemmin, voit jättää tämän kentän tyhjäksi. Huomaathan, että tuote täytyy liittää vähintään yhteen kiintiöön jotta se näkyy kaupassa.",
        },
      },
      serverAttributes: {
        isAvailable: {
          untilFurtherNotice: "Saatavilla toistaiseksi",
          untilTime: (formattedTime: String) =>
            `Saatavilla ${formattedTime} asti`,
          openingAt: (formattedTime: String) =>
            `Tulossa saataville ${formattedTime}`,
          notAvailable: "Ei saatavilla",
        },
      },
    },
    Quota: {
      listTitle: "Kiintiöt",
      singleTitle: "Kiintiöt",
      forEvent: (eventName: string) => <>tapahtumaan {eventName}</>,
      actions: {
        newQuota: {
          title: "Uusi kiintiö",
          modalActions: {
            submit: "Luo kiintiö",
            cancel: "Peruuta",
          },
        },
        editQuota: "Muokkaa kiintiötä",
        saveQuota: "Tallenna kiintiö",
        deleteQuota: {
          title: "Poista kiintiö",
          confirmation: (quotaName: string) => (
            <>
              Haluatko varmasti poistaa kiintiön <strong>{quotaName}</strong>?
              Poistamista ei voi perua.
            </>
          ),
          modalActions: {
            submit: "Poista",
            cancel: "Peruuta",
          },
          cannotDelete:
            "Tätä kiintiötä ei voi poistaa, koska siihen on liitetty tuotteita. Jotta kiintiö voidaan poistaa, tulee kaikki siihen liitetyt tuotteet ensin irrottaa kiintiöstä.",
        },
      },
      attributes: {
        name: "Nimi",
        countTotal: {
          title: "Kiintiön suuruus",
          helpTextNew:
            "Montako kappaletta tätä kiintiötä käyttäviä tuotteita voidaan yhteensä enintään myydä.",
          helpText: (countReserved: number) =>
            `Montako kappaletta tätä kiintiötä käyttäviä tuotteita voidaan yhteensä enintään myydä. Tästä kiintiöstä on myyty tällä hetkellä ${countReserved} yksikköä; kiintiötä ei voi asettaa tätä alemmaksi.`,
        },
        totalReserved: "Myyty yhteensä",
        products: {
          title: "Kiintiötä käyttävät tuotteet",
          helpText:
            "Tuote voi käyttää useampaa kiintiötä; tällöin tuotteen saatavuuden määrittelee kiintiö jota on vähiten jäljellä.",
        },
      },
    },
    Order: {
      listTitle: "Tilaukset",
      singleTitle: (orderNumber: string, paymentStatus: string) =>
        `Tilaus ${orderNumber} (${paymentStatus})`,
      forEvent: (eventName: string) => <>tapahtumaan {eventName}</>,
      contactForm: {
        title: "Yhteystiedot",
      },
      profileMessage: (
        ProfileLink: ({ children }: { children: ReactNode }) => JSX.Element,
      ) => (
        <>
          Jos sinulla on käyttäjätunnus samalla sähköpostiosoitteella, jolla
          teit tämän tilauksen, voit tarkastella tilauksiasi ja ladata sähköiset
          liput myös <ProfileLink>profiilistasi</ProfileLink>.
        </>
      ),
      profileMessages: {
        confirmationEmailSent: (
          <>
            Sähköpostiosoitteeseesi on lähetetty vahvistusviesti. Tarkista
            sähköpostisi ja seuraa ohjeita vahvistaaksesi sähköpostiosoitteesi.
          </>
        ),
        cancelled: <>Tilauksesi on peruttu onnistuneesti.</>,
        emailConfirmationFailed: (
          <>Sähköpostin vahvistaminen epäonnistui. Yritä myöhemmin uudelleen.</>
        ),
      },
      attributes: {
        orderNumberAbbr: "Tilausnro.",
        orderNumberFull: "Tilausnumero",
        createdAt: "Tilausaika",
        eventName: "Tapahtuma",
        totalPrice: "Yhteensä",
        actions: "Toiminnot",
        totalOrders: (numOrders: number) => (
          <>
            Yhteensä {numOrders} tilaus{numOrders === 1 ? "" : "ta"}.
          </>
        ),
        firstName: {
          title: "Etunimi",
        },
        lastName: {
          title: "Sukunimi",
        },
        displayName: {
          title: "Asiakkaan nimi",
        },
        email: {
          title: "Sähköposti",
          helpText:
            "Tarkista sähköpostiosoite huolellisesti! Sähköiset liput lähetetään tähän osoitteeseen.",
        },
        phone: {
          title: "Puhelin",
        },
        acceptTermsAndConditions: {
          title: "Palveluehdot hyväksytty",
          checkboxLabel(url: string) {
            return (
              <>
                Hyväksyn{" "}
                <a href={url} target="_blank" rel="noopener noreferrer">
                  palveluehdot
                </a>{" "}
                (pakollinen).
              </>
            );
          },
        },
        provider: {
          title: "Maksunvälittäjä",
          choices: {
            NONE: "Ei mitään (0-summa tai manuaalinen)",
            PAYTRAIL: "Paytrail",
            STRIPE: "Stripe",
          },
        },
        status: {
          title: "Tila",
          choices: {
            NOT_STARTED: {
              title: "Tilauksen tila on tuntematon",
              shortTitle: "Tuntematon",
              message:
                "Tilauksesi tila on tuntematon. Yritä hetken kuluttua uudelleen ja ota tarvittaessa yhteyttä tapahtuman järjestäjään.",
            },
            PENDING: {
              title: "Tilaus odottaa maksua",
              shortTitle: "Odottaa maksua",
              message:
                "Tilauksesi on vahvistettu ja tuotteet on varattu sinulle, mutta emme ole vielä vastaanottaneet maksuasi. Käytä alla olevaa painiketta maksaaksesi tilauksesi mahdollisimman pian. Maksamattomat tilaukset perutaan.",
            },
            FAILED: {
              title: "Maksu epäonnistui",
              shortTitle: "Maksu epäonnistui",
              message:
                "Tilauksen maksu epäonnistui tai keskeytettiin. Ole hyvä ja yritä uudelleen. Maksamattomat tilaukset perutaan.",
            },
            PAID: {
              title: "Tilaus on valmis!",
              shortTitle: "Maksettu",
              message:
                "Tilauksesi on valmis ja olemme saaneet maksusi. Saat pian sähköpostiisi tilausvahvistuksen. Jos tilauksessasi on sähköisiä lippuja, ne toimitetaan tilausvahvistuksen liitteenä.",
            },
            CANCELLED: {
              title: "Tilaus on peruutettu",
              shortTitle: "Peruutettu",
              message:
                "Tilauksesi on peruutettu. Jos tilauksessa oli sähköisiä lippuja, ne on mitätöity. Jos uskot tämän olevan virhe, ota yhteyttä tapahtuman järjestäjään.",
            },
            REFUND_REQUESTED: {
              title: "Tilauksen maksu on palautettu",
              shortTitle: "Palautusta pyydetty",
              message:
                "Tilauksesi on peruutettu ja maksu on palautettu. Jos tilauksessa oli sähköisiä lippuja, ne on mitätöity. Jos uskot tämän olevan virhe, ota yhteyttä tapahtuman järjestäjään.",
            },
            REFUND_FAILED: {
              title: "Tilauksen maksu on palautettu",
              shortTitle: "Palautus epäonnistui",
              message:
                "Tilauksesi on peruutettu ja maksu on palautettu. Jos tilauksessa oli sähköisiä lippuja, ne on mitätöity. Jos uskot tämän olevan virhe, ota yhteyttä tapahtuman järjestäjään.",
            },
            REFUNDED: {
              title: "Tilauksen maksu on palautettu",
              shortTitle: "Palautettu",
              message:
                "Tilauksesi on peruutettu ja maksu on palautettu. Jos tilauksessa oli sähköisiä lippuja, ne on mitätöity. Jos uskot tämän olevan virhe, ota yhteyttä tapahtuman järjestäjään.",
            },
          },
        },
      },
      errors: {
        NOT_ENOUGH_TICKETS: {
          title: "Lippuja ei ole riittävästi",
          message:
            "Yhtä tai useampaa tuotetta ei ole saatavissa sitä määrää jonka yritit tilata.",
        },
        INVALID_ORDER: {
          title: "Virhe tilauksen tiedoissa",
          message:
            "Antamasi tilaustiedot eivät kelpaa. Tarkista tilaus ja yritä uudelleen.",
        },
        NO_PRODUCTS_SELECTED: {
          title: "Et valinnut yhtään tuotetta",
          message: "Valitse vähintään yksi tuote.",
        },
        UNKNOWN_ERROR: {
          title: "Virhe tilauksen käsittelyssä",
          message:
            "Tilauksesi käsittelyssä tapahtui virhe. Ole hyvä ja yritä uudelleen.",
        },
        ORDER_NOT_FOUND: {
          title: "Tilausta ei löydy",
          message:
            "Tilausta ei ole olemassa tai sitä ei ole liitetty käyttäjätiliisi.",
          actions: {
            returnToOrderList: "Takaisin tilauslistaan",
            returnToTicketsPage: "Takaisin lippukauppaan",
          },
        },
      },
      actions: {
        purchase: "Vahvista tilaus ja siirry maksamaan",
        pay: "Maksa tilaus",
        viewTickets: "Näytä e-liput",
        newOrder: "Uusi tilaus",
        search: "Hae tilauksia",
        saveContactInformation: "Tallenna yhteystiedot",
        ownerCancel: {
          title: "Peruuta tilaus",
          label: "Peruuta",
          message: (
            <>
              <p>Oletko varma, että haluat peruuttaa tilauksesi?</p>
              <p>Kaikki varatut liput vapautetaan.</p>
              <p>
                Tilauksen peruminen on lopullista. Jos sinulla on kysyttävää,
                ota yhteyttä asiakastukeen.
              </p>
            </>
          ),
          modalActions: {
            submit: "Peruuta tilaus",
            cancel: "Sulje peruuttamatta",
          },
        },
        resendOrderConfirmation: {
          title: "Lähetä tilausvahvistus uudelleen",
          message: (emailAddress: string) => (
            <>
              <p>
                Haluatko varmasti lähettää tilausvahvistuksen (sis. mahdolliset
                e-liput) uudelleen?
              </p>
              <p>
                Tilausvahvistus lähetetään tähän osoitteeseen:{" "}
                <strong>{emailAddress}</strong>
              </p>
              <p>
                <strong>HUOM:</strong> Jos olet muuttamassa tilauksen
                sähköpostiosoitetta, muistathan tallentaa muutokset ennen kuin
                lähetät tilausvahvistuksen uudelleen.
              </p>
            </>
          ),
          modalActions: {
            submit: "Lähetä",
            cancel: "Sulje lähettämättä",
          },
        },
        cancelAndRefund: {
          title: "Peruuta ja palauta maksu",
          message: (
            <>
              <p>Tämä toiminto tekee seuraavat toimenpiteet:</p>
              <ol>
                <li>merkitsee tilauksen perutuksi,</li>
                <li>mitätöi mahdolliset e-liput,</li>
                <li>tekee maksunvälittäjälle pyynnön palauttaa maksu.</li>
              </ol>
              <p>
                Onnistuneesta maksunpalautuksesta lähetetään ilmoitus
                asiakkaalle.
              </p>
              <p>
                <strong>HUOM:</strong> Maksun palautus voi epäonnistua, jos
                maksunvälittäjän hallussa ei ole riittävästi myyjän varoja.
                Tällöin tulee siirtää varoja maksunvälittäjälle ja yrittää
                palautusta uudelleen, tai hoitaa palautus loppuun muulla tavoin.
              </p>
            </>
          ),
          modalActions: {
            submit: "Peruuta tilaus ja palauta maksu",
            cancel: "Sulje peruuttamatta tilausta",
          },
        },
        refundCancelledOrder: {
          title: "Palauta maksu",
          message: (
            <>
              <p>
                Haluatko varmasti pyytää maksunvälittäjää palauttamaan maksun?
              </p>
              <p>
                Onnistuneesta maksunpalautuksesta lähetetään ilmoitus
                asiakkaalle.
              </p>
              <p>
                <strong>HUOM:</strong> Maksun palautus voi epäonnistua, jos
                maksunvälittäjän hallussa ei ole riittävästi myyjän varoja.
                Tällöin tulee siirtää varoja maksunvälittäjälle ja yrittää
                palautusta uudelleen, tai hoitaa palautus loppuun muulla tavoin.
              </p>
            </>
          ),
          modalActions: {
            submit: "Pyydä palautusta",
            cancel: "Sulje palauttamatta maksua",
          },
        },
        cancelWithoutRefunding: {
          title: "Peruuta palauttamatta maksua",
          message: (
            <>
              <p>Tämä toiminto tekee seuraavat toimenpiteet:</p>
              <ol>
                <li>merkitsee tilauksen perutuksi, ja</li>
                <li>mitätöi mahdolliset e-liput.</li>
              </ol>
              <p>
                <strong>HUOM:</strong> Maksua ei palauteta automaattisesti. Jos
                maksu tulee palauttaa kokonaan tai osittain, se on tehtävä
                maksunvälittäjän hallintapaneelista tai{" "}
                <em>Peruuta ja palauta maksu</em> -toiminnolla.
              </p>
              <p>
                <strong>HUOM:</strong> Peruutuksesta ei lähetetä ilmoitusta
                asiakkaalle. Vastaat itse kaikesta kommunikaatiosta asiakkaan
                kanssa peruutukseen liittyen.
              </p>
            </>
          ),
          modalActions: {
            submit: "Peruuta tilaus",
            cancel: "Sulje peruuttamatta tilausta",
          },
        },
        retryRefund: {
          title: "Yritä palautusta uudelleen",
          message: (
            <>
              <p>
                Haluatko varmasti tehdä maksunvälittäjälle uuden
                maksunpalautuspyynnön?
              </p>
              <p>
                Onnistuneesta maksunpalautuksesta lähetetään ilmoitus
                asiakkaalle.
              </p>
              <p>
                <strong>HUOM:</strong> Maksun palautus voi epäonnistua, jos
                maksunvälittäjän hallussa ei ole riittävästi myyjän varoja.
                Tällöin tulee siirtää varoja maksunvälittäjälle ja yrittää
                palautusta uudelleen, tai hoitaa palautus loppuun muulla tavoin.
              </p>
            </>
          ),
          modalActions: {
            submit: "Yritä uudelleen",
            cancel: "Sulje palauttamatta maksua",
          },
        },
        refundManually: {
          title: "Merkitse manuaalisesti palautetuksi",
          message: (
            <>
              <p>
                Haluatko varmasti merkitä tämän tilauksen manuaalisesti
                palautetuksi?
              </p>
              <p>
                <strong>HUOM:</strong> Tämän jälkeen maksua ei enää yritetä
                palauttaa automaattisesti. Olet vastuussa siitä, että palautus
                tulee asianmukaisesti hoidetuksi.
              </p>
              <p>
                Asiakkaalle lähetetään ilmoitus, että tilaus on peruutettu ja
                maksu palautettu.
              </p>
            </>
          ),
          modalActions: {
            submit: "Merkitse manuaalisesti palautetuksi",
            cancel: "Sulje merkitsemättä palautetuksi",
          },
        },
        markAsPaid: {
          title: "Merkitse maksetuksi",
          message: (
            <>
              <p>Haluatko varmasti merkitä tilauksen maksetuksi?</p>
              <p>
                Asiakkaalle lähetetään kuitti. Jos tilaus sisältää sähköisiä
                lippuja, ne lähetetään kuitin liitteenä.
              </p>
            </>
          ),
          modalActions: {
            submit: "Merkitse maksetuksi",
            cancel: "Sulje merkitsemättä maksetuksi",
          },
        },
      },
    },
    PaymentStamp: {
      listTitle: "Maksutiedot",
      attributes: {
        createdAt: "Aikaleima",
        correlationId: "Tapahtumatunniste",
        type: {
          title: "Tyyppi",
          choices: {
            ZERO_PRICE: "Nollahinta",
            CREATE_PAYMENT_REQUEST: "Maksun luonti – Pyyntö",
            CREATE_PAYMENT_SUCCESS: "Maksun luonti – Onnistui",
            CREATE_PAYMENT_FAILURE: "Maksun luonti – Epäonnistui",
            PAYMENT_REDIRECT: "Uudelleenohjaus maksusta",
            PAYMENT_CALLBACK: "Jälki-ilmoitus maksusta",
            CANCEL_WITHOUT_REFUND: "Peruttu palauttamatta maksua",
            CREATE_REFUND_REQUEST: "Palautuksen luonti – Pyyntö",
            CREATE_REFUND_SUCCESS: "Palautuksen luonti – Onnistui",
            CREATE_REFUND_FAILURE: "Palautuksen luonti – Epäonnistui",
            REFUND_CALLBACK: "Jälki-ilmoitus palautuksesta",
            MANUAL_REFUND: "Manuaalinen palautus",
          },
        },
      },
      actions: {
        view: {
          title: "Näytä maksutiedot",
          message: (
            <p>
              Maksutiedoista löytyy teknisiä tietoja maksuprosessista.
              Maksutiedoista voi olla hyötyä, kun epäonnistuneita maksuja
              selvitellään maksunvälittäjän kanssa.
            </p>
          ),
          modalActions: {
            cancel: "Sulje",
            submit: "Lähetä-nappia ei ole :)",
          },
        },
      },
    },
    Receipt: {
      listTitle: "Kuitit",
      attributes: {
        id: "Tapahtumatunniste",
        createdAt: "Aikaleima",
        type: {
          title: "Tyyppi",
          choices: {
            PAID: "Tilausvahvistus",
            CANCELLED: "Peruutusilmoitus",
            REFUNDED: "Palautusilmoitus",
          },
        },
        status: {
          title: "Tila",
          choices: {
            REQUESTED: "Pyydetty",
            PROCESSING: "Käsitellään",
            FAILURE: "Epäonnistui",
            SUCCESS: "Lähetetty",
          },
        },
      },
    },
    Code: {
      listTitle: "E-lippukoodit",
      attributes: {
        code: "Koodi",
        literateCode: "Kissakoodi",
        usedOn: "Käytetty",
        productText: "Tuote",
        status: {
          title: "Tila",
          choices: {
            UNUSED: "Käyttämätön",
            USED: "Käytetty",
            MANUAL_INTERVENTION_REQUIRED: "Mitätöity",
            BEYOND_LOGIC: "Perätilassa",
          },
        },
      },
    },
    profile: {
      title: "Lipputilaukset",
      message:
        "Näet tässä lipputilauksesi, jotka on tehty vuonna 2025 tai myöhemmin. Voit myös maksaa maksamattomat tilauksesi ja ladata sähköiset lippusi täällä.",
      haveUnlinkedOrders: {
        title: "Vahvista sähköpostiosoitteesi nähdäksesi lisää tilauksia",
        message:
          "Sähköpostiosoitteellasi löytyy lisää tilauksia, joita ei ole liitetty käyttäjätunnukseesi. Vahvista sähköpostiosoitteesi nähdäksesi nämä tilaukset.",
      },
      actions: {
        confirmEmail: {
          title: "Vahvista sähköpostiosoitteesi",
          description:
            "Käyttäjätunnukseesi liitettyyn sähköpostiosoitteeseen lähetetään vahvistusviesti. Seuraa sähköpostissa olevia ohjeita vahvistaaksesi sähköpostiosoitteesi ja nähdäksesi loput tilauksesi.",
          modalActions: {
            submit: "Lähetä vahvistusviesti",
            cancel: "Peruuta",
          },
        },
      },
      noOrders: "Käyttäjätunnukseesi ei ole liitetty yhtään lipputilausta.",
    },
    admin: {
      title: "Lippukaupan hallinta",
      tabs: {
        orders: "Tilaukset",
        products: "Tuotteet",
        quotas: "Kiintiöt",
        reports: "Raportit",
        ticketControl: "Lipuntarkastus",
      },
    },
  },

  NewProgramView: {
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

  Program: {
    listTitle: "Ohjelma",
    singleTitle: "Ohjelmanumero",
    adminListTitle: "Ohjelmanumerot",
    inEvent: (eventName: string) => <>tapahtumassa {eventName}</>,
    tableFooter: (numPrograms: number) =>
      `${numPrograms} ohjelmanumero${numPrograms === 1 ? "" : "a"}.`,
    attributes: {
      slug: {
        title: "Tekninen nimi",
        helpText:
          "Ohjelmanumeron tekninen nimi. Täytyy olla uniikki tapahtuman sisällä. Ei voi muuttaa luomisen jälkeen. Voi sisältää pieniä kirjaimia, numeroita ja väliviivoja (-). Tulee osaksi osoitetta: <code>/EVENT-SLUG/programs/PROGRAM-SLUG</code> (esim. <code>/tracon2025/programs/opening-ceremony</code>).",
      },
      event: "Tapahtuma",
      title: "Otsikko",
      actions: "Toiminnot",
      description: "Kuvaus",
      state: {
        title: "Tila",
        choices: {
          new: "Uusi",
          accepted: "Hyväksytty",
        },
      },
      programOffer: {
        title: "Ohjelmatarjous",
        message:
          "Tämä ohjelmanumero on luotu seuraavan ohjelmatarjouksen perusteella:",
      },
      programHosts: {
        title: "Ohjelmanpitäjät",
      },
      scheduleItems: {
        title: "Aikataulumerkinnät",
      },
      dimensions: "Ohjelmanumeron dimensiot",
      annotations: "Lisätiedot",
    },
    actions: {
      returnToProgramList: (eventName: string) =>
        `Takaisin tapahtuman ${eventName} ohjelmaan`,
      returnToProgramAdminList: (eventName: string) =>
        `Takaisin tapahtuman ${eventName} ohjelmanumeroiden hallintaan`,
      addTheseToCalendar: "Lisää nämä ohjelmanumerot kalenteriin",
      addThisToCalendar: "Lisää tämä ohjelmanumero kalenteriin",
      signUpForThisProgram: "Ilmoittaudu tähän ohjelmanumeroon",
      preview: "Ohjelmaoppaan esikatselu",
      preferences: "Asetukset",
      create: {
        title: "Luo ohjelmanumero",
        modalActions: {
          submit: "Luo ohjelmanumero",
          cancel: "Peruuta",
        },
      },
      cancel: {
        title: "Peru tai poista ohjelmanumero",
        label: "Peru tai poista",
        message: (
          <>
            <p>Haluatko varmasti perua tai poistaa ohjelmanumeron?</p>
            <p>
              Jos merkitset ohjelmanumeron <strong>peruutetuksi</strong>, se
              säilytetään tapahtuman ohjelmalistauksessa mutta merkitään
              näkyvästi peruutetuksi. Voit palauttaa ohjelmanumeron myöhemmin,
              jos tulet toisiin ajatuksiin.
            </p>
            <p>
              Voit myös <strong>perua ja piilottaa</strong> ohjelmanumeron.
              Tällöin ohjelmanumeron tiedot säilytetään sisäisesti, mutta se
              piilotetaan ohjelmalistauksesta. Voit palauttaa ohjelmanumeron
              myöhemmin.
            </p>
            <p>
              Voit myös <strong>poistaa ohjelmanumeron kokonaan</strong>.
              Harkitse kuitenkin, riittäisikö ohjelmanumeron peruminen.
              Poistettua ohjelmanumeroa ei voi palauttaa.
            </p>
            <p>
              Jos tämä ohjelmanumero luotiin ohjelmatarjouksen perusteella, saat
              päättää ohjelmatarjouksen kohtalosta seuraavassa vaiheessa.
            </p>
          </>
        ),
        modalActions: {
          submit: "Toteuta valittu toiminto",
          cancel: "Sulje perumatta",
        },
        attributes: {
          resolution: {
            title: "Ratkaisu",
            choices: {
              CANCEL: "Merkitse ohjelmanumero peruutetuksi",
              CANCEL_AND_HIDE:
                "Peru ja piilota ohjelmanumero (ohjelmien näkyvyyttä ei ole vielä toteutettu)",
              DELETE: "Poista ohjelmanumero kokonaan",
            },
          },
        },
      },
      delete: {
        title: "Poista peruutettu ohjelmanumero",
        label: "Poista",
        message: (
          <>
            <p>
              Haluatko varmasti poistaa tämän peruutetun ohjelmanumeron? Tätä
              toimintoa ei voi perua.
            </p>
            <p>
              Jos tämä ohjelmanumero luotiin ohjelmatarjouksen perusteella, saat
              päättää ohjelmatarjouksen kohtalosta seuraavassa vaiheessa.
            </p>
          </>
        ),
        modalActions: {
          submit: "Poista",
          cancel: "Sulje poistamatta",
        },
      },
      restore: {
        title: "Palauta peruutettu ohjelmanumero",
        label: "Palauta",
        message: (
          <>
            <p>
              Haluatko varmasti palauttaa tämän peruutetun ohjelmanumeron
              aktiiviseksi?
            </p>
          </>
        ),
        modalActions: {
          submit: "Palauta",
          cancel: "Sulje palauttamatta",
        },
      },
    },
    messages: {
      failedToCreate: "Ohjelmanumeron luonti epäonnistui.",
      restored: "Ohjelmanumero palautettu.",
      cancelled: "Ohjelmanumero merkitty peruutetuksi.",
      cancelledAndHidden: "Ohjelmanumero peruttu ja piilotettu.",
      deleted: "Ohjelmanumero poistettu.",
    },
    favorites: {
      markAsFavorite: "Merkitse suosikiksi",
      unmarkAsFavorite: "Poista suosikeista",
      signInToAddFavorites:
        "Kirjautumalla sisään voit merkitä ohjelmanumeroita suosikeiksi, suodattaa näkymää näyttämään vain suosikit ja lisätä suosikkiohjelmanumerot kalenteriisi.",
    },
    filters: {
      showOnlyFavorites: "Näytä vain suosikit",
      hidePastPrograms: "Piilota menneet ohjelmat",
    },
    tabs: {
      cards: "Kortit",
      table: "Taulukko",
    },
    feedback: {
      viewTitle: "Anna palautetta",
      notAcceptingFeedback: "Tämä ohjelmanumero ei ota vastaan palautetta.",
      fields: {
        feedback: {
          title: "Palaute",
          helpText:
            "Mitä pidit ohjelmanumerosta? Olethan rakentava ja empaattinen ohjelmanpitäjää kohtaan :) Palautteesi toimitetaan ohjelmanumeron järjestäjälle.",
        },
        kissa: {
          title: "Mikä eläin sanoo miau?",
          helpText: "Tällä varmistamme, että et ole robotti. Vihje: Kissa.",
        },
      },
      actions: {
        returnToProgram: "Palaa ohjelmanumeron sivulle",
        submit: "Lähetä palaute",
      },
      anonymity: {
        title: "Vastausten yhdistäminen sinuun",
        description:
          "Jos lähetät ohjelmapalautetta kirjautuneena, palautteesi yhdistetään käyttäjätiliisi. Käyttäjäprofiiliasi ei kuitenkaan jaeta ohjelmanumeron järjestäjälle.",
      },
      thankYou: {
        title: "Kiitos palautteestasi!",
        description: "Palautteesi on tallennettu.",
      },
    },

    adminDetailTabs: {
      basicInfo: "Perustiedot",
      scheduleItems: "Aikataulutus",
      programHosts: "Ohjelmanpitäjät",
      dimensions: "Dimensiot",
      annotations: "Lisätiedot",
      preview: "Esikatselu",
    },

    profile: {
      title: "Ohjelmanumerot ja ohjelmatarjoukset",
      programItems: {
        listTitle: "Ohjelmanumerot joissa olet ohjelmanpitäjänä",
        description: (
          <>
            Tässä näet ohjelmanumerot, joihin sinut on listattu
            ohjelmanpitäjäksi ja jotka on hyväksytty tapahtuman ohjelmaan.
          </>
        ),
        tableFooter: (count: number) =>
          count === 1 ? <>Yksi ohjelmanumero.</> : <>{count} ohjelmanumeroa.</>,
      },
      programOffers: {
        listTitle: "Avoimet ohjelmatarjoukset",
        description: (
          <>
            Tässä näet tekemäsi ohjelmatarjoukset, joita ei ole vielä hyväksytty
            tai hylätty.
          </>
        ),
        tableFooter: (count: number) =>
          count === 1 ? (
            <>Yksi ohjelmatarjous.</>
          ) : (
            <>{count} ohjelmatarjousta.</>
          ),
      },
      empty: (
        <>
          Sinulla ei ole ohjelmanumeroita eikä avoimia ohjelmatarjouksia. Jos
          ilmoittaudut ohjelmanpitäjäksi tapahtumaan, joka käyttää Kompassia
          ohjelmansa hallintaan, löydät ohjelmatarjoukset ja ohjelmanumerot
          täältä.
        </>
      ),
      allProgramOffers: (
        <>
          Löydät kaikki tekemäsi ohjelmatarjoukset, mukaan lukien ne jotka on jo
          käsitelty, täältä:
        </>
      ),
    },

    ProgramForm: {
      singleTitle: "Ohjelmalomake",
      listTitle: "Ohjelmalomakkeet",
      programFormForEvent: (eventName: string) => (
        <>Ohjelmalomake tapahtumalle {eventName}</>
      ),
      tableFooter: (numForms: number) =>
        `${numForms} ohjelmalomake${numForms === 1 ? "" : "tta"}.`,
      attributes: {
        slug: {
          title: "Tekninen nimi",
          helpText: (
            <>
              Keksi ohjelmalomakkeelle tekninen nimi, joka tulee osaksi
              lomakkeen osoitetta:{" "}
              <code>/tapahtuman-tekninen-nimi/lomakkeen-tekninen-nimi</code> .
              Esimerkiksi osoitteessa <code>/tracon2025/offer-program</code>{" "}
              lomakkeen tekninen nimi on <code>offer-program</code>. Teknisen
              nimen tulee olla uniikki tapahtuman sisällä, ja sitä ei voi
              muuttaa lomakkeen luomisen jälkeen. Tekninen nimi voi sisältää{" "}
              <strong>pieniä</strong> kirjaimia, numeroita ja väliviivoja (-).
            </>
          ),
        },
        purpose: {
          title: "Käyttötarkoitus",
          shortTitle: "Tarkoitus",
          helpText: (
            <>
              Ohjelmalomakkeita voidaan käyttää eri käyttötarkoituksiin, kuten
              ohjelmatarjousten keräämiseen tai ohjelmanpitäjäkutsujen
              hyväksymiseen. Lomakkeen käyttötarkoitusta ei voi muuttaa
              lomakkeen luomisen jälkeen.
            </>
          ),
          choices: {
            DEFAULT: {
              title: "Ohjelman tarjoaminen",
              shortTitle: "Tarjous",
            },
            INVITE: {
              title: "Ohjelmanpitäjäkutsun hyväksyminen",
              shortTitle: "Kutsu",
            },
          },
        },
        programDimensionDefaults: {
          title: "Ohjelmanumeron dimensioiden oletusarvot",
          description: (
            <>
              Nämä dimensioarvot asetetaan oletusarvoisesti ohjelmatarjouksille
              ja niistä luoduille ohjelmanumeroille.
            </>
          ),
        },
        involvementDimensionDefaults: {
          title: "Ohjelmanpitäjän dimensioiden oletusarvot",
          description: (
            <>
              Nämä dimensioarvot asetetaan oletusarvoisesti ohjelmanpitäjille
              hyväksymisen yhteydessä.
            </>
          ),
        },
      },
      actions: {
        viewOffers: "Tarjoukset",
        createOfferForm: {
          title: "Luo ohjelmalomake",
          modalActions: {
            submit: "Luo",
            cancel: "Peruuta",
          },
        },
        deleteProgramForm: {
          title: "Poista ohjelmalomake",
          cannotRemove:
            "Ohjelmalomaketta ei voi poistaa, koska sillä on tehty ohjelmatarjouksia.",
          confirmation: (surveyTitle: string) => (
            <>
              Haluatko varmasti poistaa ohjelmalomakkeen{" "}
              <strong>{surveyTitle}</strong>?
            </>
          ),
          modalActions: {
            submit: "Poista",
            cancel: "Peruuta",
          },
        },
        returnToProgramFormList: (eventName: string) =>
          `Takaisin tapahtuman ${eventName} ohjelmalomakkeiden listaan`,
      },
    },

    ProgramOffer: {
      singleTitle: "Ohjelmatarjous",
      listTitle: "Ohjelmatarjoukset",

      attributes: {
        programs: {
          title: "Ohjelmanumerot",
          message: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                Seuraava ohjelmanumero on luotu tämän ohjelmatarjouksen
                perusteella:
              </>
            ) : (
              <>
                Seuraavat ohjelmanumerot on luotu tämän ohjelmatarjouksen
                perusteella:
              </>
            ),
          acceptAgainWarning: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                Seuraava ohjelmanumero on jo luotu tämän ohjelmatarjouksen
                perusteella. Voit hyväksyä ohjelmatarjouksen uudelleen, jolloin
                luodaan uusi ohjelmanumero. (Tämä linkki avautuu uuteen
                välilehteen.)
              </>
            ) : (
              <>
                Seuraavat ohjelmanumerot on jo luotu tämän ohjelmatarjouksen
                perusteella. Voit hyväksyä ohjelmatarjouksen uudelleen, jolloin
                luodaan uusi ohjelmanumero. (Nämä linkit avautuvat uuteen
                välilehteen.)
              </>
            ),
          dimensionsWillNotBeUpdatedOnProgramItem: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                Jos muutat tämän ohjelmatarjouksen dimensioita, muutokset eivät
                päivity ohjelmanumeroon. Ohjelmanumero tulee päivittää erikseen.
              </>
            ) : (
              <>
                Jos muutat tämän ohjelmatarjouksen dimensioita, muutokset eivät
                päivity ohjelmanumeroihin. Ohjelmanumerot tulee päivittää
                erikseen.
              </>
            ),
        },
      },

      actions: {
        edit: {
          title: "Muokkaa ohjelmatarjousta",
          label: "Muokkaa",
          cancel: "Peru muokkaus",
          editingOthers: (
            formattedCreatedAt: ReactNode,
            createdBy: ReactNode,
          ) => (
            <>
              Muokkaat ohjelmatarjousta, jonka lähetti {formattedCreatedAt}{" "}
              <strong>{createdBy}</strong>. Muutokset astuvat voimaan vasta, kun
              lähetät lomakkeen.
            </>
          ),
          cannotEdit: (
            <>
              <h1>Ohjelmatarjousta ei voi muokata</h1>
              <p>Et voi muokata tätä ohjelmatarjousta tällä hetkellä.</p>
            </>
          ),
          success: (title: string) => (
            <>
              Ohjelmatarjous <em>{title}</em> on päivitetty.
            </>
          ),
        },
        accept: {
          title: "Hyväksy ohjelmatarjous",
          label: "Hyväksy",
          message: (
            <>
              Voit luoda ohjelmanumeron tästä ohjelmatarjouksesta tarkistamalla
              alla olevat tiedot ja valitsemalla <em>Hyväksy</em>.
              Ohjelmanumeron tietoja voi muokata myöhemmin teknistä nimeä lukuun
              ottamatta.
            </>
          ),
          modalActions: {
            submit: "Hyväksy",
            cancel: "Sulje hyväksymättä",
          },
        },
        cancel: {
          title: "Hylkää tai peru ohjelmatarjous",
          label: "Hylkää tai peru",
          message: (
            <>
              <p>Haluatko hylätä tai perua ohjelmatarjouksen?</p>
              <p>
                Merkitse ohjelmatarjous <strong>peruutetuksi</strong>, jos
                ohjelmanpitäjä pyysi itse ohjelmatarjouksensa peruuttamista.
              </p>
              <p>
                Merkitse ohjelmatarjous <strong>hylätyksi</strong>, jos päätit
                olla ottamatta ohjelmatarjousta vastaan.
              </p>
              <p>
                Voit myös <strong>poistaa</strong> ohjelmatarjouksen kokonaan.
                Harkitse kuitenkin, sopiiko jompi kumpi edellä mainituista
                ratkaisusta tähän tilanteeseen.
              </p>
              <p>
                Jos ohjelmanumero luotiin ohjelmatarjouksesta, saat päättää
                ohjelmatarjouksen kohtalon seuraavassa vaiheessa.
              </p>
            </>
          ),
          modalActions: {
            submit: "Toteuta valittu ratkaisu",
            cancel: "Sulje perumatta ohjelmatarjousta",
          },
          attributes: {
            resolution: {
              title: "Miten haluat käsitellä ohjelmatarjouksen?",
              choices: {
                CANCEL: "Merkitse ohjelmatarjous peruutetuksi",
                REJECT: "Hylkää ohjelmatarjous",
                DELETE: "Poista ohjelmatarjous kokonaan",
              },
            },
          },
        },
      },

      messages: {
        cancelled: "Ohjelmatarjous merkitty peruutetuksi.",
        rejected: "Ohjelmatarjous hylätty.",
        deleted: "Ohjelmatarjous poistettu.",
        spawnCancelled: (
          <p>
            Tästä ohjelmatarjouksesta luotu ohjelmanumero peruttiin. Nyt
            ohjelmatarjouksen kohtalo on käsissäsi. Voit jättää sen sikseen,
            merkitä sen peruutetuksi tai hylätyksi tai poistaa sen kokonaan.
            Valitse viisaasti.
          </p>
        ),
        spawnDeleted: (
          <p>
            Tästä ohjelmatarjouksesta luotu ohjelmanumero poistettiin. Nyt
            ohjelmatarjouksen kohtalo on käsissäsi. Voit jättää sen sikseen,
            merkitä sen peruutetuksi tai hylätyksi tai poistaa sen kokonaan.
            Valitse viisaasti.
          </p>
        ),
      },

      OldVersionAlert: {
        title: "Tämä on vanha versio ohjelmatarjouksesta",
        message: "Ohjelmatarjousta on muokattu. Tämä on vanha versio.",
        actions: {
          returnToCurrentVersion: "Palaa uusimpaan versioon",
        },
      },
    },

    ProgramHost: {
      singleTitle: "Ohjelmanpitäjä",
      listTitle: "Ohjelmanpitäjät",
      attributes: {
        count: (numHosts: number) => (
          <>
            Näytetään {numHosts} ohjelmanpitäjä{numHosts === 1 ? "" : "ä"}.
          </>
        ),
        programItems: "Ohjelmanumerot",
        dimensions: "Ohjelmanpitäjän dimensiot",
        role: {
          title: "Rooli",
          choices: {
            OFFERER: {
              title: "Tarjoaja",
              description: "Ohjelmanpitäjä, joka on luonut ohjelmatarjouksen.",
            },
            INVITED: {
              title: "Kutsuttu",
              description: "Ohjelmanpitäjä, joka on kutsuttu ohjelmanumeroon.",
            },
          },
        },
      },
      actions: {
        inviteProgramHost: {
          title: "Kutsu ohjelmanpitäjä",
          attributes: {
            email: {
              title: "Sähköposti",
              helpText:
                "Tarkista sähköpostiosoite huolellisesti! Kutsu lähetetään tähän osoitteeseen.",
            },
            survey: {
              title: "Ohjelmanpitäjälomake",
              helpText:
                "Kun vastaanottaja hyväksyy kutsun, häntä pyydetään täyttämään tämä lomake.",
            },
            language: {
              title: "Kieli",
              helpText: "Millä kielellä kutsu lähetetään?",
            },
            dimensionsHeader: {
              title: "Ohjelmanpitäjän dimensiot",
              helpText:
                "Nämä dimensioarvot asetetaan ohjelmanpitäjälle kutsun hyväksymisen yhteydessä.",
            },
          },
          message: (
            <>
              Kutsu ohjelmanpitäjä syöttämällä hänen sähköpostiosoitteensa alla
              olevaan kenttään. Hänelle lähetetään kutsulinkin sisältävä
              sähköpostiviesti. Kutsun hyväksyminen edellyttää käyttäjätunnusta.
            </>
          ),
          modalActions: {
            submit: "Lähetä kutsu",
            cancel: "Peruuta",
          },
        },
        removeProgramHost: {
          title: "Poista ohjelmanpitäjä",
          label: "Poista",
          message: (programHost: string, programTitle: string) => (
            <>
              <p>
                Haluatko varmasti poistaa ohjelmanpitäjän{" "}
                <strong>{programHost}</strong> ohjelmanumerosta{" "}
                <strong>{programTitle}</strong>?
              </p>{" "}
              <p>
                Poiston peruminen edellyttää kutsun lähettämistä uudelleen.
                Ohjelmanpitäjälle ei lähetetä ilmoitusta siitä, että hänet on
                poistettu ohjelmanumerosta.
              </p>
            </>
          ),
          modalActions: {
            submit: "Poista ohjelmanpitäjä",
            cancel: "Sulje poistamatta",
          },
        },
        editProgramHost: {
          title: "Muokkaa ohjelmanpitäjää",
          label: "Muokkaa",
          modalActions: {
            submit: "Tallenna muutokset",
            cancel: "Sulje tallentamatta",
          },
        },
      },
      messages: {
        deleted: "Ohjelmanpitäjä poistettu ohjelmanumerosta.",
        invited: "Ohjelmanpitäjäkutsu lähetetty.",
        resent: "Ohjelmanpitäjäkutsu lähetettiin uudelleen.",
        revoked: "Ohjelmanpitäjäkutsu peruttiin.",
        updated: "Ohjelmanpitäjän tiedot päivitetty.",
      },
    },

    ScheduleItem: {
      singleTitle: "Aikataulumerkintä",
      listTitle: "Aikataulumerkinnät",
      tableFooter: (numScheduleItems: number) =>
        `${numScheduleItems} aikataulumerkintä${
          numScheduleItems === 1 ? "" : "ä"
        }.`,
      attributes: {
        slug: {
          title: "Tekninen nimi",
          helpText: UNTRANSLATED(
            <>
              Koneellisesti luettava nimi aikataulumerkinnälle. Täytyy olla
              uniikki tapahtuman aikataulumerkintöjen joukossa. Ei voi muuttaa
              luomisen jälkeen. Voi sisältää pieniä kirjaimia, numeroita ja
              väliviivoja (-). Jos ennakoit, että ohjelmanumerolla on vain yksi
              aikataulumerkintä, on suositeltavaa käyttää ohjelmanumeron
              teknistä nimeä myös aikataulumerkinnän teknisenä nimenä.
            </>,
          ),
        },
        subtitle: {
          title: "Alaotsikko",
          helpText: (
            <>
              Jos ohjelmanumerolla on useita aikataulumerkintöjä, alaotsikkoa
              voidaan käyttää erottamaan ne toisistaan. Alaotsikko liitetään
              ohjelmanumeron otsikkoon sulkeissa. Esimerkki: Jos ohjelmanumeron
              otsikko on <em>Freedom Fighters</em>, voi sillä olla
              aikataulumerkintöjä kuten <em>Freedom Fighters (hahmonluonti)</em>
              , <em>Freedom Fighters (pelautus 1)</em> jne. missä alaotsikko on
              se mitä on sulkeissa.
            </>
          ),
          noSubtitle: "Ei alaotsikkoa",
        },
        time: {
          title: "Ajankohta",
        },
        startTime: {
          title: "Aloitusaika",
        },
        duration: {
          title: "Kesto",
        },
        durationMinutes: {
          title: "Kesto minuutteina",
        },
        location: {
          title: "Sijainti",
        },
        room: {
          title: "Sali",
          helpText: (
            DimensionsLink: ({
              children,
            }: {
              children: ReactNode;
            }) => ReactNode,
          ) => (
            <>
              Muuttaaksesi tämän kentän vaihtoehtoja muokkaa dimensiota{" "}
              <code>room</code>{" "}
              <DimensionsLink>
                ohjelman dimensioiden muokkausnäkymässä
              </DimensionsLink>{" "}
              (aukeaa uuteen välilehteen).
            </>
          ),
        },
        freeformLocation: {
          title: "Vapaamuotoinen sijainti",
          helpText: (
            <>
              Jos yllä oleva Sali-kenttä on tyhjä, tätä kenttää käytetään
              yksinään aikataulumerkinnän kävijälle näkyvänä sijaintina. Jos
              sali on asetettu ja tämä kenttä on tyhjä, käytetään pelkästään
              salin nimeä. Jos molemmat on määritetty, tämän kentän arvo
              liitetään salin nimeen sulkeissa. Esimerkkejä: Jos sali on{" "}
              <em>Pääsali</em> ja tässä kentässä lukee <em>lava</em>, kävijälle
              näkyvä sijainti on <em>Pääsali (lava)</em>.
            </>
          ),
        },
      },
      actions: {
        edit: {
          title: "Muokkaa aikataulumerkintää",
          label: "Muokkaa",
          modalActions: {
            submit: "Tallenna muutokset",
            cancel: "Peruuta",
          },
        },
        add: {
          title: "Lisää aikataulumerkintä",
          label: "Lisää",
          modalActions: {
            submit: "Luo aikataulumerkintä",
            cancel: "Peruuta",
          },
        },
        remove: {
          title: "Poista aikataulumerkintä",
          label: "Poista",
          message: (scheduleItemTitle: string) => (
            <>
              <p>
                Are you sure you want to remove the schedule item{" "}
                <strong>{scheduleItemTitle}</strong>?
              </p>
              <p>
                This action cannot be undone. You will need to create a new
                schedule item if you want to add it back.
              </p>
            </>
          ),
          modalActions: {
            submit: "Poista aikataulumerkintä",
            cancel: "Sulje poistamatta",
          },
        },
      },

      messages: {
        created: "Aikataulumerkintä luotu.",
        updated: "Aikataulumerkintä päivitetty.",
        removed: "Aikataulumerkintä poistettu.",
      },
    },

    admin: {
      title: "Ohjelmanhallinta",
    },
  },

  Dimension: {
    listTitle: "Dimensiot",
  },

  Survey: {
    listTitle: "Kyselyt",
    singleTitle: "Kysely",
    forEvent: (eventName: string) => <>tapahtumalle {eventName}</>,
    tableFooter: (count: number) => (
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
        helpText: (
          <>
            Koneellisesti luettava nimi kyselylle. Teknisen nimen täytyy olla
            uniikki tapahtuman sisällä. Ei voi muuttaa luomisen jälkeen.
            Tekninen nimi voi sisältää pieniä kirjaimia, numeroita ja
            väliviivoja. Tekninen nimi tulee osaksi osoitetta:{" "}
            <code>/event-slug/form-slug</code> (esim.{" "}
            <code>/tracon2025/offer-program</code>).
          </>
        ),
      },
      title: "Otsikko",
      isActive: {
        title: "Avoinna vastauksille",
        untilFurtherNotice: "Avoinna toistaiseksi",
        untilTime: (formattedTime: String) => `Avoinna ${formattedTime} asti`,
        openingAt: (formattedTime: String) => `Avautuu ${formattedTime}`,
        closed: "Suljettu",
        adminOverride: {
          title: "Kysely ei ole käytössä",
          message: (
            <>
              Tämä kysely ei tällä hetkellä ota vastaan vastauksia. Näet tämän
              sivun vain, koska sinulla on ylläpitäjän oikeudet tähän kyselyyn.
              Käyttäjät, joilla ei ole ylläpitäjän oikeuksia, näkevät ainoastaan
              viestin joka ilmoittaa, että kysely ei ole käytössä.
            </>
          ),
        },
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
      responsesEditableUntil: {
        title: "Vastaukset muokattavissa tähän asti",
        helpText: (
          <>
            Jos tämä on asetettu, käyttäjät voivat muokata vastauksiaan tähän
            aikaan asti. Jos tätä ei ole asetettu, vastauksia ei voi muokata.
            (Voit myös asettaa dimension arvolle asetuksen{" "}
            <em>Lukitse kohde muokkauksilta</em> lukitaksesi muokkauksilta
            vastaukset joilla on kyseinen arvo.)
          </>
        ),
      },
      countResponses: "Vastauksia",
      languages: "Kielet",
      actions: "Toiminnot",
      anonymity: {
        secondPerson: {
          title: "Vastausten yhdistäminen sinuun",
          choices: {
            HARD: "Vastaukset ovat anonyymejä. Et voi palata katsomaan tai muokkaamaan vastauksiasi.",
            SOFT: "Jos vastaat tähän kyselyyn kirjautuneena, se yhdistetään käyttäjätiliisi, jotta voit palata katsomaan tai muokkaamaan vastauksiasi, mutta käyttäjäprofiiliasi ei jaeta kyselyn omistajan kanssa.",
            NAME_AND_EMAIL:
              "Jos vastaat tähän kyselyyn kirjautuneena, se yhdistetään käyttäjätiliisi. Nimesi ja sähköpostiosoitteesi jaetaan kyselyn omistajan kanssa. Voit palata katsomaan tai muokkaamaan vastauksiasi.",
            FULL_PROFILE:
              "Jos vastaat tähän kyselyyn kirjautuneena, se yhdistetään käyttäjätiliisi. Koko käyttäjäprofiilisi jaetaan kyselyn omistajan kanssa. Voit palata katsomaan tai muokkaamaan vastauksiasi.",
          },
        },
        thirdPerson: {
          title: "Vastausten yhdistäminen käyttäjään",
          choices: {
            HARD: "Vastaukset ovat anonyymejä. Käyttäjät eivät voi palata katsomaan tai muokkaamaan vastauksiaan.",
            SOFT: "Jos käyttäjä vastaa tähän kyselyyn kirjautuneena, hänen vastauksensa yhdistetään hänen käyttäjätiliinsä, jotta hän voi palata katsomaan tai muokkaamaan vastauksiaan, mutta hänen henkilöllisyyttään ei jaeta sinulle.",
            NAME_AND_EMAIL:
              "Jos käyttäjä vastaa tähän kyselyyn kirjautuneena, hänen vastauksensa yhdistetään hänen käyttäjätiliinsä. Hänen nimensä ja sähköpostiosoitteensa jaetaan sinulle. Hän voi palata katsomaan tai muokkaamaan vastauksiaan.",
            FULL_PROFILE:
              "Jos käyttäjä vastaa tähän kyselyyn kirjautuneena, hänen vastauksensa yhdistetään hänen käyttäjätiliinsä. Koko käyttäjäprofiili jaetaan sinulle. Hän voi palata katsomaan tai muokkaamaan vastauksiaan.",
          },
        },
        admin: {
          title: "Vastausten yhdistäminen käyttäjään",
          helpText: "HUOM! Et voi muuttaa tätä kyselyn luonnin jälkeen!",
          choices: {
            HARD: "Täysin anonyymi",
            SOFT: "Kevyesti anonyymi",
            NAME_AND_EMAIL: "Nimi ja sähköpostiosoite",
            FULL_PROFILE: "Koko profiili",
          },
        },
      },
      dimensions: "Dimensiot",
      dimension: "Dimensio",
      dimensionDefaults: {
        title: "Oletusdimensiot",
        description: (
          <>
            Nämä dimensioiden arvot asetetaan automaattisesti uusille
            kyselyvastauksille. Teknisten dimensioiden arvoja ei voi muuttaa.
          </>
        ),
        technicalDimensionsCannotBeChanged:
          "Teknisten dimensioiden arvoja ei voi muuttaa.",
      },
      values: "Arvot",
      value: "Arvo",
      sequenceNumber: "Järjestysnumero",
      originalCreatedAt: "Luotu (alkuperäinen versio)",
      originalCreatedBy: "Lähettäjä (alkuperäinen versio)",
      currentVersionCreatedAt: "Luotu (uusin versio)",
      currentVersionCreatedBy: "Lähettäjä (uusin versio)",
      versionHistory: "Versiohistoria",
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
      protectResponses: {
        title: "Suojaa vastaukset",
        helpText:
          "Jos tämä on valittuna, kyselyn vastauksia ei voi poistaa. Voit käyttää tätä suojaamaan kyselyn vastauksia tahattomalta poistolta.",
      },
      maxResponsesPerUser: {
        title: "Käyttäjän vastausten maksimimäärä",
        helpText:
          "Yksittäisen käyttäjän vastausten maksimimäärä tähän kyselyyn. Jos arvoksi on asetettu 0, määrää ei rajoiteta. Huomaathan, että tämä vaikuttaa ainoastaan sisäänkirjautuneisiin käyttäjiin. Jotta rajoitus toimisi, kyselyyn vastaaminen tulee olla rajoitettu sisäänkirjautuneille käyttäjille.",
      },
      alsoAvailableInThisLanguage: (
        LanguageLink: ({ children }: { children: ReactNode }) => JSX.Element,
      ) => (
        <>
          Tämä lomake on saatavilla myös <LanguageLink>suomeksi</LanguageLink>.
        </>
      ),
      cloneFrom: {
        title: "Kopioi olemassaolevasta",
        helpText:
          "Jos tämä on valittuna, uusi kysely luodaan kopiona valitusta kyselystä. Dimensiot sekä kieliversiot teksteineen ja kentteineen kopioidaan, mutta vastauksia ei.",
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
      viewResponse: {
        title: "Näytä vastaus",
        label: "Näytä",
      },
      viewResponses: "Vastaukset",
      toggleSubscription: "Ilmoita vastauksista",
      submit: "Lähetä",
      deleteVisibleResponses: {
        title: "Poista vastaukset",
        confirmation: (countResponses: number) => (
          <>
            Haluatko varmasti poistaa parhaillaan näkyvissä olevat{" "}
            <strong>{countResponses}</strong> vastausta?
          </>
        ),
        responsesProtected:
          "Tämän kyselyn vastaukset on suojattu. Jos haluat poistaa vastauksia, kytke ensin vastausten suojaus pois kyselyn asetuksista.",
        cannotDelete: "Vastauksia ei voi poistaa.",
        noResponsesToDelete: "Ei vastauksia poistettavaksi.",
        modalActions: {
          submit: "Poista vastaukset",
          cancel: "Peruuta poistamatta",
        },
      },
      deleteResponse: {
        title: "Poista vastaus",
        confirmation: "Haluatko varmasti poistaa tämän vastauksen?",
        cannotDelete: "Tätä vastausta ei voi poistaa.",
        modalActions: {
          submit: "Poista vastaus",
          cancel: "Peruuta poistamatta",
        },
      },
      editResponse: {
        title: "Muokkaa vastausta",
        label: "Muokkaa",
        cancel: "Peru muokkaus",
        editingOwn: (formattedCreatedAt: ReactNode) => (
          <>
            Muokkaat vastausta, jonka lähetit {formattedCreatedAt}. Muokkauksesi
            astuvat voimaan vasta kun lähetät lomakkeen.
          </>
        ),
        editingOthers: (
          formattedCreatedAt: ReactNode,
          createdBy: ReactNode,
        ) => (
          <>
            Muokkaat vastausta, jonka on lähettänyt <strong>{createdBy}</strong>{" "}
            {formattedCreatedAt}. Muokkauksesi astuvat voimaan vasta kun lähetät
            lomakkeen.
          </>
        ),
        cannotEdit: (
          <>
            <h1>Vastausta ei voi muokata</h1>
            <p>Et voi muokata tätä vastausta tällä hetkellä.</p>
          </>
        ),
      },
      exportDropdown: {
        dropdownHeader: "Lataa vastaukset",
        excel: "Lataa Excel-tiedostona",
        zip: "Lataa liitteineen (zip)",
      },
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
            Poista arvo <strong>{dimensionTitle}</strong> dimensionsta{" "}
            <strong>{valueTitle}</strong>?
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
      editDimensions: "Muokkaa dimensioita ja arvoja",
      editDimension: "Muokkaa dimensiota",
      editDimensionValue: "Muokkaa arvoa",
      editSurvey: "Muokkaa",
      viewProfile: {
        title: "Näytä käyttäjäprofiili",
        modalActions: {
          submit: "Tässä modaalissa ei ole sulkunappia :)",
          cancel: "Sulje",
        },
      },
    },
    errors: {
      noLanguageVersions: {
        title: "Kyselyllä ei ole kieliversioita",
        message: (
          <>
            Tällä kyselyllä ei ole yhtään kieliversiota. Kyselyyn ei voi vastata
            ennen kuin kyselyn omistaja lisää vähintään yhden kieliversion.
          </>
        ),
      },
      surveyNotActive: {
        title: "Kysely ei ole avoinna",
        message: <>Tämä kysely ei tällä hetkellä ota vastaan vastauksia.</>,
      },
    },
    messages: {
      responseEdited: "Muokkaus tallennettiin.",
    },
    tabs: {
      summary: "Yhteenveto",
      responses: "Vastaukset",
      properties: "Kyselyn asetukset",
      addLanguage: "Lisää kieliversio",
      texts: (languageName: string) => `Tekstit (${languageName})`,
      fields: (languageName: string) => `Kentät (${languageName})`,
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
    specialPurposeSurvey: {
      title: "Kyselyyn ei voi vastata tätä kautta",
      defaultMessage: (
        <>
          Tämän kyselyn käyttötarkoitusta on rajoitettu, eikä siihen voi vastata
          tämän näkymän kautta.
        </>
      ),
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
    deleteLanguageModal: {
      title: "Poista kieliversio",
      confirmation: (languageName: string) => (
        <>
          Haluatko varmasti poistaa kieliversion <strong>{languageName}</strong>
          ?
        </>
      ),
      modalActions: {
        submit: "Poista",
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
          helpText: (
            <>
              Koneluettava, lyhyt nimi dimensiolle. Teknistä nimeä ei voi
              muuttaa dimension luomisen jälkeen. Voi sisältää pieniä kirjaimia,
              numeroita ja väliviivoja (-). Tulee osaksi osoitetta
              suodatettaessa: <code>dimensio=arvo</code> (esim.{" "}
              <code>program-type=panel</code>).
            </>
          ),
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
        isPublic: {
          title: "Julkinen",
          helpText:
            "Jos tämä on valittuna, tämän dimension arvoja voidaan näyttää käyttäjille jotka eivät ole ylläpitäjiä.",
        },
        behaviourFlagsHeader: {
          title: "Toiminta",
          helpText:
            "Nämä asetukset muokkaavat dimension toimintaa eri näkymissä. Voit useimmissa tapauksissa jättää nämä asetukset oletusarvoihinsa.",
        },
        isListFilter: {
          title: "Luettelonäkymän suodatin",
          helpText:
            "Jos tämä on valittuna, tämä dimensio näytetään luettelonäkymissä luetteloa suodattavana alasvetovalikkona.",
        },
        isShownInDetail: {
          title: "Näytetään yksityiskohtanäkymissä",
          helpText:
            "Jos tämä on valittuna, tämän dimension arvot näytetään yksittäistä kohdetta käsittelevissä yksityiskohtanäkymissä.",
        },
        isNegativeSelection: {
          title: "Käänteinen valinta",
          helpText:
            "Jos tämä on valittuna, tämä dimensio näytetään suodattimena siten, että oletuksena kaikki dimension arvot ovat valittuna, ja käyttäjän oletetaan ruksaavan niistä pois ne joita hän ei halua. Huomaathan, että tämä on vain vihje käyttöliittymän toteutukselle ja kaikki käyttöliittymät eivät välttämättä tue tätä.",
        },
        valueOrdering: {
          title: "Arvojen järjestys",
          helpText:
            "Määrittää, missä järjestyksessä tämän dimension arvot esitetään käyttöliittymässä.",
          choices: {
            MANUAL: "Manuaalinen (vedä ja pudota järjestääksesi)",
            TITLE: "Otsikko (lokalisoitu)",
            SLUG: "Tekninen nimi",
          },
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
          helpText: (
            <>
              Koneluettava, lyhyt nimi arvolle. Teknistä nimeä ei voi muuttaa
              arvon luomisen jälkeen. Voi sisältää pieniä kirjaimia, numeroita
              ja väliviivoja (-). Tulee osaksi osoitetta suodatettaessa:{" "}
              <code>dimensio=arvo</code> (esim. <code>program-type=panel</code>
              ).
            </>
          ),
        },
        color: {
          title: "Väri",
          helpText:
            "Arvon väri vastauslistassa. Käytä kirkkaita värejä: ne vaalenevat tai tummenevat tarvittaessa.",
        },
        isSubjectLocked: {
          title: "Lukitse kohde muokkauksilta",
          helpText:
            "Jos tämä on asetettu, tämän arvon liittäminen kohteeseen lukitsee kohteen muokkauksilta.",
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
      actions: {
        submit: "Tallenna kentät",
      },
    },
    ResponseHistory: {
      title: "Vanhat versiot",
      message:
        "Tätä vastausta on muokattu. Tämä on vastauksen ajantasaisin versio. Alta löydät vanhat versiot.",
    },
    OldVersionAlert: {
      title: "Tämä on vanha versio vastauksesta",
      message: "Vastausta on muokattu. Tämä on vanha versio.",
      actions: {
        returnToCurrentVersion: "Palaa uusimpaan versioon",
      },
    },
  },

  Involvement: {
    adminTitle: "Henkilötietojen hallinta",
    listTitle: "Henkilöhaku",
    forEvent(eventName: string) {
      return <>tapahtumalle {eventName}</>;
    },
    attributes: {
      involvement: {
        title: "Osallistuminen",
      },
      count: (numPeople: number, numInvolvements: number) => (
        <>
          Näytetään {numPeople} {numPeople === 1 ? "henkilö" : "henkilöä"}{" "}
          joilla on yhteensä {numInvolvements} osallistumista.
        </>
      ),
      title: {
        title: "Otsikko",
        missing: "Ei otsikkoa",
      },
      type: {
        title: "Tyyppi",
        choices: {
          PROGRAM_HOST: "Ohjelmanumero",
          PROGRAM_OFFER: "Ohjelmatarjous",
          SURVEY_RESPONSE: "Kyselyvastaus",
        },
      },
      isActive: {
        title: "Tila",
        choices: {
          active: "Aktiivinen",
          inactive: "Ei aktiivinen",
        },
      },
    },
    messages: {},
    filters: {
      searchPlaceholder: "Hae nimellä tai sähköpostilla",
    },
    noFiltersApplied: (numPeople: number, numInvolvements: number) => (
      <>
        Suodattamaton lista piilotettu ({numPeople} henkilö
        {numPeople === 1 ? "" : "ä"} ja {numInvolvements}{" "}
        {numInvolvements === 1 ? "osallistuminen" : "osallistumista"}). Tarkenna
        hakua nähdäksesi tulokset.
      </>
    ),
  },

  Registry: {
    singleTitle: "Henkilörekisteri",
    listTitle: "Henkilörekisterit",
  },

  Invitation: {
    listTitle: "Avoimet kutsut",
    listDescription: (
      <>
        Nämä henkilöt on kutsuttu ohjelmanpitäjiksi tähän ohjelmanumeroon, mutta
        he eivät ole vielä hyväksyneet kutsua.
      </>
    ),
    attributes: {
      createdAt: "Lähetysaika",
      email: "Sähköposti",
      count: (numInvitations: number) =>
        numInvitations === 1 ? (
          <>Yksi avoin kutsu.</>
        ) : (
          <>{numInvitations} avointa kutsua.</>
        ),
      program: {
        title: "Ohjelmanumeron tiedot",
        editLater: "Pääset muokkaamaan ohjelmanumeron tietoja myöhemmin.",
      },
    },
    errors: {
      alreadyUsed: {
        title: "Kutsu on jo käytetty",
        message: "Tämä kutsu on jo käytetty. Kutsun voi käyttää vain kerran.",
      },
    },
    actions: {
      revoke: {
        title: "Peru kutsu",
        label: "Peru",
        message: (email: string) => (
          <>
            Haluatko varmasti perua osoitteeseen <strong>{email}</strong>{" "}
            lähetetyn kutsun? Vastaanottajalle ei lähetetä ilmoitusta
            peruutuksesta. Jos tulet toisiin ajatuksiin, on sinun lähetettävä
            vastaanottajalle uusi kutsu.
          </>
        ),
        modalActions: {
          submit: "Peru kutsu",
          cancel: "Sulje perumatta",
        },
      },
      resend: {
        title: "Kutsun uudelleenlähetys",
        label: "Lähetä uudelleen",
        message: (email: string) => (
          <>
            Haluatko lähettää osoitteeseen <strong>{email}</strong> lähetetyn
            kutsun uudelleen? Vastaanottaja saa uuden sähköpostiviestin, joka on
            sisällöltään sama kuin alkuperäinen kutsuviesti.
          </>
        ),
        modalActions: {
          submit: "Lähetä uudelleen",
          cancel: "Sulje uudelleenlähettämättä",
        },
      },
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
      sv: "ruotsi",
    },
    // NOTE: value always in target language
    switchTo: {
      fi: "suomeksi",
      en: "In English",
      sv: "på svenska",
    },
  },
};

export default translations;
