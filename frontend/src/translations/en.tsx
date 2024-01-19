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

    Tabs: {
      design: "Design",
      preview: "Preview",
      properties: "Properties",
    },

    FormPropertiesForm: {
      flags: {
        title: "Behaviour",
      },
      title: {
        title: "Form title",
        helpText:
          "Human-readable form title. May not be displayed in all contexts.",
      },
      slug: {
        title: "Technical name",
        helpText:
          "Machine-readable form name. Will be a part of the URL of the form. Valid characters: letters A-Za-z, numbers 0-9, underscore _. Must not start with a number.",
      },
      layout: {
        title: "Layout",
        helpText:
          "May not take effect in some contexts (eg. space-constrained forms may be forced to be horizontal).",
        choices: {
          horizontal: "Horizontal",
          vertical: "Vertical",
        },
      },
      standalone: {
        title: "Stand-alone",
        helpText:
          "Stand-alone forms can be filled using the generic form view. Non-stand-alone forms can only be filled when embedded in another use-case.",
      },
      active: {
        title: "Active",
        helpText:
          "Inactive forms cannot be filled. Only applies to stand-alone forms.",
      },
      loginRequired: {
        title: "Login required",
        helpText: "Only applies to stand-alone forms.",
      },
    },

    EditFieldForm: {
      name: {
        title: "Technical name",
        helpText:
          "Machine-readable field name. Valid characters: letters A-Za-z, numbers 0-9, underscore _. Must not start with a number.",
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
      options: {
        title: "Options",
        helpText: "value=label pairs, separated by newline",
      },
    },

    FieldTypes: {
      SingleLineText: "Single line text field",
      MultiLineText: "Multi-line text field",
      Divider: "Divider",
      StaticText: "Static text",
      Spacer: "Empty space",
      SingleCheckbox: "Single check box",
      SingleSelect: "Single select drop-down",
    },

    RemoveFieldModal: {
      title: "Confirm field removal",
      message: "Remove the selected field?",
      yes: "Yes, remove",
      no: "No, cancel",
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
    summaryTitle: "Response summary",
    ownResponsesTitle: "My responses",
    responseTableFooter: (count: number) => (
      <>
        {count} response{count === 1 ? "" : "s"}.
      </>
    ),
    dimensionTableFooter: (countDimensions: number, countValues: number) => (
      <>
        Total {countDimensions} dimension{countDimensions === 1 ? "" : "s"},{" "}
        {countValues} value{countValues === 1 ? "" : "s"}.
      </>
    ),
    attributes: {
      slug: "Slug",
      title: "Title",
      isActive: {
        title: "Receiving responses",
        untilFurtherNotice: "Open until further notice",
        untilTime: (time: Date) => `Open until ${time.toLocaleString()}`,
        openingAt: (time: Date) => `Opening at ${time.toLocaleString()}`,
        closed: "Closed",
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
    },
    actions: {
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
      summary: "Summary",
      submit: "Submit",
      downloadAsExcel: "Download as Excel",
      returnToResponseList: "Return to the list of responses",
      returnToSurveyList: "Return to the list of surveys",
      saveDimensions: "Save dimensions",
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

  // Do not translate
  LanguageSwitcher: {
    // NOTE: value always in target language
    supportedLanguages: {
      fi: "suomeksi",
      en: "In English",
    },
  },
};

export type Translations = typeof translations;
export default translations;
