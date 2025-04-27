import { JSX, ReactNode } from "react";

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
      close: "Close",
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
    tickets: "Ticket orders",
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
      dimension: {
        title: "Dimension",
        helpText: "Which dimension should the field get its choices from?",
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
      DimensionSingleSelect: "Single select (Dimension)",
      MultiSelect: "Multiple select",
      DimensionMultiSelect: "Multiple select (Dimension)",
      RadioMatrix: "Radio button matrix",
      FileUpload: "File upload",
      NumberField: "Number",
      DecimalField: "Decimal number",
      DateField: "Date",
      DateTimeField: "Date and time",
      TimeField: "Time",
    },
    advancedFieldTypes: {
      SingleSelect: {
        promoteFieldToDimension: {
          title: "Convert to a dimension field",
          modalActions: {
            submit: "Proceed with conversion",
            cancel: "Cancel without converting",
          },
          existingDimension: (
            <>
              <p>
                Are you sure you want to convert this field to a dimension
                field?
              </p>
              <p>
                If you proceed, the following actions will be taken in{" "}
                <strong>all language versions</strong> of this survey:
              </p>
              <ol>
                <li>
                  New choices, if any, will be added to the existing dimension
                  of the same slug (technical name). Translations for them will
                  be extracted from all existing language versions and combined
                  by their slugs.
                </li>
                <li>
                  This field will be replaced by a dimension selection field
                  that will receive its choices from the aforementioned
                  dimension. Other attributes of the field will be retained.
                </li>
                <li>
                  Each response in which this field has been responded to will
                  have the answers to this field set as dimension values on that
                  response.
                </li>
              </ol>
              <p>This cannot be undone.</p>
            </>
          ),
          newDimension: (
            <>
              <p>
                Are you sure you want to convert this field to a dimension
                field?
              </p>
              <p>
                If you proceed, the following actions will be taken in{" "}
                <strong>all language versions</strong> of this survey:
              </p>
              <ol>
                <li>
                  A new dimension will be created with the same technical name
                  (slug) as this field. Choices and their translations will be
                  extracted from all existing language versions and combined by
                  their slugs.
                </li>
                <li>
                  This field will be replaced by a dimension selection field
                  that will receive its choices from the aforementioned
                  dimension. Other attributes of the field will be retained.
                </li>
                <li>
                  Each response in which this field has been responded to will
                  have the answers to this field set as dimension values on that
                  response.
                </li>
              </ol>
              <p>This cannot be undone.</p>
            </>
          ),
        },
      },
      DimensionSingleSelect: {
        description: (
          <>
            This field type displays a single selection field with a list of
            choices that are defined by a dimension. When the respondent selects
            a value for this field, that dimension value will be set on the
            response.
          </>
        ),
      },
      DimensionMultiSelect: {
        description: (
          <>
            This field type displays a multiple selection field with a list of
            choices that are defined by a dimension. When the respondent selects
            values for this field, those dimension values will be set on the
            response.
          </>
        ),
      },
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
    Product: {
      listTitle: "Products",
      forEvent: (eventName: string) => <>for {eventName}</>,
      noProducts: {
        title: "No products available",
        message: "There are no products available for purchase at the moment.",
      },
      actions: {
        editProduct: "Edit product",
        newProduct: {
          title: "New product",
          modalActions: {
            submit: "Create product",
            cancel: "Cancel",
          },
        },
        saveProduct: "Save product",
        unpublishAllProducts: "Unpublish all products",
        viewOldVersion: {
          title: "Old version of product",
          label: "View old version of product",
          modalActions: {
            submit: "",
            cancel: "Close",
          },
        },
        deleteProduct: {
          title: "Delete product",
          confirmation: (productName: string) => (
            <>
              Are you sure you want to delete the product{" "}
              <strong>{productName}</strong>? This action cannot be undone.
            </>
          ),
          modalActions: {
            submit: "Delete",
            cancel: "Cancel",
          },
          cannotDelete:
            "This product cannot be deleted because it has been sold.",
        },
      },
      // json serializable values only under clientAttributes
      clientAttributes: {
        product: "Product",
        title: "Title",
        createdAt: "Created at",
        unitPrice: {
          title: "Unit price",
          helpText: "Price per unit in euros.",
        },
        quantity: {
          title: "Quantity",
          unit: "pcs",
        },
        total: "Total",
        description: {
          title: "Description",
          helpText:
            "Title and description will be shown to the customer on the ticket purchase page.",
        },
        maxPerOrder: {
          title: "Maximum amount per order",
          helpText: "No more than this amount will be sold in one order.",
        },
        eticketsPerProduct: {
          title: "Number of electronic tickets per product",
          helpText:
            "The number of electronic ticket codes that will be generated for each instance of the product sold. If set to 0, no electronic tickets will be generated.",
        },
        availableFrom: {
          title: "Available from",
          helpText:
            "In order for the product to become available, this field must be set and the time set herein must have passed.",
        },
        availableUntil: {
          title: "Available until",
          helpText:
            "If set, the product will no longer be available after this time.",
        },
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
        revisions: {
          title: "Revisions of this product",
          description:
            "If a product is edited after being sold, a new revision will be created that will replace the product in the shop. Setting the availability schedule or quotas will not create a new revision.",
          current: "Current",
        },
        quotas: {
          title: "Quotas",
          helpText:
            "Quotas determine how many pieces of a product may be sold. A product may use multiple quotas; the quota that has the least stock determines the availability of the product. You can edit and create new quotas on the Quotas tab.",
        },
        selectedQuotas: "Selected quotas",
        soldOut: "Sold out",
        isAvailable: "Availability schedule",
        dragToReorder: "Drag to reorder",
        newProductQuota: {
          title: "Quota",
          helpText:
            "You can create a quota with the name of the product by setting the quota here. If you want to skip creating a quota and set the quotas later, you can leave this blank. Note that a product needs to be associated with at least one quota in order to become available.",
        },
      },
      serverAttributes: {
        isAvailable: {
          untilFurtherNotice: "Available until further notice",
          untilTime: (formattedTime: String) =>
            `Available until ${formattedTime}`,
          openingAt: (formattedTime: String) =>
            `Will become available at ${formattedTime}`,
          notAvailable: "Not available",
        },
      },
    },
    Quota: {
      listTitle: "Quotas",
      singleTitle: "Quota",
      forEvent: (eventName: string) => <>for {eventName}</>,
      actions: {
        newQuota: {
          title: "New quota",
          modalActions: {
            submit: "Create quota",
            cancel: "Cancel",
          },
        },
        editQuota: "Edit quota",
        saveQuota: "Save quota",
        deleteQuota: {
          title: "Delete quota",
          confirmation: (quotaName: string) => (
            <>
              Are you sure you want to delete the quota{" "}
              <strong>{quotaName}</strong>? This action cannot be undone.
            </>
          ),
          modalActions: {
            submit: "Delete",
            cancel: "Cancel",
          },
          cannotDelete:
            "This quota cannot be deleted because it has been associated with products. To delete, first unassociate the quota from all products.",
        },
      },
      attributes: {
        name: "Name",
        countTotal: {
          title: "Quota",
          helpTextNew:
            "How many units of products using this quota may at most be sold.",
          helpText: (countReserved: number) =>
            `How many units of products using this quota may at most be sold. There are currently ${countReserved} units sold; the quota cannot be adjusted lower than that.`,
        },
        totalReserved: "Total sold",
        products: {
          title: "Products using this quota",
          helpText:
            "A product may use multiple quotas; the quota that has the least stock determines the availability of the product.",
        },
      },
    },
    Order: {
      listTitle: "Orders",
      singleTitle: (orderNumber: string, paymentStatus: string) =>
        `Order ${orderNumber} (${paymentStatus})`,
      forEvent: (eventName: string) => <>for {eventName}</>,
      contactForm: {
        title: "Contact information",
      },
      profileMessage: (
        ProfileLink: ({ children }: { children: ReactNode }) => JSX.Element,
      ) => (
        <>
          If you have a user account with the email address you used to place
          this order, you can also view your orders and download electronic
          tickets from your <ProfileLink>profile</ProfileLink>.
        </>
      ),
      attributes: {
        orderNumberAbbr: "Order #",
        orderNumberFull: "Order number",
        createdAt: "Order date",
        eventName: "Event",
        totalPrice: "Total price",
        actions: "Actions",
        totalOrders: (numOrders: number) => (
          <>
            Total {numOrders} order{numOrders === 1 ? "" : "s"}.
          </>
        ),
        firstName: {
          title: "First name",
        },
        lastName: {
          title: "Last name",
        },
        displayName: {
          title: "Customer name",
        },
        email: {
          title: "Email",
          helpText:
            "Check the email address carefully! Your tickets will be sent to this address.",
        },
        phone: {
          title: "Phone number",
        },
        acceptTermsAndConditions: {
          title: "Terms and conditions accepted",
          checkboxLabel(url: string) {
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
        provider: {
          title: "Payment provider",
          choices: {
            NONE: "None",
            PAYTRAIL: "Paytrail",
            STRIPE: "Stripe",
          },
        },
        status: {
          title: "Status",
          choices: {
            NOT_STARTED: {
              title: "Your order is awaiting payment",
              shortTitle: "Not started",
              message:
                "Your order has been confirmed and the products have been reserved to you, but we have not yet received your payment. Please use the button below to pay for your order as soon as possible. Unpaid orders will be eventually cancelled.",
            },
            PENDING: {
              title: "Your order is awaiting payment",
              shortTitle: "Awaiting payment",
              message:
                "Your order has been confirmed and the products have been reserved to you, but we have not yet received your payment. Please use the button below to pay for your order as soon as possible. Unpaid orders will be eventually cancelled.",
            },
            FAILED: {
              title: "Payment failed",
              shortTitle: "Payment failed",
              message:
                "The payment for your order failed or was cancelled. Please try again. Unpaid orders will be eventually cancelled.",
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
            REFUND_REQUESTED: {
              title: "Your order has been refunded",
              shortTitle: "Refund requested",
              message:
                "Your order has been refunded. If there were electronic tickets in the order, they have been invalidated. If you believe this is an error, please contact the event organizer.",
            },
            REFUND_FAILED: {
              title: "Your order has been refunded",
              shortTitle: "Refund failed",
              message:
                "Your order has been refunded. If there were electronic tickets in the order, they have been invalidated. If you believe this is an error, please contact the event organizer.",
            },
            REFUNDED: {
              title: "Your order has been refunded",
              shortTitle: "Refunded",
              message:
                "Your order has been refunded. If there were electronic tickets in the order, they have been invalidated. If you believe this is an error, please contact the event organizer.",
            },
          },
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
        NO_PRODUCTS_SELECTED: {
          title: "No products selected",
          message: "Please select at least one product to purchase.",
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
      actions: {
        purchase: "Confirm order and proceed to payment",
        pay: "Pay for order",
        viewTickets: "View e-tickets",
        newOrder: "New order",
        search: "Search orders",
        saveContactInformation: "Save contact information",
        resendOrderConfirmation: {
          title: "Resend order confirmation",
          message: (emailAddress: string) => (
            <>
              <p>
                Are you sure you want to resend the order confirmation email
                (incl. electronic tickets, if any) to the customer?
              </p>
              <p>
                The confirmation email will be sent to the following address:{" "}
                <strong>{emailAddress}</strong>
              </p>
              <p>
                <strong>NOTE:</strong> If you are changing the email address,
                please make sure to remember to save contact information before
                resending the confirmation.
              </p>
            </>
          ),
          modalActions: {
            submit: "Resend",
            cancel: "Close without resending",
          },
        },
        cancelAndRefund: {
          title: "Cancel and refund",
          message: (
            <>
              <p>Are you sure you want to</p>
              <ol>
                <li>mark the order as cancelled,</li>
                <li>invalidate any electronic tickets,</li>
                <li>send a cancellation notice to the customer, and</li>
                <li>request the payment processor to refund the payment?</li>
              </ol>
            </>
          ),
          modalActions: {
            submit: "Cancel order and request refund",
            cancel: "Close without cancelling",
          },
        },
        refundCancelledOrder: {
          title: "Refund",
          message: (
            <p>
              Are you sure you want request the payment processor to refund the
              payment?
            </p>
          ),
          modalActions: {
            submit: "Request refund",
            cancel: "Close without refunding",
          },
        },
        cancelWithoutRefunding: {
          title: "Cancel without refunding",
          message: (
            <>
              <p>Are you sure you want to</p>
              <ol>
                <li>mark the order as cancelled,</li>
                <li>invalidate any electronic tickets, and</li>
                <li>send a cancellation notice to the customer?</li>
              </ol>
              <p>
                <strong>NOTE:</strong> No automatic refund will be made. If the
                payment needs to be refunded in part or in full, you will need
                to do this via the merchant panel of the payment processor, or
                use the &quot;Cancel and refund&quot; function.
              </p>
            </>
          ),
          modalActions: {
            submit: "Cancel order without refunding",
            cancel: "Close without cancelling",
          },
        },
        retryRefund: {
          title: "Retry refund",
          message: (
            <p>
              Are you sure you want to make a new request the payment processor
              to refund the payment?
            </p>
          ),
          modalActions: {
            submit: "Retry refund",
            cancel: "Close without refunding",
          },
        },
        refundManually: {
          title: "Refund manually",
          message: (
            <>
              <p>
                Are you sure you want to mark this order as manually refunded?
              </p>
              <p>
                <strong>NOTE:</strong> No further automatic refund will be
                attempted. It is entirely up to you to make sure the customer
                gets their money back.
              </p>
            </>
          ),
          modalActions: {
            submit: "Mark as manually refunded",
            cancel: "Close without marking",
          },
        },
        refundCommon: {
          refundMayFail: (
            <>
              <strong>NOTE:</strong> The refund may fail if there are not
              sufficient funds deposited with the payment processor. In this
              case, you need to transfer funds and retry the refund at a later
              date, or complete the refund via other means.
            </>
          ),
        },
      },
    },
    PaymentStamp: {
      listTitle: "Payment stamps",
      attributes: {
        createdAt: "Timestamp",
        correlationId: "Correlation ID",
        type: {
          title: "Type",
          choices: {
            ZERO_PRICE: "Zero price",
            CREATE_PAYMENT_REQUEST: "Create payment – Request",
            CREATE_PAYMENT_SUCCESS: "Create payment – OK",
            CREATE_PAYMENT_FAILURE: "Create payment – Failed",
            PAYMENT_REDIRECT: "Payment redirect",
            PAYMENT_CALLBACK: "Payment callback",
            CANCEL_WITHOUT_REFUND: "Cancel without refund",
            CREATE_REFUND_REQUEST: "Create refund – Request",
            CREATE_REFUND_SUCCESS: "Create refund – OK",
            CREATE_REFUND_FAILURE: "Create refund – Failed",
            REFUND_CALLBACK: "Refund callback",
            MANUAL_REFUND: "Manual refund",
          },
        },
      },
      actions: {
        view: {
          title: "View payment stamp",
          message: (
            <p>
              Payment stamps contain technical information about the payment
              process. This may be used to troubleshoot failed payments with the
              payment processor.
            </p>
          ),
          modalActions: {
            cancel: "Close",
            submit: "There is no submit button :)",
          },
        },
      },
    },
    Receipt: {
      listTitle: "Receipts",
      attributes: {
        id: "Correlation ID",
        createdAt: "Sent at",
        type: {
          title: "Type",
          choices: {
            PAID: "Order confirmation",
            CANCELLED: "Cancellation notice",
            REFUNDED: "Refund notice",
          },
        },
        status: {
          title: "Status",
          choices: {
            REQUESTED: "Requested",
            PROCESSING: "Processing",
            FAILURE: "Failed",
            SUCCESS: "Sent",
          },
        },
      },
    },
    Code: {
      listTitle: "Electronic ticket codes",
      attributes: {
        code: "Code",
        literateCode: "Literate code",
        usedOn: "Used on",
        productText: "Product",
        status: {
          title: "Status",
          choices: {
            UNUSED: "Unused",
            USED: "Used",
            MANUAL_INTERVENTION_REQUIRED: "Revoked",
            BEYOND_LOGIC: "Beyond logic",
          },
        },
      },
    },
    profile: {
      title: "Ticket orders",
      message:
        "Here you can see your ticket orders made in 2025 and later. You can pay for unpaid orders and download your electronic tickets here.",
      haveUnlinkedOrders: {
        title: "Confirm your email address to see more orders",
        message:
          "There are ticket orders associated with your email address that are not linked to your user account. Confirm your email address to see these orders.",
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
      },
      noOrders:
        "There are no orders associated with your user account to show.",
    },
    admin: {
      title: "Ticket shop admin",
      tabs: {
        orders: "Orders",
        products: "Products",
        quotas: "Quotas",
        reports: "Reports",
        ticketControl: "Ticket control",
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
    adminListTitle: "Program items",
    singleTitle: "Program item",
    inEvent: (eventName: string) => <>in {eventName}</>,
    attributes: {
      slug: {
        title: "Slug",
        helpText:
          "Machine-readable name of the program item. Must be unique within the event. Cannot be changed after creation. Can contain lower case letters, numbers and dashes (-). Will be part of the URL: <code>/EVENT-SLUG/programs/PROGRAM-SLUG</code> (eg. <code>/tracon2025/programs/opening-ceremony</code>).",
      },
      title: "Title",
      actions: "Actions",
      description: "Description",
      state: {
        title: "State",
        choices: {
          new: "New",
          accepted: "Accepted",
        },
      },
      programOffer: {
        title: "Program offer",
        message:
          "This program item was created based on the following program offer:",
      },
    },
    actions: {
      returnToProgramList: (eventName: string) =>
        `Return to the program schedule of ${eventName}`,
      returnToProgramAdminList: (eventName: string) =>
        `Return to the list of program items of ${eventName}`,
      addTheseToCalendar: "Add these program items to your calendar",
      addThisToCalendar: "Add this program item to your calendar",
      signUpForThisProgram: "Sign up for this program item",
      preview: "Preview schedule",
      preferences: "Preferences",
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

    adminDetailTabs: {
      basicInfo: "Basic info",
      scheduleItems: "Schedule",
      programHosts: "Program hosts",
      dimensions: "Dimensions",
      annotations: "Annotations",
    },

    ProgramForm: {
      singleTitle: "Program form",
      listTitle: "Program forms",
      tableFooter: (numForms: number) =>
        `${numForms} form${numForms === 1 ? "" : "s"}.`,
      attributes: {
        slug: {
          title: "Slug",
          helpText: (
            <>
              Machine-readable name of the program form. Must be unique within
              the event. Cannot be changed after creation. Can contain lower
              case letters, numbers and dashes (-). Will be part of the URL:{" "}
              <code>/event-slug/form-slug</code> (eg.{" "}
              <code>/tracon2025/offer-program</code>).
            </>
          ),
        },
      },
      actions: {
        viewOffers: "View offers",
        createOfferForm: {
          title: "Create program form",
          modalActions: {
            submit: "Create",
            cancel: "Cancel",
          },
        },
        deleteProgramForm: {
          title: "Remove program form",
          cannotRemove:
            "A program form that has program offers cannot be removed.",
          confirmation: (surveyTitle: string) => (
            <>
              Are you sure you want to remove the program form{" "}
              <strong>{surveyTitle}</strong>?
            </>
          ),
          modalActions: {
            submit: "Remove",
            cancel: "Cancel",
          },
        },
      },
    },

    ProgramOffer: {
      singleTitle: "Program offer",
      listTitle: "Program offers",

      attributes: {
        programs: {
          title: "Program items",
          message: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                The following program item has been created based on this
                program offer:
              </>
            ) : (
              <>
                The following program items have been created from this offer:
              </>
            ),
          acceptAgainWarning: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                The following program item has already been created based on
                this program offer. You are free to accept the offer again, in
                which case another program item will be created. (The link will
                open in a new tab.)
              </>
            ) : (
              <>
                The following program items have already been created based on
                this program offer. You are free to accept the offer again, in
                which case another program item will be created. (These links
                will open in a new tab.)
              </>
            ),
          dimensionsWillNotBeUpdatedOnProgramItem: (numPrograms: number) =>
            numPrograms === 1 ? (
              <>
                If you change the dimensions of this program offer, the changes
                will not be reflected in the program item created from this
                offer. You will need to edit the program item separately.
              </>
            ) : (
              <>
                If you change the dimensions of this program offer, the changes
                will not be reflected in the program items created from this
                offer. You will need to edit the program items separately.
              </>
            ),
        },
      },

      actions: {
        accept: {
          title: "Accept program offer",
          message: (
            <>
              To create a program item from this program offer, please review
              the following information about the program offer and select{" "}
              <em>Accept</em>. You can change this information later except for
              the slug.
            </>
          ),
          modalActions: {
            submit: "Accept",
            cancel: "Close without accepting",
          },
        },
      },
    },

    ProgramHost: {
      singleTitle: "Program host",
      listTitle: "Program hosts",
    },

    ScheduleItem: {
      singleTitle: "Schedule item",
      listTitle: "Schedule items",
      attributes: {
        startTime: "Start time",
      },
    },

    admin: {
      title: "Program admin",
    },
  },

  Dimension: {
    listTitle: "Dimensions",
  },

  Survey: {
    listTitle: "Surveys",
    singleTitle: "Survey",
    forEvent: (eventName: string) => <>for {eventName}</>,
    tableFooter: (count: number) => (
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
        helpText: (
          <>
            Machine-readable name of the survey. Must be unique within the
            event. Cannot be changed after creation. Can contain lower case
            letters, numbers and dashes (-). Will be part of the URL:{" "}
            <code>/event-slug/form-slug</code> (eg.{" "}
            <code>/tracon2025/offer-program</code>).
          </>
        ),
      },
      title: "Title",
      isActive: {
        title: "Receiving responses",
        untilFurtherNotice: "Open until further notice",
        untilTime: (formattedTime: String) => `Open until ${formattedTime}`,
        openingAt: (formattedTime: String) => `Opening at ${formattedTime}`,
        closed: "Closed",
        adminOverride: {
          title: "This survey is not active",
          message: (
            <>
              This survey is not currently open for responses. You can only see
              this page due to your administrative privileges. Users without
              admin privileges will only see a message that the survey is not
              active.
            </>
          ),
        },
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
        admin: {
          title: "Connecting responses to users",
          helpText:
            "NOTE: You cannot change this after the survey has been created!",
          choices: {
            HARD: "Hard anonymous",
            SOFT: "Soft anonymous",
            NAME_AND_EMAIL: "Name and email",
            FULL_PROFILE: "Full profile",
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
      protectResponses: {
        title: "Protect responses",
        helpText:
          "If checked, responses to this survey cannot be removed. Use this to protect responses from accidential removal.",
      },
      maxResponsesPerUser: {
        title: "Maximum number of responses per user",
        helpText:
          "The maximum number of responses a single user can submit to this survey. If set to 0, there is no limit. Note that this only applies to signed-in users. To enforce the limit, select Sign-in required as well.",
      },
      alsoAvailableInThisLanguage: (
        LanguageLink: ({ children }: { children: ReactNode }) => JSX.Element,
      ) => (
        <>
          This form is also available <LanguageLink>in English</LanguageLink>.
        </>
      ),
      cloneFrom: {
        title: "Clone from",
        helpText:
          "If selected, the new form will be created as a copy of an existing one. Dimensions and language versions along with their fields and texts will be copied, but responses will not.",
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
      toggleSubscription: "Notify for responses",
      submit: "Submit",
      deleteVisibleResponses: {
        title: "Delete responses",
        confirmation: (countResponses: number) => (
          <>
            Are you sure you want to remove the{" "}
            <strong>{countResponses}</strong> responses that are currently
            visible?
          </>
        ),
        responsesProtected:
          "The responses to this survey are protected. To remove, disable response protection from query settings first.",
        cannotDelete: "Cannot delete responses.",
        noResponsesToDelete: "No responses to delete.",
        modalActions: {
          submit: "Delete responses",
          cancel: "Cancel without deleting",
        },
      },
      deleteResponse: {
        title: "Delete response",
        confirmation: "Are you sure you want to delete this response?",
        cannotDelete: "This response cannot be deleted.",
        modalActions: {
          submit: "Delete response",
          cancel: "Cancel without deleting",
        },
      },
      exportDropdown: {
        dropdownHeader: "Export responses",
        excel: "Download as Excel",
        zip: "Download with attachments (zip)",
      },
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
      properties: "Properties",
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
          helpText: (
            <>
              Machine-readable, short name for the dimension. Cannot be changed
              after creation. Can contain lower case letters, numbers and dashes
              (-). Will become part of query string parameters in the URL:{" "}
              <code>dimension=value</code> (eg. <code>program-type=panel</code>
              ).
            </>
          ),
        },
        localizedTitleHeader: {
          title: "Localized titles",
          helpText:
            "The title of the dimension in different languages. The title need not be provided in all supported languages: if the title is missing in the selected language, it will fall back first to the default language and then to the technical name.",
        },
        behaviourFlagsHeader: {
          title: "Behaviour",
          helpText:
            "These settings change the way this dimension functions in various UI views. In most cases, you can leave these to their default values.",
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
        isPublic: {
          title: "Public",
          helpText:
            "If checked, values of this dimension may be shown to non-admin users",
        },
        isListFilter: {
          title: "List filter",
          helpText:
            "If checked, this dimension will be presented as a drop-down filter in list views.",
        },
        isShownInDetail: {
          title: "Shown in detail views",
          helpText:
            "If checked, values of this dimension will be shown in single-item detail views.",
        },
        isNegativeSelection: {
          title: "Negative selection",
          helpText:
            "If checked, suggests to UI that when filtering, by default all items of this dimension should be selected and the user will likely make selections by un-checking ones they do not want. Only makes sense with multi-value dimensions.",
        },
        valueOrdering: {
          title: "Value ordering",
          helpText: "In which order will the values be presented?",
          choices: {
            MANUAL: "Manual (drag to order)",
            TITLE: "Title (localized)",
            SLUG: "Technical name",
          },
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
          helpText: (
            <>
              Machine-readable, short name for the dimension value. Cannot be
              changed after creation. Can contain lower case letters, numbers
              and dashes (-). Will become part of query string parameters in the
              URL: <code>dimension=value</code> (eg.{" "}
              <code>program-type=panel</code>).
            </>
          ),
        },
        color: {
          title: "Color",
          helpText:
            "Color of the value in the response list. Use bright colors: they will be lightened or darkened as needed.",
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
