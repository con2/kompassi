const translations = {
  AccommodationOnboardingView: {
    title: "Accommodation onboarding",
  },
  Common: {
    ok: "OK",
    cancel: "Cancel",
    submit: "Submit",
    search: "Search",
    somethingWentWrong:
      "Something went wrong. There may be further information in the JavaScript console.",
    actions: "Actions",
    standardActions: {
      open: "Open",
      edit: "Edit",
      delete: "Delete",
      create: "Create",
    },
    formFields: {
      firstName: {
        title: "First name",
      },
      lastName: {
        title: "Last name",
      },
      email: {
        title: "Email address",
      },
      phone: {
        title: "Phone number",
      },
    },
  },
  // Note that this also defines the type for the messages object that can be passed to the InterceptingRouteModal component
  Modal: {
    submit: "Submit",
    cancel: "Cancel",
  },
  DataTable: {
    create: "Create",
  },
  Event: {
    title: "Events",
    headline: "Date and venue",
    name: "Name",
    workInProgress:
      "Kompassi v2 is a work in progress. This is not the final front page, but rather a demo of the table component.",
  },
  UserMenu: {
    responses: "Survey responses",
    signIn: "Sign in",
    signOut: "Sign out",
  },
  NotFound: {
    notFoundHeader: "Page not found",
    notFoundMessage:
      "The address does not conform to any of the recognized address patterns. Please double-check the address.",
  },
  SchemaForm: {
    submit: "Submit",
    warnings: {
      noFileUploaded: "No file uploaded.",
    },
  },
  Forms: {
    heading: "Forms",
    title: "Title",
    slug: "Slug",
    create: "New form",
  },
  FormResponses: {
    heading: "Form responses",
    form: "Form",
    user: "User",
  },
  MainView: {
    defaultErrorMessage:
      "Something went wrong. There may be further information in the JavaScript console.",
  },
  FormEditor: {
    editField: "Edit field",
    moveUp: "Move up",
    moveDown: "Move down",
    removeField: "Remove field",
    addFieldAbove: "Add field above",
    addField: "Add field",
    save: "Save form",
    cancel: "Return without saving",
    open: "Open form",
    saveFailedErrorMessage:
      "Something went wrong while saving the form. There may be further information in the JavaScript console.",

    tabs: {
      design: "Design",
      preview: "Preview",
      properties: "Properties",
    },

    editFieldForm: {
      slug: {
        title: "Technical name",
        helpText:
          "Machine-readable field name. Valid characters: letters A-Za-z, numbers 0-9, dash -. Must not start with a number.",
      },
      title: {
        title: "Title",
        helpText:
          "Human-readable field label. If unset, defaults to field name.",
      },
      helpText: {
        title: "Help text",
        helpText: "Displayed below the field.",
      },
      required: {
        title: "Required",
      },
      choices: {
        title: "Choices",
        helpText: "value=label pairs, separated by newline",
      },
    },

    formPropertiesForm: {
      title: {
        title: "Title",
        helpText: "Human-readable title for the form.",
      },
      description: {
        title: "Description",
        helpText: "Will be shown to the user at the top of the form.",
      },
      thankYouMessage: {
        title: "Thank you message",
        helpText:
          "Will be shown to the user after they have submitted the form. If the thank you message is not set, the default message will be shown.",
      },
    },

    fieldTypes: {
      SingleLineText: "Single line text field",
      MultiLineText: "Multi-line text field",
      Divider: "Divider",
      StaticText: "Static text",
      Spacer: "Empty space",
      SingleCheckbox: "Single check box",
      SingleSelect: "Single select",
      MultiSelect: "Multiple select",
      RadioMatrix: "Radio button matrix",
      FileUpload: "File upload",
      NumberField: "Number",
      DecimalField: "Decimal number",
    },

    removeFieldModal: {
      title: "Confirm field removal",
      message: "Remove the selected field?",
      actions: {
        submit: "Remove",
        cancel: "Cancel",
      },
    },

    editFieldModal: {
      title: "Edit field",
      actions: {
        submit: "Save field",
        cancel: "Cancel",
      },
    },
  },

  SplashView: {
    engagement: (
      <>
        Stay tuned while we reimplement key functions of the{" "}
        <strong style={{ whiteSpace: "nowrap" }}>
          Kompassi Event Management System
        </strong>{" "}
        using modern web technologies for better user experience and greater
        self-service customisability!
      </>
    ),
    backToKompassi: "Back to Kompassi",
  },

  EventsView: {
    title: "Events",
  },

  TicketsView: {
    title: "Purchase tickets",
    productsTable: {
      product: "Product",
      price: "Price",
      quantity: "Quantity",
    },
    contactForm: {
      title: "Contact information",
    },
    purchaseButtonText: "Purchase",
    acceptTermsAndConditions(url: string) {
      return (
        <>
          I accept the{" "}
          <a href={url} target="_blank" rel="noopener noreferrer">
            terms and conditions
          </a>{" "}
          (required).
        </>
      );
    },
  },

  NewProgrammeView: {
    title: "Offer a program item",
    engagement: (eventName: string) => (
      <>
        Thank you for your interest in offering programme at {eventName}! Please
        begin by selecting the type of program you wish to offer below.
      </>
    ),
    selectThisProgramType: "Select this program type",
    backToProgramFormSelection: "Back to program type selection",
    forEvent: (eventName: string) => <>for {eventName}</>,
    submit: "Submit",
  },

  Survey: {
    listTitle: "Surveys",
    singleTitle: "Survey",
    forEvent: (eventName: string) => <>for {eventName}</>,
    surveyTableFooter: (count: number) => (
      <>
        {count} survey{count === 1 ? "" : "s"}.
      </>
    ),
    responseListTitle: "Responses",
    responseDetailTitle: "Response",
    ownResponsesTitle: "My responses",
    showingResponses: (filteredCount: number, totalCount: number) => (
      <>
        Displaying {filteredCount} response{filteredCount === 1 ? "" : "s"}{" "}
        (total {totalCount}).
      </>
    ),
    dimensionTableFooter: (countDimensions: number, countValues: number) => (
      <>
        Total {countDimensions} dimension{countDimensions === 1 ? "" : "s"},{" "}
        {countValues} value{countValues === 1 ? "" : "s"}.
      </>
    ),
    summaryOf: (filteredCount: number, totalCount: number) => (
      <>
        Summary of {filteredCount} response{filteredCount === 1 ? "" : "s"}{" "}
        (total {totalCount}).
      </>
    ),
    attributes: {
      slug: {
        title: "Slug",
        helpText:
          "Machine-readable name of the survey. Must be unique within the event. Cannot be changed after creation.",
      },
      title: "Title",
      isActive: {
        title: "Receiving responses",
        untilFurtherNotice: "Open until further notice",
        untilTime: (time: Date) => `Open until ${time.toLocaleString()}`,
        openingAt: (time: Date) => `Opening at ${time.toLocaleString()}`,
        closed: "Closed",
      },
      activeFrom: {
        title: "Active from",
        helpText: "If set, the survey will open for responses at this time.",
      },
      activeUntil: {
        title: "Active until",
        helpText: "If set, the survey will close for responses at this time.",
      },
      countResponses: "Responses",
      languages: "Languages",
      actions: "Actions",
      anonymity: {
        secondPerson: {
          title: "Connecting your response to you",
          choices: {
            HARD: "Responses are anonymous. You cannot return to view or edit your responses.",
            SOFT: "If you answer this survey while logged in, it will be connected to your user account, so that you can return to view or edit your responses, but your identity will not be shared with the survey owner.",
            NAME_AND_EMAIL:
              "If you answer this survey while logged in, it will be connected to your user account. Your name and email address will be shared with the survey owner. You can return to view or edit your responses.",
          },
        },
        thirdPerson: {
          title: "Connecting responses to users",
          choices: {
            HARD: "Responses are anonymous. Users cannot return to view or edit their responses.",
            SOFT: "If the user answer thiss survey while logged in, their response will be connected to their user account, so that they can return to view or edit their responses, but their identities will not be shared with you.",
            NAME_AND_EMAIL:
              "If the user answers this survey while logged in, their response will be connected to their user account. Their names and email addresses will be shared with you. They can return to view or edit their responses.",
          },
        },
      },
      dimensions: "Dimensions",
      dimension: "Dimension",
      values: "Values",
      value: "Arvo",
      sequenceNumber: "Sequence number",
      createdAt: "Created at",
      createdBy: "Created by",
      event: "Event",
      formTitle: "Survey title",
      language: "Language",
      choice: "Choice",
      question: "Question",
      countMissingResponses: "No response",
      percentageOfResponses: "Share of responses",
      technicalDetails: "Technical details",
      loginRequired: {
        title: "Sign-in required",
        helpText:
          "If checked, the survey can only be filled in by signed-in users.",
      },
      maxResponsesPerUser: {
        title: "Maximum number of responses per user",
        helpText:
          "The maximum number of responses a single user can submit to this survey. If set to 0, there is no limit. Note that this only applies to signed-in users. To enforce the limit, select Sign-in required as well.",
      },
    },
    actions: {
      createSurvey: "Create survey",
      fillIn: {
        title: "Fill in",
        disabledTooltip: "Closed survey cannot be filled in",
      },
      share: {
        title: "Share",
        tooltip: "Copy link to clipboard",
        success: "A link to the survey has been copied to clipboard.",
      },
      viewResponses: "View responses",
      submit: "Submit",
      downloadAsExcel: "Download as Excel",
      returnToResponseList: "Return to the list of responses",
      returnToSurveyList: "Return to the list of surveys",
      returnToDimensionList: "Return to the list of dimensions",
      saveDimensions: "Save dimensions",
      saveProperties: "Save properties",
      addDimension: "Add dimension",
      addDimensionValue: "Add value",
      deleteDimension: {
        title: "Remove dimension",
        cannotRemove:
          "A dimension that has been associated with a response cannot be removed.",
        confirmation: (dimensionTitle: string) => (
          <>
            Remove dimension <strong>{dimensionTitle}</strong> and and all its
            values?
          </>
        ),
        modalActions: {
          submit: "Remove",
          cancel: "Cancel",
        },
      },
      deleteDimensionValue: {
        title: "Remove value",
        cannotRemove:
          "A value that has been associated with a response cannot be removed.",
        confirmation: (dimensionTitle: string, valueTitle: string) => (
          <>
            Remove value <strong>{valueTitle}</strong> from dimension{" "}
            <strong>{dimensionTitle}</strong>?
          </>
        ),
      },
      editDimension: "Edit dimension",
      editDimensionValue: "Edit value",
      editSurvey: "Edit",
    },
    tabs: {
      summary: "Summary",
      responses: "Responses",
      properties: "Survey properties",
      addLanguage: "Add language",
      languageVersion: (languageName: string) =>
        `Language version: ${languageName}`,
    },
    thankYou: {
      title: "Thank you for your answers!",
      defaultMessage:
        "Your answers have been recorded. You can now close this tab.",
    },
    maxResponsesPerUserReached: {
      title: "Maximum number of responses reached",
      defaultMessage: (
        maxResponsesPerUser: number,
        countResponsesByCurrentUser: number,
      ) =>
        `You have already submitted ${countResponsesByCurrentUser} response${
          countResponsesByCurrentUser === 1 ? "" : "s"
        } to this survey. The maximum number of responses per user is ${maxResponsesPerUser}.`,
    },
    warnings: {
      choiceNotFound:
        "Choice not found. It may have been removed after this response was submitted.",
    },
    checkbox: {
      checked: "Checked",
      unchecked: "Not checked",
    },
    addLanguageModal: {
      language: "Language",
      actions: {
        submit: "Continue",
        cancel: "Cancel",
      },
    },
    editDimensionModal: {
      editTitle: "Edit dimension",
      addTitle: "Add dimension",
      actions: {
        submit: "Save dimension",
        cancel: "Cancel",
      },
      attributes: {
        slug: {
          title: "Technical name",
          // TODO add pattern for slug and document it in helpText
          helpText:
            "Machine-readable dimension name. Cannot be changed after creation.",
        },
        localizedTitleHeader: {
          title: "Localized titles",
          helpText:
            "The title of the dimension in different languages. The title need not be provided in all supported languages: if the title is missing in the selected language, it will fall back first to the default language and then to the technical name.",
        },
        title: {
          fi: "Title in Finnish",
          en: "Title in English",
          sv: "Title in Swedish",
        },
        isKeyDimension: {
          title: "Key dimension",
          helpText:
            "Values of key dimensions are displayed to in the response list.",
        },
        isMultiValue: {
          title: "Multi-value",
          helpText:
            "If checked, multiple values can be selected for this dimension.",
        },
        isShownToRespondent: {
          title: "Shown to respondent",
          helpText:
            "If checked, the values of this dimension are shown to the respondent in the single response view under their profile. Additionally, if this dimension is also a key dimension, it is shown in the responses list under their profile.",
        },
      },
    },
    editValueModal: {
      editTitle: "Edit value",
      addTitle: "Add value",
      actions: {
        submit: "Save value",
        cancel: "Cancel",
      },
      attributes: {
        slug: {
          title: "Technical name",
          // TODO add pattern for slug and document it in helpText
          helpText:
            "Machine-readable name of the value. Cannot be changed after creation.",
        },
        localizedTitleHeader: {
          title: "Localized titles",
          helpText:
            "The title of the value in different languages. The title need not be provided in all supported languages: if the title is missing in the selected language, it will fall back first to the default language and then to the technical name.",
        },
        title: {
          fi: "Title in Finnish",
          en: "Title in English",
          sv: "Title in Swedish",
        },
      },
    },
    createSurveyModal: {
      title: "Create a new survey",
      actions: {
        submit: "Create",
        cancel: "Cancel",
      },
    },
    editSurveyPage: {
      title: "Muokkaa kyselyä",
    },
  },

  SignInRequired: {
    metadata: {
      title: "Sign-in required – Kompassi",
    },
    title: "Sign-in required",
    message: "You need to sign in to access this page.",
    signIn: "Sign in",
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

export type Translations = typeof translations;
export default translations;
