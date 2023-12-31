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
  Navigation: {
    forms: "Forms",
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

  SurveyView: {
    thankYou: {
      title: "Thank you for your answers!",
      defaultMessage:
        "Your answers have been recorded. You can now close this tab.",
    },
  },

  EventSurveyResponse: {
    listTitle: "Responses",
    singleTitle: "Response",
    returnToResponseList: "Return to the list of responses",
    attributes: {
      createdAt: "Created at",
      language: "Language",
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
  },

  // Do not translate
  LanguageSelection: {
    // NOTE: quality of life hack only until we have a third language
    currentLanguage: {
      nameInCurrentLanguage: "In English",
      code: "en",
    },
    otherLanguage: {
      nameInOtherLanguage: "suomeksi",
      code: "fi",
    },
  },
};

export type Translations = typeof translations;
export default translations;
