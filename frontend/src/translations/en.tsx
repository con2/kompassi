const translations = {
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
    boolean: {
      true: "Yes",
      false: "No",
    },
  },
  Profile: {
    attributes: {
      displayName: {
        title: "Name",
      },
      email: {
        title: "Email",
      },
    },
    keysView: {
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
    tickets: "Tickets",
    responses: "Survey responses",
    keys: "Encryption keys",
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

    attributes: {
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

    editFieldForm: {
      slug: {
        title: "Technical name",
        helpText:
          "Machine-readable field name. Valid characters: letters A-Za-z, numbers 0-9, underscore _. Must not start with a number. The slug must be the same in different languages.",
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
        helpText:
          'Each line should contain one choice in the form of "slug: Choice shown to the user".',
      },
      questions: {
        title: "Questions",
        helpText:
          'Each line should contain one question in the form of "slug: Question shown to the user".',
      },
      encryptTo: {
        title: "Encrypt to",
        helpText:
          "If you want to encrypt the responses to this field, enter the user names of users who should be able to decrypt the responses (one per line). These users must have a key pair generated in their profile.",
      },
    },

    fieldTypes: {
      SingleLineText: "Single line text",
      MultiLineText: "Multi-line text",
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
      DateField: "Date",
      DateTimeField: "Date and time",
      TimeField: "Time",
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

  Tickets: {
    title: "Purchase tickets",
    forEvent: (eventName: string) => <>for {eventName}</>,
    returnToTicketsPage: "Return to the tickets page",
    noProducts: {
      title: "No products available",
      message: "There are no products available for purchase at the moment.",
    },
    productsTable: {
      product: "Product",
      unitPrice: "Unit price",
      quantity: {
        title: "Quantity",
        unit: "pcs",
      },
      total: "Total",
    },
    contactForm: {
      title: "Contact information",
      fields: {
        firstName: {
          title: "First name",
        },
        lastName: {
          title: "Last name",
        },
        email: {
          title: "Email",
          helpText:
            "Check the email address carefully! Your tickets will be sent to this address.",
        },
        phone: {
          title: "Phone number",
        },
      },
    },
    orderPage: {
      title: (orderNumber: string) => <>Order {orderNumber}</>,
      payButtonText: "Pay",
    },
    orderStatus: {
      UNKNOWN: {
        title: "Unknown order status",
        shortTitle: "Unknown",
        message:
          "The status of your order is unknown. Please contact the event organizer for more information.",
      },
      PENDING: {
        title: "Your order is awaiting payment",
        shortTitle: "Awaiting payment",
        message:
          "Your order has been confirmed and the products have been reserved to you, but we have not yet received your payment. Please use the button below to pay for your order as soon as possible. Unpaid orders will be eventually cancelled.",
      },
      PAID: {
        title: "Your order is complete!",
        shortTitle: "Paid",
        message:
          "Your order has been paid. You will receive a confirmation email shortly. If there are electronic tickets, they will be attached to the email.",
      },
      CANCELLED: {
        title: "Your order has been cancelled",
        shortTitle: "Cancelled",
        message:
          "Your order has been cancelled. If there were electronic tickets in the order, they have been invalidated. If you believe this is an error, please contact the event organizer.",
      },
      REFUNDED: {
        title: "Your order has been refunded",
        shortTitle: "Refunded",
        message:
          "Your order has been refunded. If there were electronic tickets in the order, they have been invalidated. If you believe this is an error, please contact the event organizer.",
      },
    },
    errors: {
      NOT_ENOUGH_TICKETS: {
        title: "Not enough tickets",
        message:
          "One or more of the products you tried to purchase are no longer available in the quantity you requested.",
      },
      INVALID_ORDER: {
        title: "Invalid order",
        message:
          "The details you entered on the order page were not accepted. Please check your order and try again.",
      },
      UNKNOWN_ERROR: {
        title: "Error processing order",
        message:
          "An error occurred while processing your order. Please try again later.",
      },
      ORDER_NOT_FOUND: {
        title: "Order not found",
        message:
          "The order you are trying to view does not exist or is not associated with your user account.",
        actions: {
          returnToOrderList: "Return to list of orders",
          returnToTicketsPage: "Return to the tickets page",
        },
      },
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
    profile: {
      title: "Ticket orders",
      description:
        "Here you can see your ticket orders made in 2025 and later. You can pay for unpaid orders and download your electronic tickets here.",
      haveUnlinkedOrders: {
        title: "Confirm your email address to see more orders",
        message:
          "There are ticket orders associated with your email address that are not linked to your user account. Confirm your email address to see these orders.",
      },
      attributes: {
        orderNumber: "Order number",
        createdAt: "Order date",
        eventName: "Event",
        totalPrice: "Total",
        actions: "Actions",
        status: "Status",
        totalOrders: (numOrders: number) => (
          <>
            Total {numOrders} order{numOrders === 1 ? "" : "s"}.
          </>
        ),
      },
      actions: {
        confirmEmail: {
          title: "Confirm email address",
          description:
            "An email will be sent to the email address of your user account. Follow the instructions in the email to confirm your email address and see the rest of your orders.",
          modalActions: {
            submit: "Send confirmation message",
            cancel: "Cancel",
          },
        },
        pay: {
          title: "Pay",
        },
        downloadTickets: {
          title: "Download tickets",
        },
      },
    },
    admin: {
      tabs: {
        orders: "Orders",
        products: "Products",
        quotas: "Quotas",
        reports: "Reports",
        ticketControl: "Ticket control",
      },
      products: {
        title: "Products",
        forEvent: (eventName: string) => <>for {eventName}</>,
        attributes: {
          title: "Title",
          description: "Description",
          price: "Price",
          isAvailable: {
            title: "Availability schedule",
            untilFurtherNotice: "Available until further notice",
            untilTime: (formattedTime: String) =>
              `Available until ${formattedTime}`,
            openingAt: (formattedTime: String) =>
              `Will become available at ${formattedTime}`,
            notAvailable: "Not available",
          },
          availableFrom: "Available from",
          availableUntil: "Available until",
          countPaid: "Paid",
          countReserved: {
            title: "Sold",
            description:
              "In addition to paid orders, includes those orders that have been confirmed but not yet paid.",
          },
          countAvailable: "Remaining",
          countTotal: "Total",
          actions: "Actions",
          totalReserved: "Total sold",
          totalPaid: "Total paid",
        },
      },
      quotas: {
        title: "Quotas",
        forEvent: (eventName: string) => <>for {eventName}</>,
      },
    },
  },

  NewProgramView: {
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

  Program: {
    listTitle: "Program",
    singleTitle: "Program item",
    inEvent: (eventName: string) => <>in {eventName}</>,
    attributes: {
      title: "Title",
      placeAndTime: "Location and time",
      actions: "Actions",
    },
    actions: {
      returnToProgramList: (eventName: string) =>
        `Return to the program schedule of ${eventName}`,
      addTheseToCalendar: "Add these program items to your calendar",
      addThisToCalendar: "Add this program item to your calendar",
      signUpForThisProgram: "Sign up for this program item",
    },
    favorites: {
      markAsFavorite: "Mark as favorite",
      unmarkAsFavorite: "Unmark as favorite",
      signInToAddFavorites:
        "By logging in, you can mark program items as favorites, filter this view to show only favorites and add favorite program items to your calendar.",
    },
    filters: {
      showOnlyFavorites: "Show only favorites",
      hidePastPrograms: "Hide past program items",
    },
    tabs: {
      cards: "Cards",
      table: "Table",
    },
    feedback: {
      viewTitle: "Give feedback",
      notAcceptingFeedback: "This program item is not accepting feedback.",
      fields: {
        feedback: {
          title: "Feedback",
          helpText:
            "How did you like the program? Please be constructive and empathetic towards the program host :) Your feedback will be shared with the program host.",
        },
        kissa: {
          title: "Which animal says meow?",
          helpText: "Please answer to prove you are not a robot. Hint: Cat.",
        },
      },
      actions: {
        returnToProgram: "Return to the program item",
        submit: "Submit feedback",
      },
      anonymity: {
        title: "Connecting your response to you",
        description:
          "If you give program feedback while logged in, your user profile will be connected to your feedback. However, your user profile will not be shared with the program host.",
      },
      thankYou: {
        title: "Thank you for your feedback!",
        description: "Your feedback has been recorded.",
      },
    },
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
    theseProfileFieldsWillBeShared:
      "When you submit this survey, the following information will be shared with the survey owner:",
    correctInYourProfile: (profileLink: string) => (
      <>
        If these are not correct, please correct them in your{" "}
        <a href={profileLink} target="_blank" rel="noopener noreferrer">
          profile
        </a>{" "}
        (opens in a new tab).
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
        untilTime: (formattedTime: String) => `Open until ${formattedTime}`,
        openingAt: (formattedTime: String) => `Opening at ${formattedTime}`,
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
            SOFT: "If you answer this survey while logged in, it will be connected to your user account, so that you can return to view or edit your responses, but your user profile will not be shared with the survey owner.",
            NAME_AND_EMAIL:
              "If you answer this survey while logged in, it will be connected to your user account. Your name and email address will be shared with the survey owner. You can return to view or edit your responses.",
          },
        },
        thirdPerson: {
          title: "Connecting responses to users",
          choices: {
            HARD: "Responses are anonymous. Users cannot return to view or edit their responses.",
            SOFT: "If the user answer this survey while logged in, their response will be connected to their user account, so that they can return to view or edit their responses, but their identities will not be shared with you.",
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
      viewResponses: "Responses",
      toggleSubscription: "Notify me about new responses",
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
      deleteSurvey: {
        title: "Remove survey",
        cannotRemove: "A survey that has responses cannot be removed.",
        confirmation: (surveyTitle: string) => (
          <>
            Are you sure you want to remove the survey{" "}
            <strong>{surveyTitle}</strong>?
          </>
        ),
        modalActions: {
          submit: "Remove",
          cancel: "Cancel",
        },
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
      texts: (languageName: string) => `Texts (${languageName})`,
      fields: (languageName: string) => `Fields (${languageName})`,
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
      language: {
        title: "Language",
        helpText: "Only supported languages can be added.",
      },
      copyFrom: {
        title: "Copy from",
        helpText:
          "The new language version will be a copy of the selected one. You can also select to start from scratch.",
      },
      actions: {
        submit: "Continue",
        cancel: "Cancel",
      },
    },
    deleteLanguageModal: {
      title: "Remove language version",
      confirmation: (languageName: string) => (
        <>
          Remove the <strong>{languageName}</strong> language version?
        </>
      ),
      modalActions: {
        submit: "Remove",
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
        isShownToSubject: {
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
        color: {
          title: "Color",
          helpText:
            "Color of the value in the response list. Use bright colors: they will be lightened or darkened as needed.",
        },
        isInitial: {
          title: "Initial value",
          helpText: "If set, this value will be applied to all new responses.",
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
      title: "Edit survey",
      actions: {
        submit: "Save fields",
      },
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
      fi: "Finnish",
      en: "English",
      sv: "Swedish",
    },
    // NOTE: value always in target language
    switchTo: {
      fi: "suomeksi",
      en: "In English",
      sv: "på svenska",
    },
  },
};

export type Translations = typeof translations;
export default translations;
