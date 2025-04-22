/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /**
   * The `DateTime` scalar type represents a DateTime
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  DateTime: { input: string; output: string; }
  /** The `Decimal` scalar type represents a python Decimal. */
  Decimal: { input: any; output: any; }
  /**
   * The `GenericScalar` scalar type represents a generic
   * GraphQL scalar value that could be:
   * String, Boolean, Int, Float, List or Object.
   */
  GenericScalar: { input: unknown; output: unknown; }
  /**
   * Allows use of a JSON String for input / output from the GraphQL schema.
   *
   * Use of this type is *not recommended* as you lose the benefits of having a defined, static
   * schema (one of the key benefits of GraphQL).
   */
  JSONString: { input: string; output: string; }
  /**
   * Leverages the internal Python implementation of UUID (uuid.UUID) to provide native UUID objects
   * in fields, resolvers and input.
   */
  UUID: { input: string; output: string; }
};

export type AcceptProgramOffer = {
  __typename?: 'AcceptProgramOffer';
  program: FullProgramType;
};

export type AcceptProgramOfferInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  responseId: Scalars['UUID']['input'];
};

/** An enumeration. */
export enum AnnotationDataType {
  Boolean = 'BOOLEAN',
  Number = 'NUMBER',
  String = 'STRING'
}

export type AnnotationSchemoidType = {
  __typename?: 'AnnotationSchemoidType';
  description: Scalars['String']['output'];
  isPublic: Scalars['Boolean']['output'];
  isShownInDetail: Scalars['Boolean']['output'];
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  type: AnnotationDataType;
};


export type AnnotationSchemoidTypeDescriptionArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type AnnotationSchemoidTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

/** An enumeration. */
export enum Anonymity {
  Hard = 'HARD',
  NameAndEmail = 'NAME_AND_EMAIL',
  Soft = 'SOFT'
}

export type CancelAndRefundOrder = {
  __typename?: 'CancelAndRefundOrder';
  order?: Maybe<LimitedOrderType>;
};

export type CancelAndRefundOrderInput = {
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
  refundType: RefundType;
};

/** An enumeration. */
export enum CodeStatus {
  BeyondLogic = 'BEYOND_LOGIC',
  ManualInterventionRequired = 'MANUAL_INTERVENTION_REQUIRED',
  Unused = 'UNUSED',
  Used = 'USED'
}

export type ConfirmEmail = {
  __typename?: 'ConfirmEmail';
  user?: Maybe<LimitedUserType>;
};

export type ConfirmEmailInput = {
  locale: Scalars['String']['input'];
};

export type CreateProduct = {
  __typename?: 'CreateProduct';
  product?: Maybe<LimitedProductType>;
};

export type CreateProductInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
};

export type CreateProgramFeedback = {
  __typename?: 'CreateProgramFeedback';
  success: Scalars['Boolean']['output'];
};

export type CreateProgramForm = {
  __typename?: 'CreateProgramForm';
  survey?: Maybe<FullSurveyType>;
};

export type CreateProgramFormInput = {
  copyFrom?: InputMaybe<Scalars['String']['input']>;
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type CreateQuota = {
  __typename?: 'CreateQuota';
  quota?: Maybe<LimitedQuotaType>;
};

export type CreateQuotaInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
};

export type CreateSurvey = {
  __typename?: 'CreateSurvey';
  survey?: Maybe<FullSurveyType>;
};

export type CreateSurveyInput = {
  anonymity: Anonymity;
  copyFrom?: InputMaybe<Scalars['String']['input']>;
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type CreateSurveyLanguage = {
  __typename?: 'CreateSurveyLanguage';
  form?: Maybe<FormType>;
};

export type CreateSurveyLanguageInput = {
  copyFrom?: InputMaybe<Scalars['String']['input']>;
  eventSlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type CreateSurveyResponse = {
  __typename?: 'CreateSurveyResponse';
  response?: Maybe<ProfileResponseType>;
};

export type CreateSurveyResponseInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  surveySlug: Scalars['String']['input'];
};

export type DeleteDimension = {
  __typename?: 'DeleteDimension';
  slug?: Maybe<Scalars['String']['output']>;
};

export type DeleteDimensionInput = {
  dimensionSlug: Scalars['String']['input'];
  scopeSlug: Scalars['String']['input'];
  universeSlug: Scalars['String']['input'];
};

export type DeleteDimensionValue = {
  __typename?: 'DeleteDimensionValue';
  slug?: Maybe<Scalars['String']['output']>;
};

export type DeleteDimensionValueInput = {
  dimensionSlug: Scalars['String']['input'];
  scopeSlug: Scalars['String']['input'];
  universeSlug: Scalars['String']['input'];
  valueSlug: Scalars['String']['input'];
};

export type DeleteProduct = {
  __typename?: 'DeleteProduct';
  id: Scalars['String']['output'];
};

export type DeleteProductInput = {
  eventSlug: Scalars['String']['input'];
  productId: Scalars['String']['input'];
};

export type DeleteQuota = {
  __typename?: 'DeleteQuota';
  id: Scalars['String']['output'];
};

export type DeleteQuotaInput = {
  eventSlug: Scalars['String']['input'];
  quotaId: Scalars['String']['input'];
};

export type DeleteSurvey = {
  __typename?: 'DeleteSurvey';
  slug?: Maybe<Scalars['String']['output']>;
};

export type DeleteSurveyInput = {
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type DeleteSurveyLanguage = {
  __typename?: 'DeleteSurveyLanguage';
  language?: Maybe<Scalars['String']['output']>;
};

export type DeleteSurveyLanguageInput = {
  eventSlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type DeleteSurveyResponses = {
  __typename?: 'DeleteSurveyResponses';
  countDeleted: Scalars['Int']['output'];
};

export type DeleteSurveyResponsesInput = {
  eventSlug: Scalars['String']['input'];
  responseIds?: InputMaybe<Array<InputMaybe<Scalars['String']['input']>>>;
  surveySlug: Scalars['String']['input'];
};

/**
 * Used to construct dimension filters in GraphQL queries.
 * When a list of these is present, the semantics are AND.
 * For each element in the list, with respect to the values list, the semantics are OR.
 * The absence of the values list, or the special value "*" in the values list, means that the dimension must exist.
 */
export type DimensionFilterInput = {
  dimension: Scalars['String']['input'];
  values?: InputMaybe<Array<Scalars['String']['input']>>;
};

export type DimensionValueType = {
  __typename?: 'DimensionValueType';
  canRemove: Scalars['Boolean']['output'];
  color: Scalars['String']['output'];
  /** Initial values are set on new atoms automatically. */
  isInitial: Scalars['Boolean']['output'];
  /** Technical values cannot be edited in the UI. They are used for internal purposes and have some assumptions about them. */
  isTechnical: Scalars['Boolean']['output'];
  slug: Scalars['String']['output'];
  title?: Maybe<Scalars['String']['output']>;
  titleEn: Scalars['String']['output'];
  titleFi: Scalars['String']['output'];
  titleSv: Scalars['String']['output'];
};


export type DimensionValueTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

/** An enumeration. */
export enum DimensionsDimensionValueOrderingChoices {
  /** Manual */
  Manual = 'MANUAL',
  /** Alphabetical (slug) */
  Slug = 'SLUG',
  /** Alphabetical (localized title) */
  Title = 'TITLE'
}

export type FavoriteInput = {
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
};

export type FavoriteScheduleItemInput = {
  eventSlug: Scalars['String']['input'];
  scheduleItemSlug: Scalars['String']['input'];
};

export type FormType = {
  __typename?: 'FormType';
  /** A form can be removed if it has no responses. */
  canRemove: Scalars['Boolean']['output'];
  description: Scalars['String']['output'];
  event: LimitedEventType;
  fields?: Maybe<Scalars['GenericScalar']['output']>;
  language: FormsFormLanguageChoices;
  survey?: Maybe<LimitedSurveyType>;
  thankYouMessage: Scalars['String']['output'];
  title: Scalars['String']['output'];
};


export type FormTypeFieldsArgs = {
  enrich?: InputMaybe<Scalars['Boolean']['input']>;
};

export type FormsEventMetaType = {
  __typename?: 'FormsEventMetaType';
  survey?: Maybe<FullSurveyType>;
  surveys?: Maybe<Array<FullSurveyType>>;
};


export type FormsEventMetaTypeSurveyArgs = {
  app?: InputMaybe<SurveyApp>;
  slug: Scalars['String']['input'];
};


export type FormsEventMetaTypeSurveysArgs = {
  app: SurveyApp;
  includeInactive?: InputMaybe<Scalars['Boolean']['input']>;
};

/** An enumeration. */
export enum FormsFormLanguageChoices {
  /** English */
  En = 'EN',
  /** Finnish */
  Fi = 'FI',
  /** Swedish */
  Sv = 'SV'
}

export type FormsProfileMetaType = {
  __typename?: 'FormsProfileMetaType';
  /** Returns a single response submitted by the current user. */
  response?: Maybe<ProfileResponseType>;
  /** Returns all responses submitted by the current user. */
  responses: Array<ProfileResponseType>;
  /** Returns all surveys accessible by the current user. To limit to surveys subscribed to, specify `relation: SUBSCRIBED`. To limit by event, specify `eventSlug: $eventSlug`. */
  surveys: Array<FullSurveyType>;
};


export type FormsProfileMetaTypeResponseArgs = {
  id: Scalars['String']['input'];
};


export type FormsProfileMetaTypeSurveysArgs = {
  eventSlug?: InputMaybe<Scalars['String']['input']>;
  relation?: InputMaybe<SurveyRelation>;
};

export type FullDimensionType = {
  __typename?: 'FullDimensionType';
  canRemove: Scalars['Boolean']['output'];
  /** Key dimensions are shown lists of atoms. */
  isKeyDimension: Scalars['Boolean']['output'];
  /** Suggests to UI that this dimension should be shown as a list filter. */
  isListFilter: Scalars['Boolean']['output'];
  /** Multi-value dimensions allow multiple values to be selected. NOTE: In the database, all dimensions are multi-value, so this is just a UI hint. */
  isMultiValue: Scalars['Boolean']['output'];
  /** Suggests to UI that when this dimension is not being filtered on, all values should be selected. Intended for use cases when the user is expected to rather exclude certain values than only include some. One such use case is accessibility and content warnings. NOTE: Does not make sense without `is_multi_value`. */
  isNegativeSelection: Scalars['Boolean']['output'];
  /** Public dimensions are returned to non-admin users. */
  isPublic: Scalars['Boolean']['output'];
  /** Suggests to UI that this dimension should be shown in detail view. */
  isShownInDetail: Scalars['Boolean']['output'];
  isShownToSubject: Scalars['Boolean']['output'];
  /** Technical dimensions are not editable in the UI. They are used for internal purposes have some assumptions about them (eg. their existence and that of certain values). */
  isTechnical: Scalars['Boolean']['output'];
  slug: Scalars['String']['output'];
  title?: Maybe<Scalars['String']['output']>;
  titleEn: Scalars['String']['output'];
  titleFi: Scalars['String']['output'];
  titleSv: Scalars['String']['output'];
  /** In which order are the values of this dimension returned in the GraphQL API. NOTE: When using Alphabetical (localized title), the language needs to be provided to `values` and `values.title` fields separately. */
  valueOrdering: DimensionsDimensionValueOrderingChoices;
  values: Array<DimensionValueType>;
};


export type FullDimensionTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type FullDimensionTypeValuesArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type FullEventType = {
  __typename?: 'FullEventType';
  endTime?: Maybe<Scalars['DateTime']['output']>;
  forms?: Maybe<FormsEventMetaType>;
  name: Scalars['String']['output'];
  program?: Maybe<ProgramV2EventMetaType>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  startTime?: Maybe<Scalars['DateTime']['output']>;
  tickets?: Maybe<TicketsV2EventMetaType>;
  timezone: Scalars['String']['output'];
  timezoneName: Scalars['String']['output'];
};

export type FullOrderType = {
  __typename?: 'FullOrderType';
  canPay: Scalars['Boolean']['output'];
  /** Returns whether the order can be refunded. */
  canRefund: Scalars['Boolean']['output'];
  /** Electronic ticket codes related to this order. */
  codes: Array<LimitedCodeType>;
  createdAt: Scalars['DateTime']['output'];
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  /** Returns a link at which the admin can view their electronic tickets. Returns null if the order does not contain electronic tickets. */
  eticketsLink?: Maybe<Scalars['String']['output']>;
  event: LimitedEventType;
  firstName: Scalars['String']['output'];
  formattedOrderNumber: Scalars['String']['output'];
  id: Scalars['UUID']['output'];
  language: TicketsV2OrderLanguageChoices;
  lastName: Scalars['String']['output'];
  /** Order number used in contexts where UUID cannot be used. Such places include generating reference numbers and the customer reading the order number aloud to an event rep. Prefer id (UUID) for everything else (eg. URLs). */
  orderNumber: Scalars['Int']['output'];
  /** Payment stamps related to this order. */
  paymentStamps: Array<LimitedPaymentStampType>;
  phone: Scalars['String']['output'];
  /** Contents of the order (product x quantity). */
  products: Array<OrderProductType>;
  /** Receipts related to this order. */
  receipts: Array<LimitedReceiptType>;
  status: PaymentStatus;
  totalPrice: Scalars['Decimal']['output'];
};

export type FullProductType = {
  __typename?: 'FullProductType';
  availableFrom?: Maybe<Scalars['DateTime']['output']>;
  availableUntil?: Maybe<Scalars['DateTime']['output']>;
  /** Returns true if the product can be deleted. A product can be deleted if it has not been sold at all. */
  canDelete: Scalars['Boolean']['output'];
  /** Computes the amount of available units of this product. Other versions of this product are grouped together. Null if the product has no quotas. */
  countAvailable?: Maybe<Scalars['Int']['output']>;
  /** Computes the amount of paid units of this product. Other versions of this product are grouped together. */
  countPaid: Scalars['Int']['output'];
  /** Computes the amount of reserved units of this product. Other versions of this product are grouped together. */
  countReserved: Scalars['Int']['output'];
  createdAt: Scalars['DateTime']['output'];
  description: Scalars['String']['output'];
  eticketsPerProduct: Scalars['Int']['output'];
  id: Scalars['ID']['output'];
  /** Returns true if the product can currently be sold; that is, if it has not been superseded and it is within its availability window. This does not take into account if the product has been sold out; for that, consult `count_available`. */
  isAvailable: Scalars['Boolean']['output'];
  maxPerOrder: Scalars['Int']['output'];
  /** Old versions of this product. */
  oldVersions: Array<LimitedProductType>;
  price: Scalars['Decimal']['output'];
  quotas: Array<LimitedQuotaType>;
  /** The product superseding this product, if any. */
  supersededBy?: Maybe<LimitedProductType>;
  title: Scalars['String']['output'];
};

export type FullProgramType = {
  __typename?: 'FullProgramType';
  /** Program annotation values with schema attached to them. Only public annotations are returned. NOTE: If querying a lot of program items, consider using cachedAnnotations instead for SPEED. */
  annotations: Array<ProgramAnnotationType>;
  /** A mapping of program annotation slug to annotation value. Only public annotations are returned. */
  cachedAnnotations: Scalars['GenericScalar']['output'];
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** The earliest start time of any schedule item of this program. NOTE: This is not the same as the program's start time. The intended purpose of this field is to exclude programs that have not yet started. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedEarliestStartTime?: Maybe<Scalars['DateTime']['output']>;
  cachedHosts: Scalars['String']['output'];
  /** The latest end time of any schedule item of this program. NOTE: This is not the same as the program's start end. The intended purpose of this field is to exclude programs that have already ended. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedLatestEndTime?: Maybe<Scalars['DateTime']['output']>;
  color: Scalars['String']['output'];
  createdAt: Scalars['DateTime']['output'];
  description: Scalars['String']['output'];
  /** `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  dimensions: Array<ProgramDimensionValueType>;
  isAcceptingFeedback: Scalars['Boolean']['output'];
  /** Get the links associated with the program. If types are not specified, all links are returned. */
  links: Array<ProgramLink>;
  /** Supplied for convenience. Prefer scheduleItem.location if possible. Caveat: When a program item has multiple schedule items, they may be in different locations. In such cases, a comma separated list of locations is returned. */
  location?: Maybe<Scalars['String']['output']>;
  programOffer?: Maybe<LimitedResponseType>;
  scheduleItems: Array<LimitedScheduleItemType>;
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type FullProgramTypeAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullProgramTypeCachedAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullProgramTypeDimensionsArgs = {
  isListFilter?: InputMaybe<Scalars['Boolean']['input']>;
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullProgramTypeLinksArgs = {
  includeExpired?: InputMaybe<Scalars['Boolean']['input']>;
  lang?: InputMaybe<Scalars['String']['input']>;
  types?: InputMaybe<Array<InputMaybe<ProgramLinkType>>>;
};


export type FullProgramTypeLocationArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type FullQuotaType = {
  __typename?: 'FullQuotaType';
  /** Returns true if the product can be deleted. A product can be deleted if it has not been sold at all. */
  canDelete: Scalars['Boolean']['output'];
  countAvailable: Scalars['Int']['output'];
  countPaid: Scalars['Int']['output'];
  countReserved: Scalars['Int']['output'];
  countTotal: Scalars['Int']['output'];
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
  products: Array<LimitedProductType>;
};

export type FullResponseType = {
  __typename?: 'FullResponseType';
  /** Returns the dimensions of the response as a dict of dimension slug -> list of dimension value slugs. If the response is not related to a survey, there will be no dimensions and an empty dict will always be returned. Using this field is more efficient than querying the dimensions field on the response, as the dimensions are cached on the response object. */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who submitted the response. If response is to an anonymous survey,
   * this information will not be available.
   *
   */
  createdBy?: Maybe<LimitedUserType>;
  dimensions: Array<ResponseDimensionValueType>;
  form: FormType;
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
  /** Language code of the form used to submit this response. */
  language: Scalars['String']['output'];
  /** If this response is a program offer, this field returns the program items created from this program offer. If this response is not to a program offer form, this will always be empty. */
  programs: Array<LimitedProgramType>;
  /** Sequence number of this response within the use case (eg. survey). */
  sequenceNumber: Scalars['Int']['output'];
  values?: Maybe<Scalars['GenericScalar']['output']>;
};


export type FullResponseTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullResponseTypeValuesArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};

export type FullScheduleItemType = {
  __typename?: 'FullScheduleItemType';
  createdAt: Scalars['DateTime']['output'];
  endTime: Scalars['DateTime']['output'];
  endTimeUnixSeconds: Scalars['Int']['output'];
  lengthMinutes: Scalars['Int']['output'];
  location?: Maybe<Scalars['String']['output']>;
  program: LimitedProgramType;
  /** NOTE: Slug must be unique within Event. It does not suffice to be unique within Program. */
  slug: Scalars['String']['output'];
  startTime: Scalars['DateTime']['output'];
  startTimeUnixSeconds: Scalars['Int']['output'];
  subtitle: Scalars['String']['output'];
  /** Returns the title of the program, with subtitle if it exists, in the format "Program title – Schedule item subtitle". */
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type FullScheduleItemTypeLocationArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type FullSurveyType = {
  __typename?: 'FullSurveyType';
  /** The form will be available from this date onwards. If not set, the form will not be available. */
  activeFrom?: Maybe<Scalars['DateTime']['output']>;
  /** The form will be available until this date. If not set, the form will be available indefinitely provided that active_from is set and has passed. */
  activeUntil?: Maybe<Scalars['DateTime']['output']>;
  anonymity: Anonymity;
  /** Surveys that have language versions cannot be removed. Having language versions is also a prerequisite for a survey to have responses. */
  canRemove: Scalars['Boolean']['output'];
  /** Checks that the user has permission to remove responses to this survey. This requires proper CBAC permission and that `survey.protect_responses` is false. */
  canRemoveResponses: Scalars['Boolean']['output'];
  /** Returns the number of responses to this survey regardless of language version used. Authorization required. */
  countResponses: Scalars['Int']['output'];
  /** Returns the number of responses to this survey by the current user. */
  countResponsesByCurrentUser: Scalars['Int']['output'];
  dimensions?: Maybe<Array<FullDimensionType>>;
  event: LimitedEventType;
  /** A survey's language versions may have differing fields. This field presents them combined as a single list of fields. If a language is specified, that language is used as the base for the combined fields. Order of fields not present in the base language is not guaranteed. */
  fields?: Maybe<Scalars['GenericScalar']['output']>;
  /** Will attempt to give the form in the requested language, falling back to another language if that language is not available. */
  form?: Maybe<FormType>;
  isActive: Scalars['Boolean']['output'];
  /** Key fields will be shown in the response list. */
  keyFields: Array<Scalars['String']['output']>;
  languages: Array<FormType>;
  loginRequired: Scalars['Boolean']['output'];
  /** Maximum number of responses per user. 0 = unlimited. Note that if login_required is not set, this only takes effect for logged in users.Has no effect if the survey is hard anonymous. */
  maxResponsesPerUser: Scalars['Int']['output'];
  /** If enabled, responses cannot be deleted from the UI without disabling this first. */
  protectResponses: Scalars['Boolean']['output'];
  response?: Maybe<FullResponseType>;
  /** Returns the responses to this survey regardless of language version used. Authorization required. */
  responses?: Maybe<Array<LimitedResponseType>>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  /** Returns a summary of responses to this survey. If a language is specified, that language is used as the base for the combined fields. Order of fields not present in the base language is not guaranteed. Authorization required. */
  summary?: Maybe<Scalars['GenericScalar']['output']>;
  title?: Maybe<Scalars['String']['output']>;
};


export type FullSurveyTypeCountResponsesArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
};


export type FullSurveyTypeDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullSurveyTypeFieldsArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type FullSurveyTypeFormArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type FullSurveyTypeResponseArgs = {
  id: Scalars['String']['input'];
};


export type FullSurveyTypeResponsesArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
};


export type FullSurveyTypeSummaryArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type FullSurveyTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type GenerateKeyPair = {
  __typename?: 'GenerateKeyPair';
  id: Scalars['String']['output'];
};

export type InitFileUploadInput = {
  fileType: Scalars['String']['input'];
  filename: Scalars['String']['input'];
};

export type InitFileUploadResponse = {
  __typename?: 'InitFileUploadResponse';
  fileUrl?: Maybe<Scalars['String']['output']>;
  uploadUrl?: Maybe<Scalars['String']['output']>;
};

export type KeyPairType = {
  __typename?: 'KeyPairType';
  createdAt: Scalars['DateTime']['output'];
  id: Scalars['UUID']['output'];
  publicKey: Scalars['JSONString']['output'];
};

export type LimitedCodeType = {
  __typename?: 'LimitedCodeType';
  code: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  literateCode: Scalars['String']['output'];
  productText: Scalars['String']['output'];
  /** Status of the code. Kompassi uses the MIR state to indicate cancelled orders or otherwise revoked codes. */
  status: CodeStatus;
  usedOn?: Maybe<Scalars['DateTime']['output']>;
};

export type LimitedEventType = {
  __typename?: 'LimitedEventType';
  name: Scalars['String']['output'];
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
};

export type LimitedOrderType = {
  __typename?: 'LimitedOrderType';
  canPay: Scalars['Boolean']['output'];
  createdAt: Scalars['DateTime']['output'];
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  formattedOrderNumber: Scalars['String']['output'];
  id: Scalars['UUID']['output'];
  language: TicketsV2OrderLanguageChoices;
  lastName: Scalars['String']['output'];
  /** Order number used in contexts where UUID cannot be used. Such places include generating reference numbers and the customer reading the order number aloud to an event rep. Prefer id (UUID) for everything else (eg. URLs). */
  orderNumber: Scalars['Int']['output'];
  phone: Scalars['String']['output'];
  status: PaymentStatus;
  totalPrice: Scalars['Decimal']['output'];
};

export type LimitedPaymentStampType = {
  __typename?: 'LimitedPaymentStampType';
  /** The correlation ID ties together the payment stamps related to the same payment attempt. For Paytrail, this is what they call 'stamp'. */
  correlationId: Scalars['UUID']['output'];
  createdAt: Scalars['DateTime']['output'];
  data: Scalars['GenericScalar']['output'];
  id: Scalars['UUID']['output'];
  provider: PaymentProvider;
  status: PaymentStatus;
  type: PaymentStampType;
};

export type LimitedProductType = {
  __typename?: 'LimitedProductType';
  availableFrom?: Maybe<Scalars['DateTime']['output']>;
  availableUntil?: Maybe<Scalars['DateTime']['output']>;
  /** Returns true if the product can be deleted. A product can be deleted if it has not been sold at all. */
  canDelete: Scalars['Boolean']['output'];
  /** Computes the amount of available units of this product. Other versions of this product are grouped together. Null if the product has no quotas. */
  countAvailable?: Maybe<Scalars['Int']['output']>;
  /** Computes the amount of paid units of this product. Other versions of this product are grouped together. */
  countPaid: Scalars['Int']['output'];
  /** Computes the amount of reserved units of this product. Other versions of this product are grouped together. */
  countReserved: Scalars['Int']['output'];
  createdAt: Scalars['DateTime']['output'];
  description: Scalars['String']['output'];
  eticketsPerProduct: Scalars['Int']['output'];
  id: Scalars['ID']['output'];
  maxPerOrder: Scalars['Int']['output'];
  price: Scalars['Decimal']['output'];
  title: Scalars['String']['output'];
};

/**
 * "Limited" program items are returned when queried through ScheduleItem.program so as to
 * limit DoS via deep nesting. It lacks access to `scheduleItems` which might be used to
 * cause a rapid expansion of the response via deep nesting, and also lacks access to
 * some fields that may be expensive to compute such as `dimensions`; however,
 * `cachedDimensions` is still provided.
 */
export type LimitedProgramType = {
  __typename?: 'LimitedProgramType';
  /** A mapping of program annotation slug to annotation value. Only public annotations are returned. */
  cachedAnnotations: Scalars['GenericScalar']['output'];
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** The earliest start time of any schedule item of this program. NOTE: This is not the same as the program's start time. The intended purpose of this field is to exclude programs that have not yet started. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedEarliestStartTime?: Maybe<Scalars['DateTime']['output']>;
  cachedHosts: Scalars['String']['output'];
  /** The latest end time of any schedule item of this program. NOTE: This is not the same as the program's start end. The intended purpose of this field is to exclude programs that have already ended. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedLatestEndTime?: Maybe<Scalars['DateTime']['output']>;
  color: Scalars['String']['output'];
  createdAt: Scalars['DateTime']['output'];
  description: Scalars['String']['output'];
  isAcceptingFeedback: Scalars['Boolean']['output'];
  /** Get the links associated with the program. If types are not specified, all links are returned. */
  links: Array<ProgramLink>;
  /** Supplied for convenience. Prefer scheduleItem.location if possible. Caveat: When a program item has multiple schedule items, they may be in different locations. In such cases, a comma separated list of locations is returned. */
  location?: Maybe<Scalars['String']['output']>;
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


/**
 * "Limited" program items are returned when queried through ScheduleItem.program so as to
 * limit DoS via deep nesting. It lacks access to `scheduleItems` which might be used to
 * cause a rapid expansion of the response via deep nesting, and also lacks access to
 * some fields that may be expensive to compute such as `dimensions`; however,
 * `cachedDimensions` is still provided.
 */
export type LimitedProgramTypeCachedAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
};


/**
 * "Limited" program items are returned when queried through ScheduleItem.program so as to
 * limit DoS via deep nesting. It lacks access to `scheduleItems` which might be used to
 * cause a rapid expansion of the response via deep nesting, and also lacks access to
 * some fields that may be expensive to compute such as `dimensions`; however,
 * `cachedDimensions` is still provided.
 */
export type LimitedProgramTypeLinksArgs = {
  includeExpired?: InputMaybe<Scalars['Boolean']['input']>;
  lang?: InputMaybe<Scalars['String']['input']>;
  types?: InputMaybe<Array<InputMaybe<ProgramLinkType>>>;
};


/**
 * "Limited" program items are returned when queried through ScheduleItem.program so as to
 * limit DoS via deep nesting. It lacks access to `scheduleItems` which might be used to
 * cause a rapid expansion of the response via deep nesting, and also lacks access to
 * some fields that may be expensive to compute such as `dimensions`; however,
 * `cachedDimensions` is still provided.
 */
export type LimitedProgramTypeLocationArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type LimitedQuotaType = {
  __typename?: 'LimitedQuotaType';
  /** Returns true if the product can be deleted. A product can be deleted if it has not been sold at all. */
  canDelete: Scalars['Boolean']['output'];
  countAvailable: Scalars['Int']['output'];
  countPaid: Scalars['Int']['output'];
  countReserved: Scalars['Int']['output'];
  countTotal: Scalars['Int']['output'];
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
};

export type LimitedReceiptType = {
  __typename?: 'LimitedReceiptType';
  /** The correlation ID ties together the receipt stamps related to the same receipt attempt. Usually you would use the correlation ID of the payment stamp that you used to determine this order is paid. */
  correlationId: Scalars['UUID']['output'];
  createdAt: Scalars['DateTime']['output'];
  /** The email address to which the receipt was sent. */
  email: Scalars['String']['output'];
  status: ReceiptStatus;
  type: ReceiptType;
};

export type LimitedResponseType = {
  __typename?: 'LimitedResponseType';
  /** Returns the dimensions of the response as a dict of dimension slug -> list of dimension value slugs. If the response is not related to a survey, there will be no dimensions and an empty dict will always be returned. Using this field is more efficient than querying the dimensions field on the response, as the dimensions are cached on the response object. */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who submitted the response. If response is to an anonymous survey,
   * this information will not be available.
   *
   */
  createdBy?: Maybe<LimitedUserType>;
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
  /** Language code of the form used to submit this response. */
  language: Scalars['String']['output'];
  /** Sequence number of this response within the use case (eg. survey). */
  sequenceNumber: Scalars['Int']['output'];
  values?: Maybe<Scalars['GenericScalar']['output']>;
};


export type LimitedResponseTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type LimitedResponseTypeValuesArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};

export type LimitedScheduleItemType = {
  __typename?: 'LimitedScheduleItemType';
  createdAt: Scalars['DateTime']['output'];
  endTime: Scalars['DateTime']['output'];
  endTimeUnixSeconds: Scalars['Int']['output'];
  lengthMinutes: Scalars['Int']['output'];
  location?: Maybe<Scalars['String']['output']>;
  /** NOTE: Slug must be unique within Event. It does not suffice to be unique within Program. */
  slug: Scalars['String']['output'];
  startTime: Scalars['DateTime']['output'];
  startTimeUnixSeconds: Scalars['Int']['output'];
  subtitle: Scalars['String']['output'];
  /** Returns the title of the program, with subtitle if it exists, in the format "Program title – Schedule item subtitle". */
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type LimitedScheduleItemTypeLocationArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type LimitedSurveyType = {
  __typename?: 'LimitedSurveyType';
  /** The form will be available from this date onwards. If not set, the form will not be available. */
  activeFrom?: Maybe<Scalars['DateTime']['output']>;
  /** The form will be available until this date. If not set, the form will be available indefinitely provided that active_from is set and has passed. */
  activeUntil?: Maybe<Scalars['DateTime']['output']>;
  anonymity: Anonymity;
  isActive: Scalars['Boolean']['output'];
  loginRequired: Scalars['Boolean']['output'];
  /** Maximum number of responses per user. 0 = unlimited. Note that if login_required is not set, this only takes effect for logged in users.Has no effect if the survey is hard anonymous. */
  maxResponsesPerUser: Scalars['Int']['output'];
  /** If enabled, responses cannot be deleted from the UI without disabling this first. */
  protectResponses: Scalars['Boolean']['output'];
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  title?: Maybe<Scalars['String']['output']>;
};


export type LimitedSurveyTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type LimitedUserType = {
  __typename?: 'LimitedUserType';
  /** User's full name. */
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  lastName: Scalars['String']['output'];
};

/** Deprecated. Use MarkScheduleItemAsFavorite instead. */
export type MarkProgramAsFavorite = {
  __typename?: 'MarkProgramAsFavorite';
  success: Scalars['Boolean']['output'];
};

export type MarkScheduleItemAsFavorite = {
  __typename?: 'MarkScheduleItemAsFavorite';
  success: Scalars['Boolean']['output'];
};

export type Mutation = {
  __typename?: 'Mutation';
  acceptProgramOffer?: Maybe<AcceptProgramOffer>;
  cancelAndRefundOrder?: Maybe<CancelAndRefundOrder>;
  confirmEmail?: Maybe<ConfirmEmail>;
  createProduct?: Maybe<CreateProduct>;
  createProgramFeedback?: Maybe<CreateProgramFeedback>;
  createProgramForm?: Maybe<CreateProgramForm>;
  createQuota?: Maybe<CreateQuota>;
  createSurvey?: Maybe<CreateSurvey>;
  createSurveyLanguage?: Maybe<CreateSurveyLanguage>;
  createSurveyResponse?: Maybe<CreateSurveyResponse>;
  deleteDimension?: Maybe<DeleteDimension>;
  deleteDimensionValue?: Maybe<DeleteDimensionValue>;
  deleteProduct?: Maybe<DeleteProduct>;
  deleteQuota?: Maybe<DeleteQuota>;
  deleteSurvey?: Maybe<DeleteSurvey>;
  deleteSurveyLanguage?: Maybe<DeleteSurveyLanguage>;
  deleteSurveyResponses?: Maybe<DeleteSurveyResponses>;
  generateKeyPair?: Maybe<GenerateKeyPair>;
  initFileUpload?: Maybe<InitFileUploadResponse>;
  /** Deprecated. Use MarkScheduleItemAsFavorite instead. */
  markProgramAsFavorite?: Maybe<MarkProgramAsFavorite>;
  markScheduleItemAsFavorite?: Maybe<MarkScheduleItemAsFavorite>;
  putDimension?: Maybe<PutDimension>;
  putDimensionValue?: Maybe<PutDimensionValue>;
  reorderProducts?: Maybe<ReorderProducts>;
  resendOrderConfirmation?: Maybe<ResendOrderConfirmation>;
  revokeKeyPair?: Maybe<RevokeKeyPair>;
  subscribeToSurveyResponses?: Maybe<SubscribeToSurveyResponses>;
  /** Deprecated. Use UnmarkScheduleItemAsFavorite instead. */
  unmarkProgramAsFavorite?: Maybe<UnmarkProgramAsFavorite>;
  unmarkScheduleItemAsFavorite?: Maybe<UnmarkScheduleItemAsFavorite>;
  unsubscribeFromSurveyResponses?: Maybe<UnsubscribeFromSurveyResponses>;
  updateForm?: Maybe<UpdateForm>;
  updateFormFields?: Maybe<UpdateFormFields>;
  updateOrder?: Maybe<UpdateOrder>;
  updateProduct?: Maybe<UpdateProduct>;
  updateProgram?: Maybe<UpdateProgram>;
  updateProgramForm?: Maybe<UpdateProgramForm>;
  updateQuota?: Maybe<UpdateQuota>;
  updateResponseDimensions?: Maybe<UpdateResponseDimensions>;
  updateSurvey?: Maybe<UpdateSurvey>;
};


export type MutationAcceptProgramOfferArgs = {
  input: AcceptProgramOfferInput;
};


export type MutationCancelAndRefundOrderArgs = {
  input: CancelAndRefundOrderInput;
};


export type MutationConfirmEmailArgs = {
  input: ConfirmEmailInput;
};


export type MutationCreateProductArgs = {
  input: CreateProductInput;
};


export type MutationCreateProgramFeedbackArgs = {
  input: ProgramFeedbackInput;
};


export type MutationCreateProgramFormArgs = {
  input: CreateProgramFormInput;
};


export type MutationCreateQuotaArgs = {
  input: CreateQuotaInput;
};


export type MutationCreateSurveyArgs = {
  input: CreateSurveyInput;
};


export type MutationCreateSurveyLanguageArgs = {
  input: CreateSurveyLanguageInput;
};


export type MutationCreateSurveyResponseArgs = {
  input: CreateSurveyResponseInput;
};


export type MutationDeleteDimensionArgs = {
  input: DeleteDimensionInput;
};


export type MutationDeleteDimensionValueArgs = {
  input: DeleteDimensionValueInput;
};


export type MutationDeleteProductArgs = {
  input: DeleteProductInput;
};


export type MutationDeleteQuotaArgs = {
  input: DeleteQuotaInput;
};


export type MutationDeleteSurveyArgs = {
  input: DeleteSurveyInput;
};


export type MutationDeleteSurveyLanguageArgs = {
  input: DeleteSurveyLanguageInput;
};


export type MutationDeleteSurveyResponsesArgs = {
  input: DeleteSurveyResponsesInput;
};


export type MutationGenerateKeyPairArgs = {
  password: Scalars['String']['input'];
};


export type MutationInitFileUploadArgs = {
  input: InitFileUploadInput;
};


export type MutationMarkProgramAsFavoriteArgs = {
  input: FavoriteInput;
};


export type MutationMarkScheduleItemAsFavoriteArgs = {
  input: FavoriteScheduleItemInput;
};


export type MutationPutDimensionArgs = {
  input: PutDimensionInput;
};


export type MutationPutDimensionValueArgs = {
  input: PutDimensionValueInput;
};


export type MutationReorderProductsArgs = {
  input: ReorderProductsInput;
};


export type MutationResendOrderConfirmationArgs = {
  input: ResendOrderConfirmationInput;
};


export type MutationRevokeKeyPairArgs = {
  id: Scalars['String']['input'];
};


export type MutationSubscribeToSurveyResponsesArgs = {
  input: SubscriptionInput;
};


export type MutationUnmarkProgramAsFavoriteArgs = {
  input: FavoriteInput;
};


export type MutationUnmarkScheduleItemAsFavoriteArgs = {
  input: FavoriteScheduleItemInput;
};


export type MutationUnsubscribeFromSurveyResponsesArgs = {
  input: SubscriptionInput;
};


export type MutationUpdateFormArgs = {
  input: UpdateFormInput;
};


export type MutationUpdateFormFieldsArgs = {
  input: UpdateFormFieldsInput;
};


export type MutationUpdateOrderArgs = {
  input: UpdateOrderInput;
};


export type MutationUpdateProductArgs = {
  input: UpdateProductInput;
};


export type MutationUpdateProgramArgs = {
  input: UpdateProgramInput;
};


export type MutationUpdateProgramFormArgs = {
  input: UpdateSurveyInput;
};


export type MutationUpdateQuotaArgs = {
  input: UpdateQuotaInput;
};


export type MutationUpdateResponseDimensionsArgs = {
  input: UpdateResponseDimensionsInput;
};


export type MutationUpdateSurveyArgs = {
  input: UpdateSurveyInput;
};

export type OrderProductType = {
  __typename?: 'OrderProductType';
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Int']['output'];
  title: Scalars['String']['output'];
};

/** An enumeration. */
export enum PaymentProvider {
  None = 'NONE',
  Paytrail = 'PAYTRAIL',
  Stripe = 'STRIPE'
}

/** An enumeration. */
export enum PaymentStampType {
  CancelWithoutRefund = 'CANCEL_WITHOUT_REFUND',
  CreatePaymentFailure = 'CREATE_PAYMENT_FAILURE',
  CreatePaymentRequest = 'CREATE_PAYMENT_REQUEST',
  CreatePaymentSuccess = 'CREATE_PAYMENT_SUCCESS',
  CreateRefundFailure = 'CREATE_REFUND_FAILURE',
  CreateRefundRequest = 'CREATE_REFUND_REQUEST',
  CreateRefundSuccess = 'CREATE_REFUND_SUCCESS',
  ManualRefund = 'MANUAL_REFUND',
  PaymentCallback = 'PAYMENT_CALLBACK',
  PaymentRedirect = 'PAYMENT_REDIRECT',
  RefundCallback = 'REFUND_CALLBACK',
  ZeroPrice = 'ZERO_PRICE'
}

/** An enumeration. */
export enum PaymentStatus {
  Cancelled = 'CANCELLED',
  Failed = 'FAILED',
  NotStarted = 'NOT_STARTED',
  Paid = 'PAID',
  Pending = 'PENDING',
  Refunded = 'REFUNDED',
  RefundFailed = 'REFUND_FAILED',
  RefundRequested = 'REFUND_REQUESTED'
}

export type ProfileOrderType = {
  __typename?: 'ProfileOrderType';
  canPay: Scalars['Boolean']['output'];
  createdAt: Scalars['DateTime']['output'];
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  /** Returns a link at which the user can view their electronic tickets. They need to be the owner of the order (or an admin) to access that link. Returns null if the order does not contain electronic tickets. */
  eticketsLink?: Maybe<Scalars['String']['output']>;
  event: LimitedEventType;
  firstName: Scalars['String']['output'];
  formattedOrderNumber: Scalars['String']['output'];
  id: Scalars['UUID']['output'];
  language: TicketsV2OrderLanguageChoices;
  lastName: Scalars['String']['output'];
  /** Order number used in contexts where UUID cannot be used. Such places include generating reference numbers and the customer reading the order number aloud to an event rep. Prefer id (UUID) for everything else (eg. URLs). */
  orderNumber: Scalars['Int']['output'];
  phone: Scalars['String']['output'];
  /** Returns a link at which the user can view their electronic tickets. They need to be the owner of the order (or an admin) to access that link. Returns null if the order does not contain electronic tickets. */
  products: Array<OrderProductType>;
  status: PaymentStatus;
  totalPrice: Scalars['Decimal']['output'];
};

export enum ProfileProgramInclude {
  Favorited = 'FAVORITED',
  Hosting = 'HOSTING',
  SignedUp = 'SIGNED_UP'
}

export type ProfileResponseType = {
  __typename?: 'ProfileResponseType';
  /** Returns the dimensions of the response as a dict of dimension slug -> list of dimension value slugs. If the response is not related to a survey, there will be no dimensions and an empty dict will always be returned. Using this field is more efficient than querying the dimensions field on the response, as the dimensions are cached on the response object. The respondent will only see values of dimensions that are designated as being shown to the respondent. */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who submitted the response. If response is to an anonymous survey,
   * this information will not be available.
   *
   */
  createdBy?: Maybe<LimitedUserType>;
  dimensions?: Maybe<Array<ResponseDimensionValueType>>;
  form: FormType;
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
  /** Language code of the form used to submit this response. */
  language: Scalars['String']['output'];
  values?: Maybe<Scalars['GenericScalar']['output']>;
};


export type ProfileResponseTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type ProfileResponseTypeDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type ProfileResponseTypeValuesArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};

export type ProfileType = {
  __typename?: 'ProfileType';
  displayName?: Maybe<Scalars['String']['output']>;
  /** Email is the primary means of contact for event-related matters. */
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  /** Namespace for queries related to forms and the current user. */
  forms: FormsProfileMetaType;
  keypairs?: Maybe<Array<KeyPairType>>;
  lastName?: Maybe<Scalars['String']['output']>;
  /** If you go by a nick name or handle that you want printed in your badge and programme details, enter it here. */
  nick: Scalars['String']['output'];
  phoneNumber?: Maybe<Scalars['String']['output']>;
  /** Namespace for queries related to programs and the current user. */
  program: ProgramV2ProfileMetaType;
  /** Namespace for queries related to tickets and the current user. */
  tickets: TicketsV2ProfileMetaType;
};

export type ProgramAnnotationType = {
  __typename?: 'ProgramAnnotationType';
  annotation: AnnotationSchemoidType;
  value?: Maybe<Scalars['GenericScalar']['output']>;
};


export type ProgramAnnotationTypeValueArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type ProgramDimensionValueType = {
  __typename?: 'ProgramDimensionValueType';
  dimension: FullDimensionType;
  value: DimensionValueType;
};

export type ProgramFeedbackInput = {
  eventSlug: Scalars['String']['input'];
  feedback: Scalars['String']['input'];
  kissa: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
};

export type ProgramLink = {
  __typename?: 'ProgramLink';
  href: Scalars['String']['output'];
  title: Scalars['String']['output'];
  type: ProgramLinkType;
};

export enum ProgramLinkType {
  Calendar = 'CALENDAR',
  Feedback = 'FEEDBACK',
  GuideV2Embedded = 'GUIDE_V2_EMBEDDED',
  GuideV2Light = 'GUIDE_V2_LIGHT',
  Material = 'MATERIAL',
  Other = 'OTHER',
  Recording = 'RECORDING',
  Remote = 'REMOTE',
  Reservation = 'RESERVATION',
  Signup = 'SIGNUP',
  Tickets = 'TICKETS'
}

/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaType = {
  __typename?: 'ProgramV2EventMetaType';
  annotations: Array<AnnotationSchemoidType>;
  /** Returns a link to the calendar export view for the event. The calendar export view accepts the following GET parameters, all optional: `favorited` - set to a truthy value to receive only favorites, `slug` - include only these programmes (can be multi-valued or separated by commas), `language` - the language to use when resolving dimensions. */
  calendarExportLink: Scalars['String']['output'];
  /** Returns the total number of program offers (not taking into account filters). */
  countProgramOffers: Scalars['Int']['output'];
  /** `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  dimensions: Array<FullDimensionType>;
  program?: Maybe<FullProgramType>;
  /** Returns a single response program offer. */
  programOffer?: Maybe<FullResponseType>;
  /** Returns all responses to all program offer forms of this event. */
  programOffers: Array<FullResponseType>;
  programs: Array<FullProgramType>;
  scheduleItems: Array<FullScheduleItemType>;
  /** Returns the state dimension of the event, if there is one. */
  stateDimension?: Maybe<FullDimensionType>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeAnnotationsArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeDimensionsArgs = {
  isListFilter?: InputMaybe<Scalars['Boolean']['input']>;
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeProgramArgs = {
  slug: Scalars['String']['input'];
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeProgramOfferArgs = {
  id: Scalars['String']['input'];
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeProgramOffersArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeProgramsArgs = {
  favoritesOnly?: InputMaybe<Scalars['Boolean']['input']>;
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
  updatedAfter?: InputMaybe<Scalars['DateTime']['input']>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeScheduleItemsArgs = {
  favoritesOnly?: InputMaybe<Scalars['Boolean']['input']>;
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
  updatedAfter?: InputMaybe<Scalars['DateTime']['input']>;
};

export type ProgramV2ProfileMetaType = {
  __typename?: 'ProgramV2ProfileMetaType';
  /** Get programs that relate to this user in some way. Currently only favorites are implemented, but in the future also signed up and hosting. Dimension filter may only be specified when event_slug is given. */
  programs?: Maybe<Array<FullProgramType>>;
  /** Get programs that relate to this user in some way. Currently only favorites are implemented, but in the future also signed up and hosting. Dimension filter may only be specified when event_slug is given. */
  scheduleItems?: Maybe<Array<FullScheduleItemType>>;
};


export type ProgramV2ProfileMetaTypeProgramsArgs = {
  eventSlug?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
  include?: InputMaybe<Array<InputMaybe<ProfileProgramInclude>>>;
};


export type ProgramV2ProfileMetaTypeScheduleItemsArgs = {
  eventSlug?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
  include?: InputMaybe<Array<InputMaybe<ProfileProgramInclude>>>;
};

export type PutDimension = {
  __typename?: 'PutDimension';
  dimension?: Maybe<FullDimensionType>;
};

export type PutDimensionInput = {
  /** If set, update existing; otherwise, create new */
  dimensionSlug?: InputMaybe<Scalars['String']['input']>;
  formData: Scalars['GenericScalar']['input'];
  scopeSlug: Scalars['String']['input'];
  universeSlug: Scalars['String']['input'];
};

export type PutDimensionValue = {
  __typename?: 'PutDimensionValue';
  value?: Maybe<DimensionValueType>;
};

export type PutDimensionValueInput = {
  dimensionSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  scopeSlug: Scalars['String']['input'];
  universeSlug: Scalars['String']['input'];
  /** If set, update existing; otherwise, create new */
  valueSlug?: InputMaybe<Scalars['String']['input']>;
};

export type Query = {
  __typename?: 'Query';
  event?: Maybe<FullEventType>;
  profile?: Maybe<ProfileType>;
};


export type QueryEventArgs = {
  slug: Scalars['String']['input'];
};

/** An enumeration. */
export enum ReceiptStatus {
  Failure = 'FAILURE',
  Processing = 'PROCESSING',
  Requested = 'REQUESTED',
  Success = 'SUCCESS'
}

/** An enumeration. */
export enum ReceiptType {
  Cancelled = 'CANCELLED',
  Paid = 'PAID',
  Refunded = 'REFUNDED'
}

/** An enumeration. */
export enum RefundType {
  Manual = 'MANUAL',
  None = 'NONE',
  Provider = 'PROVIDER'
}

export type ReorderProducts = {
  __typename?: 'ReorderProducts';
  products: Array<LimitedProductType>;
};

export type ReorderProductsInput = {
  eventSlug: Scalars['String']['input'];
  productIds: Array<Scalars['String']['input']>;
};

export type ResendOrderConfirmation = {
  __typename?: 'ResendOrderConfirmation';
  order?: Maybe<LimitedOrderType>;
  receipt?: Maybe<LimitedReceiptType>;
};

export type ResendOrderConfirmationInput = {
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
};

export type ResponseDimensionValueType = {
  __typename?: 'ResponseDimensionValueType';
  dimension: FullDimensionType;
  value: DimensionValueType;
};

export type RevokeKeyPair = {
  __typename?: 'RevokeKeyPair';
  id: Scalars['String']['output'];
};

export type SubscribeToSurveyResponses = {
  __typename?: 'SubscribeToSurveyResponses';
  success: Scalars['Boolean']['output'];
};

export type SubscriptionInput = {
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

/** An enumeration. */
export enum SurveyApp {
  Forms = 'FORMS',
  ProgramV2 = 'PROGRAM_V2'
}

/** An enumeration. */
export enum SurveyRelation {
  Accessible = 'ACCESSIBLE',
  Subscribed = 'SUBSCRIBED'
}

export type TicketsV2EventMetaType = {
  __typename?: 'TicketsV2EventMetaType';
  /** Returns orders made to this event. Admin oriented view; customers will access order information through `profile.tickets`. */
  order?: Maybe<FullOrderType>;
  /** Returns orders made to this event. Admin oriented view; customers will access order information through `profile.tickets`. */
  orders: Array<FullOrderType>;
  /** Returns a product defined for this event. Admin oriented view; customers will access product information through /api/tickets-v2. */
  product: FullProductType;
  /** Returns products defined for this event. Admin oriented view; customers will access product information through /api/tickets-v2. */
  products: Array<FullProductType>;
  providerId: TicketsV2TicketsV2EventMetaProviderIdChoices;
  /** Returns a quota defined for this event. Admin oriented view; customers will access product information through /api/tickets-v2. */
  quota: FullQuotaType;
  quotas: Array<FullQuotaType>;
};


export type TicketsV2EventMetaTypeOrderArgs = {
  id: Scalars['String']['input'];
};


export type TicketsV2EventMetaTypeOrdersArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  search?: InputMaybe<Scalars['String']['input']>;
};


export type TicketsV2EventMetaTypeProductArgs = {
  id: Scalars['String']['input'];
};


export type TicketsV2EventMetaTypeQuotaArgs = {
  id: Scalars['Int']['input'];
};

/** An enumeration. */
export enum TicketsV2OrderLanguageChoices {
  /** English */
  En = 'EN',
  /** Finnish */
  Fi = 'FI',
  /** Swedish */
  Sv = 'SV'
}

export type TicketsV2ProfileMetaType = {
  __typename?: 'TicketsV2ProfileMetaType';
  /** Returns true if the user has unlinked orders made with the same email address. These orders can be linked to the user account by verifying the email address again. */
  haveUnlinkedOrders: Scalars['Boolean']['output'];
  order?: Maybe<ProfileOrderType>;
  /** Returns the orders of the current user. Note that unlinked orders made with the same email address are not returned. They need to be linked first (ie. their email confirmed again). */
  orders: Array<ProfileOrderType>;
};


export type TicketsV2ProfileMetaTypeOrderArgs = {
  eventSlug: Scalars['String']['input'];
  id: Scalars['String']['input'];
};

/** An enumeration. */
export enum TicketsV2TicketsV2EventMetaProviderIdChoices {
  /** NONE */
  A_0 = 'A_0',
  /** PAYTRAIL */
  A_1 = 'A_1',
  /** STRIPE */
  A_2 = 'A_2'
}

/** Deprecated. Use UnmarkScheduleItemAsFavorite instead. */
export type UnmarkProgramAsFavorite = {
  __typename?: 'UnmarkProgramAsFavorite';
  success: Scalars['Boolean']['output'];
};

export type UnmarkScheduleItemAsFavorite = {
  __typename?: 'UnmarkScheduleItemAsFavorite';
  success: Scalars['Boolean']['output'];
};

export type UnsubscribeFromSurveyResponses = {
  __typename?: 'UnsubscribeFromSurveyResponses';
  success: Scalars['Boolean']['output'];
};

export type UpdateForm = {
  __typename?: 'UpdateForm';
  survey?: Maybe<FullSurveyType>;
};

export type UpdateFormFields = {
  __typename?: 'UpdateFormFields';
  survey?: Maybe<FullSurveyType>;
};

export type UpdateFormFieldsInput = {
  eventSlug: Scalars['String']['input'];
  fields: Scalars['GenericScalar']['input'];
  language: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type UpdateFormInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  language: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type UpdateOrder = {
  __typename?: 'UpdateOrder';
  order?: Maybe<LimitedOrderType>;
};

export type UpdateOrderInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  orderId: Scalars['String']['input'];
};

export type UpdateProduct = {
  __typename?: 'UpdateProduct';
  product?: Maybe<LimitedProductType>;
};

export type UpdateProductInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  productId: Scalars['String']['input'];
};

export type UpdateProgram = {
  __typename?: 'UpdateProgram';
  program?: Maybe<FullProgramType>;
};

export type UpdateProgramForm = {
  __typename?: 'UpdateProgramForm';
  survey?: Maybe<FullSurveyType>;
};

export type UpdateProgramInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  programSlug: Scalars['String']['input'];
};

export type UpdateQuota = {
  __typename?: 'UpdateQuota';
  quota?: Maybe<LimitedQuotaType>;
};

export type UpdateQuotaInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  quotaId: Scalars['String']['input'];
};

export type UpdateResponseDimensions = {
  __typename?: 'UpdateResponseDimensions';
  response?: Maybe<FullResponseType>;
};

export type UpdateResponseDimensionsInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  responseId: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type UpdateSurvey = {
  __typename?: 'UpdateSurvey';
  survey?: Maybe<FullSurveyType>;
};

export type UpdateSurveyInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  surveySlug: Scalars['String']['input'];
};

export type CreateSurveyResponseMutationVariables = Exact<{
  input: CreateSurveyResponseInput;
}>;


export type CreateSurveyResponseMutation = { __typename?: 'Mutation', createSurveyResponse?: { __typename?: 'CreateSurveyResponse', response?: { __typename?: 'ProfileResponseType', id: string } | null } | null };

export type InitFileUploadMutationMutationVariables = Exact<{
  input: InitFileUploadInput;
}>;


export type InitFileUploadMutationMutation = { __typename?: 'Mutation', initFileUpload?: { __typename?: 'InitFileUploadResponse', uploadUrl?: string | null, fileUrl?: string | null } | null };

export type SurveyPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyPageQueryQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', displayName?: string | null, email: string } | null, event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', loginRequired: boolean, anonymity: Anonymity, maxResponsesPerUser: number, countResponsesByCurrentUser: number, form?: { __typename?: 'FormType', language: FormsFormLanguageChoices, title: string, description: string, fields?: unknown | null } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type SurveyThankYouPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyThankYouPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', form?: { __typename?: 'FormType', title: string, thankYouMessage: string } | null } | null } | null } | null };

export type ResendOrderConfirmationMutationVariables = Exact<{
  input: ResendOrderConfirmationInput;
}>;


export type ResendOrderConfirmationMutation = { __typename?: 'Mutation', resendOrderConfirmation?: { __typename?: 'ResendOrderConfirmation', order?: { __typename?: 'LimitedOrderType', id: string } | null } | null };

export type UpdateOrderMutationVariables = Exact<{
  input: UpdateOrderInput;
}>;


export type UpdateOrderMutation = { __typename?: 'Mutation', updateOrder?: { __typename?: 'UpdateOrder', order?: { __typename?: 'LimitedOrderType', id: string } | null } | null };

export type CancelAndRefundOrderMutationVariables = Exact<{
  input: CancelAndRefundOrderInput;
}>;


export type CancelAndRefundOrderMutation = { __typename?: 'Mutation', cancelAndRefundOrder?: { __typename?: 'CancelAndRefundOrder', order?: { __typename?: 'LimitedOrderType', id: string } | null } | null };

export type AdminOrderPaymentStampFragment = { __typename?: 'LimitedPaymentStampType', id: string, createdAt: string, correlationId: string, provider: PaymentProvider, type: PaymentStampType, status: PaymentStatus, data: unknown };

export type AdminOrderReceiptFragment = { __typename?: 'LimitedReceiptType', correlationId: string, createdAt: string, email: string, type: ReceiptType, status: ReceiptStatus };

export type AdminOrderCodeFragment = { __typename?: 'LimitedCodeType', code: string, literateCode: string, status: CodeStatus, usedOn?: string | null, productText: string };

export type AdminOrderDetailQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
}>;


export type AdminOrderDetailQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, tickets?: { __typename?: 'TicketsV2EventMetaType', order?: { __typename?: 'FullOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, firstName: string, lastName: string, email: string, phone: string, canRefund: boolean, products: Array<{ __typename?: 'OrderProductType', title: string, quantity: number, price: any }>, paymentStamps: Array<{ __typename?: 'LimitedPaymentStampType', id: string, createdAt: string, correlationId: string, provider: PaymentProvider, type: PaymentStampType, status: PaymentStatus, data: unknown }>, receipts: Array<{ __typename?: 'LimitedReceiptType', correlationId: string, createdAt: string, email: string, type: ReceiptType, status: ReceiptStatus }>, codes: Array<{ __typename?: 'LimitedCodeType', code: string, literateCode: string, status: CodeStatus, usedOn?: string | null, productText: string }> } | null } | null } | null };

export type OrderListFragment = { __typename?: 'FullOrderType', id: string, formattedOrderNumber: string, displayName: string, email: string, createdAt: string, totalPrice: any, status: PaymentStatus };

export type ProductChoiceFragment = { __typename?: 'FullProductType', id: string, title: string };

export type OrderListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
  searchTerm?: InputMaybe<Scalars['String']['input']>;
}>;


export type OrderListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', products: Array<{ __typename?: 'FullProductType', id: string, title: string }>, orders: Array<{ __typename?: 'FullOrderType', id: string, formattedOrderNumber: string, displayName: string, email: string, createdAt: string, totalPrice: any, status: PaymentStatus }> } | null } | null };

export type UpdateProductMutationVariables = Exact<{
  input: UpdateProductInput;
}>;


export type UpdateProductMutation = { __typename?: 'Mutation', updateProduct?: { __typename?: 'UpdateProduct', product?: { __typename?: 'LimitedProductType', id: string } | null } | null };

export type DeleteProductMutationVariables = Exact<{
  input: DeleteProductInput;
}>;


export type DeleteProductMutation = { __typename?: 'Mutation', deleteProduct?: { __typename?: 'DeleteProduct', id: string } | null };

export type AdminProductOldVersionFragment = { __typename?: 'LimitedProductType', createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number };

export type AdminProductDetailFragment = { __typename?: 'FullProductType', id: string, createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number, availableFrom?: string | null, availableUntil?: string | null, canDelete: boolean, quotas: Array<{ __typename?: 'LimitedQuotaType', id: string }>, supersededBy?: { __typename?: 'LimitedProductType', id: string } | null, oldVersions: Array<{ __typename?: 'LimitedProductType', createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number }> };

export type AdminProductDetailPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  productId: Scalars['String']['input'];
}>;


export type AdminProductDetailPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', quotas: Array<{ __typename?: 'FullQuotaType', id: string, name: string, countTotal: number }>, product: { __typename?: 'FullProductType', id: string, createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number, availableFrom?: string | null, availableUntil?: string | null, canDelete: boolean, quotas: Array<{ __typename?: 'LimitedQuotaType', id: string }>, supersededBy?: { __typename?: 'LimitedProductType', id: string } | null, oldVersions: Array<{ __typename?: 'LimitedProductType', createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number }> } } | null } | null };

export type CreateProductMutationVariables = Exact<{
  input: CreateProductInput;
}>;


export type CreateProductMutation = { __typename?: 'Mutation', createProduct?: { __typename?: 'CreateProduct', product?: { __typename?: 'LimitedProductType', id: string } | null } | null };

export type ReorderProductsMutationVariables = Exact<{
  input: ReorderProductsInput;
}>;


export type ReorderProductsMutation = { __typename?: 'Mutation', reorderProducts?: { __typename?: 'ReorderProducts', products: Array<{ __typename?: 'LimitedProductType', id: string }> } | null };

export type ProductListFragment = { __typename?: 'FullProductType', id: string, title: string, description: string, price: any, isAvailable: boolean, availableFrom?: string | null, availableUntil?: string | null, countPaid: number, countReserved: number, countAvailable?: number | null };

export type ProductListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
}>;


export type ProductListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', products: Array<{ __typename?: 'FullProductType', id: string, title: string, description: string, price: any, isAvailable: boolean, availableFrom?: string | null, availableUntil?: string | null, countPaid: number, countReserved: number, countAvailable?: number | null }> } | null } | null };

export type UpdateProgramBasicInfoMutationVariables = Exact<{
  input: UpdateProgramInput;
}>;


export type UpdateProgramBasicInfoMutation = { __typename?: 'Mutation', updateProgram?: { __typename?: 'UpdateProgram', program?: { __typename?: 'FullProgramType', slug: string } | null } | null };

export type ProgramAdminDetailQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminDetailQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', calendarExportLink: string, program?: { __typename?: 'FullProgramType', slug: string, title: string, description: string, cachedHosts: string, programOffer?: { __typename?: 'LimitedResponseType', id: string, values?: unknown | null } | null, links: Array<{ __typename?: 'ProgramLink', type: ProgramLinkType, href: string, title: string }>, annotations: Array<{ __typename?: 'ProgramAnnotationType', value?: unknown | null, annotation: { __typename?: 'AnnotationSchemoidType', slug: string, type: AnnotationDataType, title: string } }>, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null } }>, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, subtitle: string, location?: string | null, startTime: string, endTime: string }> } | null } | null } | null };

export type ProgramAdminFragment = { __typename?: 'FullProgramType', slug: string, title: string, cachedDimensions?: unknown | null, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', startTime: string }> };

export type ProgramAdminListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type ProgramAdminListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, program?: { __typename?: 'ProgramV2EventMetaType', listFilters: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, keyDimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, programs: Array<{ __typename?: 'FullProgramType', slug: string, title: string, cachedDimensions?: unknown | null, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', startTime: string }> }> } | null } | null };

export type PutProgramDimensionMutationVariables = Exact<{
  input: PutDimensionInput;
}>;


export type PutProgramDimensionMutation = { __typename?: 'Mutation', putDimension?: { __typename?: 'PutDimension', dimension?: { __typename?: 'FullDimensionType', slug: string } | null } | null };

export type DeleteProgramDimensionMutationVariables = Exact<{
  input: DeleteDimensionInput;
}>;


export type DeleteProgramDimensionMutation = { __typename?: 'Mutation', deleteDimension?: { __typename?: 'DeleteDimension', slug?: string | null } | null };

export type PutProgramDimensionValueMutationVariables = Exact<{
  input: PutDimensionValueInput;
}>;


export type PutProgramDimensionValueMutation = { __typename?: 'Mutation', putDimensionValue?: { __typename?: 'PutDimensionValue', value?: { __typename?: 'DimensionValueType', slug: string } | null } | null };

export type DeleteProgramDimensionValueMutationVariables = Exact<{
  input: DeleteDimensionValueInput;
}>;


export type DeleteProgramDimensionValueMutation = { __typename?: 'Mutation', deleteDimensionValue?: { __typename?: 'DeleteDimensionValue', slug?: string | null } | null };

export type ProgramDimensionsListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale: Scalars['String']['input'];
}>;


export type ProgramDimensionsListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, program?: { __typename?: 'ProgramV2EventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isInitial: boolean, isTechnical: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }> } | null } | null };

export type UpdateProgramFormLanguageMutationVariables = Exact<{
  input: UpdateFormInput;
}>;


export type UpdateProgramFormLanguageMutation = { __typename?: 'Mutation', updateForm?: { __typename?: 'UpdateForm', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type DeleteProgramFormLanguageMutationVariables = Exact<{
  input: DeleteSurveyLanguageInput;
}>;


export type DeleteProgramFormLanguageMutation = { __typename?: 'Mutation', deleteSurveyLanguage?: { __typename?: 'DeleteSurveyLanguage', language?: string | null } | null };

export type UpdateFormFieldsMutationMutationVariables = Exact<{
  input: UpdateFormFieldsInput;
}>;


export type UpdateFormFieldsMutationMutation = { __typename?: 'Mutation', updateFormFields?: { __typename?: 'UpdateFormFields', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type EditProgramFormFieldsFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditProgramFormFieldsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditProgramFormFieldsPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type EditProgramFormLanguageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditProgramFormLanguagePageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditProgramFormLanguagePageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type CreateProgramFormLanguageMutationVariables = Exact<{
  input: CreateSurveyLanguageInput;
}>;


export type CreateProgramFormLanguageMutation = { __typename?: 'Mutation', createSurveyLanguage?: { __typename?: 'CreateSurveyLanguage', form?: { __typename?: 'FormType', language: FormsFormLanguageChoices } | null } | null };

export type UpdateProgramFormMutationMutationVariables = Exact<{
  input: UpdateSurveyInput;
}>;


export type UpdateProgramFormMutationMutation = { __typename?: 'Mutation', updateProgramForm?: { __typename?: 'UpdateProgramForm', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type DeleteProrgamFormMutationMutationVariables = Exact<{
  input: DeleteSurveyInput;
}>;


export type DeleteProrgamFormMutationMutation = { __typename?: 'Mutation', deleteSurvey?: { __typename?: 'DeleteSurvey', slug?: string | null } | null };

export type EditProgramFormFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, activeFrom?: string | null, activeUntil?: string | null, canRemove: boolean, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> };

export type EditProgramFormPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditProgramFormPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, activeFrom?: string | null, activeUntil?: string | null, canRemove: boolean, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> } | null } | null } | null };

export type CreateProgramFormMutationVariables = Exact<{
  input: CreateProgramFormInput;
}>;


export type CreateProgramFormMutation = { __typename?: 'Mutation', createProgramForm?: { __typename?: 'CreateProgramForm', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type OfferFormFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type ProgramFormsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramFormsPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, forms?: { __typename?: 'FormsEventMetaType', surveys?: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> }> | null } | null } | null };

export type AcceptProgramOfferMutationVariables = Exact<{
  input: AcceptProgramOfferInput;
}>;


export type AcceptProgramOfferMutation = { __typename?: 'Mutation', acceptProgramOffer?: { __typename?: 'AcceptProgramOffer', program: { __typename?: 'FullProgramType', slug: string } } | null };

export type ProgramOfferDetailFragment = { __typename?: 'FullResponseType', id: string, sequenceNumber: number, createdAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string, email: string } | null, form: { __typename?: 'FormType', fields?: unknown | null, survey?: { __typename?: 'LimitedSurveyType', title?: string | null, slug: string } | null }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> };

export type ProgramOfferPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramOfferPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, program?: { __typename?: 'ProgramV2EventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, programOffer?: { __typename?: 'FullResponseType', id: string, sequenceNumber: number, createdAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string, email: string } | null, form: { __typename?: 'FormType', fields?: unknown | null, survey?: { __typename?: 'LimitedSurveyType', title?: string | null, slug: string } | null }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> } | null } | null } | null };

export type ProgramOfferFragment = { __typename?: 'FullResponseType', id: string, createdAt: string, sequenceNumber: number, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string } | null, form: { __typename?: 'FormType', language: FormsFormLanguageChoices, survey?: { __typename?: 'LimitedSurveyType', title?: string | null } | null }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> };

export type ProgramOfferDimensionFragment = { __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string, isTechnical: boolean }> };

export type ProgramOffersQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type ProgramOffersQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, program?: { __typename?: 'ProgramV2EventMetaType', countProgramOffers: number, listFilters: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string, isTechnical: boolean }> }>, keyDimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string, isTechnical: boolean }> }>, stateDimension?: { __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string, isTechnical: boolean }> } | null, programOffers: Array<{ __typename?: 'FullResponseType', id: string, createdAt: string, sequenceNumber: number, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string } | null, form: { __typename?: 'FormType', language: FormsFormLanguageChoices, survey?: { __typename?: 'LimitedSurveyType', title?: string | null } | null }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> }> } | null } | null };

export type MarkScheduleItemAsFavoriteMutationVariables = Exact<{
  input: FavoriteScheduleItemInput;
}>;


export type MarkScheduleItemAsFavoriteMutation = { __typename?: 'Mutation', markScheduleItemAsFavorite?: { __typename?: 'MarkScheduleItemAsFavorite', success: boolean } | null };

export type UnmarkScheduleItemAsFavoriteMutationVariables = Exact<{
  input: FavoriteScheduleItemInput;
}>;


export type UnmarkScheduleItemAsFavoriteMutation = { __typename?: 'Mutation', unmarkScheduleItemAsFavorite?: { __typename?: 'UnmarkScheduleItemAsFavorite', success: boolean } | null };

export type ScheduleProgramFragment = { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string };

export type ScheduleItemListFragment = { __typename?: 'FullScheduleItemType', slug: string, location?: string | null, subtitle: string, startTime: string, endTime: string, program: { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string } };

export type ProgramListQueryQueryVariables = Exact<{
  locale?: InputMaybe<Scalars['String']['input']>;
  eventSlug: Scalars['String']['input'];
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
}>;


export type ProgramListQueryQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', program: { __typename?: 'ProgramV2ProfileMetaType', scheduleItems?: Array<{ __typename?: 'FullScheduleItemType', slug: string, location?: string | null, subtitle: string, startTime: string, endTime: string, program: { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string } }> | null } } | null, event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', calendarExportLink: string, listFilters: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isListFilter: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, scheduleItems: Array<{ __typename?: 'FullScheduleItemType', slug: string, location?: string | null, subtitle: string, startTime: string, endTime: string, program: { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string } }> } | null } | null };

export type CreateFeedbackMutationVariables = Exact<{
  input: ProgramFeedbackInput;
}>;


export type CreateFeedbackMutation = { __typename?: 'Mutation', createProgramFeedback?: { __typename?: 'CreateProgramFeedback', success: boolean } | null };

export type ProgramFeedbackQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
}>;


export type ProgramFeedbackQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, program?: { __typename?: 'ProgramV2EventMetaType', program?: { __typename?: 'FullProgramType', title: string, isAcceptingFeedback: boolean } | null } | null } | null };

export type ProgramDetailAnnotationFragment = { __typename?: 'ProgramAnnotationType', value?: unknown | null, annotation: { __typename?: 'AnnotationSchemoidType', slug: string, type: AnnotationDataType, title: string } };

export type ProgramDetailQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramDetailQueryQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', program: { __typename?: 'ProgramV2ProfileMetaType', scheduleItems?: Array<{ __typename?: 'FullScheduleItemType', slug: string }> | null } } | null, event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', calendarExportLink: string, program?: { __typename?: 'FullProgramType', title: string, description: string, cachedHosts: string, links: Array<{ __typename?: 'ProgramLink', type: ProgramLinkType, href: string, title: string }>, annotations: Array<{ __typename?: 'ProgramAnnotationType', value?: unknown | null, annotation: { __typename?: 'AnnotationSchemoidType', slug: string, type: AnnotationDataType, title: string } }>, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null } }>, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, subtitle: string, location?: string | null, startTime: string, endTime: string }> } | null } | null } | null };

export type UpdateQuotaMutationVariables = Exact<{
  input: UpdateQuotaInput;
}>;


export type UpdateQuotaMutation = { __typename?: 'Mutation', updateQuota?: { __typename?: 'UpdateQuota', quota?: { __typename?: 'LimitedQuotaType', id: string } | null } | null };

export type DeleteQuotaMutationVariables = Exact<{
  input: DeleteQuotaInput;
}>;


export type DeleteQuotaMutation = { __typename?: 'Mutation', deleteQuota?: { __typename?: 'DeleteQuota', id: string } | null };

export type QuotaProductFragment = { __typename?: 'LimitedProductType', id: string, title: string, price: any, countReserved: number };

export type AdminQuotaDetailPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  quotaId: Scalars['Int']['input'];
}>;


export type AdminQuotaDetailPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', quota: { __typename?: 'FullQuotaType', id: string, name: string, countReserved: number, canDelete: boolean, quota: number, products: Array<{ __typename?: 'LimitedProductType', id: string, title: string, price: any, countReserved: number }> } } | null } | null };

export type CreateQuotaMutationVariables = Exact<{
  input: CreateQuotaInput;
}>;


export type CreateQuotaMutation = { __typename?: 'Mutation', createQuota?: { __typename?: 'CreateQuota', quota?: { __typename?: 'LimitedQuotaType', id: string } | null } | null };

export type QuotaListFragment = { __typename?: 'FullQuotaType', id: string, countPaid: number, countReserved: number, countAvailable: number, countTotal: number, title: string };

export type QuotaListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
}>;


export type QuotaListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', quotas: Array<{ __typename?: 'FullQuotaType', id: string, countPaid: number, countReserved: number, countAvailable: number, countTotal: number, title: string }> } | null } | null };

export type PutSurveyDimensionMutationVariables = Exact<{
  input: PutDimensionInput;
}>;


export type PutSurveyDimensionMutation = { __typename?: 'Mutation', putDimension?: { __typename?: 'PutDimension', dimension?: { __typename?: 'FullDimensionType', slug: string } | null } | null };

export type DeleteSurveyDimensionMutationVariables = Exact<{
  input: DeleteDimensionInput;
}>;


export type DeleteSurveyDimensionMutation = { __typename?: 'Mutation', deleteDimension?: { __typename?: 'DeleteDimension', slug?: string | null } | null };

export type PutSurveyDimensionValueMutationVariables = Exact<{
  input: PutDimensionValueInput;
}>;


export type PutSurveyDimensionValueMutation = { __typename?: 'Mutation', putDimensionValue?: { __typename?: 'PutDimensionValue', value?: { __typename?: 'DimensionValueType', slug: string } | null } | null };

export type DeleteSurveyDimensionValueMutationVariables = Exact<{
  input: DeleteDimensionValueInput;
}>;


export type DeleteSurveyDimensionValueMutation = { __typename?: 'Mutation', deleteDimensionValue?: { __typename?: 'DeleteDimensionValue', slug?: string | null } | null };

export type ValueFieldsFragment = { __typename?: 'DimensionValueType', slug: string, color: string, isInitial: boolean, isTechnical: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string };

export type DimensionRowGroupFragment = { __typename?: 'FullDimensionType', slug: string, canRemove: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isInitial: boolean, isTechnical: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> };

export type DimensionsListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale: Scalars['String']['input'];
}>;


export type DimensionsListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }>, dimensions?: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isInitial: boolean, isTechnical: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }> | null } | null } | null } | null };

export type UpdateFormMutationMutationVariables = Exact<{
  input: UpdateFormInput;
}>;


export type UpdateFormMutationMutation = { __typename?: 'Mutation', updateForm?: { __typename?: 'UpdateForm', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type DeleteSurveyLanguageMutationVariables = Exact<{
  input: DeleteSurveyLanguageInput;
}>;


export type DeleteSurveyLanguageMutation = { __typename?: 'Mutation', deleteSurveyLanguage?: { __typename?: 'DeleteSurveyLanguage', language?: string | null } | null };

export type EditSurveyFieldsPageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditSurveyFieldsPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditSurveyFieldsPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type EditFormLanguagePageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditFormLanguagePageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditFormLanguagePageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type CreateSurveyLanguageMutationVariables = Exact<{
  input: CreateSurveyLanguageInput;
}>;


export type CreateSurveyLanguageMutation = { __typename?: 'Mutation', createSurveyLanguage?: { __typename?: 'CreateSurveyLanguage', form?: { __typename?: 'FormType', language: FormsFormLanguageChoices } | null } | null };

export type UpdateSurveyMutationMutationVariables = Exact<{
  input: UpdateSurveyInput;
}>;


export type UpdateSurveyMutationMutation = { __typename?: 'Mutation', updateSurvey?: { __typename?: 'UpdateSurvey', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type DeleteSurveyMutationMutationVariables = Exact<{
  input: DeleteSurveyInput;
}>;


export type DeleteSurveyMutationMutation = { __typename?: 'Mutation', deleteSurvey?: { __typename?: 'DeleteSurvey', slug?: string | null } | null };

export type EditSurveyPageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, loginRequired: boolean, anonymity: Anonymity, maxResponsesPerUser: number, countResponsesByCurrentUser: number, activeFrom?: string | null, activeUntil?: string | null, canRemove: boolean, protectResponses: boolean, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> };

export type EditSurveyPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditSurveyPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, loginRequired: boolean, anonymity: Anonymity, maxResponsesPerUser: number, countResponsesByCurrentUser: number, activeFrom?: string | null, activeUntil?: string | null, canRemove: boolean, protectResponses: boolean, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> } | null } | null } | null };

export type UpdateResponseDimensionsMutationVariables = Exact<{
  input: UpdateResponseDimensionsInput;
}>;


export type UpdateResponseDimensionsMutation = { __typename?: 'Mutation', updateResponseDimensions?: { __typename?: 'UpdateResponseDimensions', response?: { __typename?: 'FullResponseType', id: string } | null } | null };

export type SurveyResponseDetailQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyResponseDetailQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', title?: string | null, slug: string, anonymity: Anonymity, canRemoveResponses: boolean, protectResponses: boolean, dimensions?: Array<{ __typename?: 'FullDimensionType', title?: string | null, slug: string, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', title?: string | null, slug: string, color: string }> }> | null, response?: { __typename?: 'FullResponseType', id: string, sequenceNumber: number, createdAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string, email: string } | null, form: { __typename?: 'FormType', fields?: unknown | null } } | null } | null } | null } | null };

export type SubscribeToSurveyResponsesMutationVariables = Exact<{
  input: SubscriptionInput;
}>;


export type SubscribeToSurveyResponsesMutation = { __typename?: 'Mutation', subscribeToSurveyResponses?: { __typename?: 'SubscribeToSurveyResponses', success: boolean } | null };

export type UnsubscribeFromSurveyResponsesMutationVariables = Exact<{
  input: SubscriptionInput;
}>;


export type UnsubscribeFromSurveyResponsesMutation = { __typename?: 'Mutation', unsubscribeFromSurveyResponses?: { __typename?: 'UnsubscribeFromSurveyResponses', success: boolean } | null };

export type DeleteSurveyResponsesMutationVariables = Exact<{
  input: DeleteSurveyResponsesInput;
}>;


export type DeleteSurveyResponsesMutation = { __typename?: 'Mutation', deleteSurveyResponses?: { __typename?: 'DeleteSurveyResponses', countDeleted: number } | null };

export type SurveyResponseFragment = { __typename?: 'LimitedResponseType', id: string, sequenceNumber: number, createdAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string } | null };

export type FormResponsesQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type FormResponsesQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', forms: { __typename?: 'FormsProfileMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string }> } } | null, event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, anonymity: Anonymity, fields?: unknown | null, countResponses: number, canRemoveResponses: boolean, protectResponses: boolean, dimensions?: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }> | null, responses?: Array<{ __typename?: 'LimitedResponseType', id: string, sequenceNumber: number, createdAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, createdBy?: { __typename?: 'LimitedUserType', displayName: string } | null }> | null } | null } | null } | null };

export type SurveySummaryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type SurveySummaryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', title?: string | null, fields?: unknown | null, summary?: unknown | null, countResponses: number, countFilteredResponses: number, dimensions?: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }> | null } | null } | null } | null };

export type CreateSurveyMutationVariables = Exact<{
  input: CreateSurveyInput;
}>;


export type CreateSurveyMutation = { __typename?: 'Mutation', createSurvey?: { __typename?: 'CreateSurvey', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type SurveyFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type SurveysQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveysQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', forms: { __typename?: 'FormsProfileMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, event: { __typename?: 'LimitedEventType', slug: string, name: string } }> } } | null, event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', surveys?: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> }> | null } | null } | null };

export type GenerateKeyPairMutationVariables = Exact<{
  password: Scalars['String']['input'];
}>;


export type GenerateKeyPairMutation = { __typename?: 'Mutation', generateKeyPair?: { __typename?: 'GenerateKeyPair', id: string } | null };

export type RevokeKeyPairMutationVariables = Exact<{
  id: Scalars['String']['input'];
}>;


export type RevokeKeyPairMutation = { __typename?: 'Mutation', revokeKeyPair?: { __typename?: 'RevokeKeyPair', id: string } | null };

export type ProfileEncryptionKeysFragment = { __typename?: 'KeyPairType', id: string, createdAt: string };

export type ProfileEncryptionKeysQueryVariables = Exact<{ [key: string]: never; }>;


export type ProfileEncryptionKeysQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', keypairs?: Array<{ __typename?: 'KeyPairType', id: string, createdAt: string }> | null } | null };

export type ProfileOrderDetailQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
}>;


export type ProfileOrderDetailQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', tickets: { __typename?: 'TicketsV2ProfileMetaType', order?: { __typename?: 'ProfileOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, canPay: boolean, products: Array<{ __typename?: 'OrderProductType', title: string, quantity: number, price: any }>, event: { __typename?: 'LimitedEventType', slug: string, name: string } } | null } } | null };

export type ConfirmEmailMutationVariables = Exact<{
  input: ConfirmEmailInput;
}>;


export type ConfirmEmailMutation = { __typename?: 'Mutation', confirmEmail?: { __typename?: 'ConfirmEmail', user?: { __typename?: 'LimitedUserType', email: string } | null } | null };

export type ProfileOrderFragment = { __typename?: 'ProfileOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, canPay: boolean, event: { __typename?: 'LimitedEventType', slug: string, name: string } };

export type ProfileOrdersQueryVariables = Exact<{ [key: string]: never; }>;


export type ProfileOrdersQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', tickets: { __typename?: 'TicketsV2ProfileMetaType', haveUnlinkedOrders: boolean, orders: Array<{ __typename?: 'ProfileOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, canPay: boolean, event: { __typename?: 'LimitedEventType', slug: string, name: string } }> } } | null };

export type ProfileSurveyResponsePageQueryVariables = Exact<{
  locale: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
}>;


export type ProfileSurveyResponsePageQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', forms: { __typename?: 'FormsProfileMetaType', response?: { __typename?: 'ProfileResponseType', id: string, createdAt: string, values?: unknown | null, dimensions?: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }> | null, form: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, event: { __typename?: 'LimitedEventType', slug: string, name: string }, survey?: { __typename?: 'LimitedSurveyType', anonymity: Anonymity } | null } } | null } } | null };

export type ProfileResponsesTableRowFragment = { __typename?: 'ProfileResponseType', id: string, createdAt: string, dimensions?: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }> | null, form: { __typename?: 'FormType', title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string } } };

export type OwnFormResponsesQueryVariables = Exact<{
  locale: Scalars['String']['input'];
}>;


export type OwnFormResponsesQuery = { __typename?: 'Query', profile?: { __typename?: 'ProfileType', forms: { __typename?: 'FormsProfileMetaType', responses: Array<{ __typename?: 'ProfileResponseType', id: string, createdAt: string, dimensions?: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }> | null, form: { __typename?: 'FormType', title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string } } }> } } | null };

export type DimensionBadgeFragment = { __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } };

export const AdminOrderPaymentStampFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderPaymentStamp"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedPaymentStampType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"provider"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"data"}}]}}]} as unknown as DocumentNode<AdminOrderPaymentStampFragment, unknown>;
export const AdminOrderReceiptFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderReceipt"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedReceiptType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}}]} as unknown as DocumentNode<AdminOrderReceiptFragment, unknown>;
export const AdminOrderCodeFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderCode"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedCodeType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"literateCode"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"usedOn"}},{"kind":"Field","name":{"kind":"Name","value":"productText"}}]}}]} as unknown as DocumentNode<AdminOrderCodeFragment, unknown>;
export const OrderListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OrderList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}}]} as unknown as DocumentNode<OrderListFragment, unknown>;
export const ProductChoiceFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductChoice"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]} as unknown as DocumentNode<ProductChoiceFragment, unknown>;
export const AdminProductOldVersionFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductOldVersion"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}}]} as unknown as DocumentNode<AdminProductOldVersionFragment, unknown>;
export const AdminProductDetailFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminProductOldVersion"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductOldVersion"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}}]} as unknown as DocumentNode<AdminProductDetailFragment, unknown>;
export const ProductListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"isAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}}]}}]} as unknown as DocumentNode<ProductListFragment, unknown>;
export const ProgramAdminFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdmin"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"startTime"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramAdminFragment, unknown>;
export const EditProgramFormFieldsFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramFormFields"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormFieldsFragment, unknown>;
export const EditProgramFormLanguageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramFormLanguage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormLanguageFragment, unknown>;
export const EditProgramFormFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormFragment, unknown>;
export const OfferFormFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OfferForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<OfferFormFragment, unknown>;
export const ProgramOfferDetailFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramOfferDetailFragment, unknown>;
export const ProgramOfferFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOffer"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramOfferFragment, unknown>;
export const ProgramOfferDimensionFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDimension"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}}]}}]}}]} as unknown as DocumentNode<ProgramOfferDimensionFragment, unknown>;
export const ScheduleProgramFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleProgram"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]} as unknown as DocumentNode<ScheduleProgramFragment, unknown>;
export const ScheduleItemListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleItemList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullScheduleItemType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"location"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleProgram"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleProgram"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]} as unknown as DocumentNode<ScheduleItemListFragment, unknown>;
export const ProgramDetailAnnotationFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDetailAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<ProgramDetailAnnotationFragment, unknown>;
export const QuotaProductFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaProduct"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}}]}}]} as unknown as DocumentNode<QuotaProductFragment, unknown>;
export const QuotaListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullQuotaType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","alias":{"kind":"Name","value":"title"},"name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"countTotal"}}]}}]} as unknown as DocumentNode<QuotaListFragment, unknown>;
export const ValueFieldsFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ValueFields"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isInitial"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}}]} as unknown as DocumentNode<ValueFieldsFragment, unknown>;
export const DimensionRowGroupFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionRowGroup"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ValueFields"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ValueFields"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isInitial"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}}]} as unknown as DocumentNode<DimensionRowGroupFragment, unknown>;
export const EditSurveyFieldsPageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyFieldsPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditSurveyFieldsPageFragment, unknown>;
export const EditFormLanguagePageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditFormLanguagePage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditFormLanguagePageFragment, unknown>;
export const EditSurveyPageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"loginRequired"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"maxResponsesPerUser"}},{"kind":"Field","name":{"kind":"Name","value":"countResponsesByCurrentUser"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditSurveyPageFragment, unknown>;
export const SurveyResponseFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"SurveyResponse"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}]}]}}]} as unknown as DocumentNode<SurveyResponseFragment, unknown>;
export const SurveyFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Survey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<SurveyFragment, unknown>;
export const ProfileEncryptionKeysFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileEncryptionKeys"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"KeyPairType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}}]}}]} as unknown as DocumentNode<ProfileEncryptionKeysFragment, unknown>;
export const ProfileOrderFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileOrder"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"canPay"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]} as unknown as DocumentNode<ProfileOrderFragment, unknown>;
export const ProfileResponsesTableRowFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponsesTableRow"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]} as unknown as DocumentNode<ProfileResponsesTableRowFragment, unknown>;
export const DimensionBadgeFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<DimensionBadgeFragment, unknown>;
export const CreateSurveyResponseDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateSurveyResponse"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyResponseInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyResponse"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateSurveyResponseMutation, CreateSurveyResponseMutationVariables>;
export const InitFileUploadMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"InitFileUploadMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"InitFileUploadInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"initFileUpload"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"uploadUrl"}},{"kind":"Field","name":{"kind":"Name","value":"fileUrl"}}]}}]}}]} as unknown as DocumentNode<InitFileUploadMutationMutation, InitFileUploadMutationMutationVariables>;
export const SurveyPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"NullValue"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"loginRequired"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"maxResponsesPerUser"}},{"kind":"Field","name":{"kind":"Name","value":"countResponsesByCurrentUser"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveyPageQueryQuery, SurveyPageQueryQueryVariables>;
export const SurveyThankYouPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyThankYouPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveyThankYouPageQueryQuery, SurveyThankYouPageQueryQueryVariables>;
export const ResendOrderConfirmationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ResendOrderConfirmation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ResendOrderConfirmationInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"resendOrderConfirmation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<ResendOrderConfirmationMutation, ResendOrderConfirmationMutationVariables>;
export const UpdateOrderDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateOrder"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateOrderInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateOrder"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateOrderMutation, UpdateOrderMutationVariables>;
export const CancelAndRefundOrderDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CancelAndRefundOrder"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CancelAndRefundOrderInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"cancelAndRefundOrder"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CancelAndRefundOrderMutation, CancelAndRefundOrderMutationVariables>;
export const AdminOrderDetailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminOrderDetail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phone"}},{"kind":"Field","name":{"kind":"Name","value":"canRefund"}},{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"quantity"}},{"kind":"Field","name":{"kind":"Name","value":"price"}}]}},{"kind":"Field","name":{"kind":"Name","value":"paymentStamps"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminOrderPaymentStamp"}}]}},{"kind":"Field","name":{"kind":"Name","value":"receipts"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminOrderReceipt"}}]}},{"kind":"Field","name":{"kind":"Name","value":"codes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminOrderCode"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderPaymentStamp"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedPaymentStampType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"provider"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"data"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderReceipt"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedReceiptType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderCode"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedCodeType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"literateCode"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"usedOn"}},{"kind":"Field","name":{"kind":"Name","value":"productText"}}]}}]} as unknown as DocumentNode<AdminOrderDetailQuery, AdminOrderDetailQueryVariables>;
export const OrderListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"OrderList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"searchTerm"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProductChoice"}}]}},{"kind":"Field","name":{"kind":"Name","value":"orders"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"search"},"value":{"kind":"Variable","name":{"kind":"Name","value":"searchTerm"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"OrderList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductChoice"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OrderList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}}]} as unknown as DocumentNode<OrderListQuery, OrderListQueryVariables>;
export const UpdateProductDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProduct"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateProductInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProduct"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"product"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProductMutation, UpdateProductMutationVariables>;
export const DeleteProductDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProduct"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteProductInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteProduct"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<DeleteProductMutation, DeleteProductMutationVariables>;
export const AdminProductDetailPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminProductDetailPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"productId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countTotal"}}]}},{"kind":"Field","name":{"kind":"Name","value":"product"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"productId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminProductDetail"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductOldVersion"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminProductOldVersion"}}]}}]}}]} as unknown as DocumentNode<AdminProductDetailPageQuery, AdminProductDetailPageQueryVariables>;
export const CreateProductDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProduct"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateProductInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProduct"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"product"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProductMutation, CreateProductMutationVariables>;
export const ReorderProductsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ReorderProducts"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ReorderProductsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"reorderProducts"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<ReorderProductsMutation, ReorderProductsMutationVariables>;
export const ProductListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProductList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProductList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"isAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}}]}}]} as unknown as DocumentNode<ProductListQuery, ProductListQueryVariables>;
export const UpdateProgramBasicInfoDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramBasicInfo"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateProgramInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProgram"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramBasicInfoMutation, UpdateProgramBasicInfoMutationVariables>;
export const ProgramAdminDetailQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminDetailQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"calendarExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"cachedHosts"}},{"kind":"Field","name":{"kind":"Name","value":"programOffer"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"values"}}]}},{"kind":"Field","name":{"kind":"Name","value":"links"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"href"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDetailAnnotation"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"location"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDetailAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<ProgramAdminDetailQueryQuery, ProgramAdminDetailQueryQueryVariables>;
export const ProgramAdminListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"listFilters"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isListFilter"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","alias":{"kind":"Name","value":"keyDimensions"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdmin"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdmin"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"startTime"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramAdminListQuery, ProgramAdminListQueryVariables>;
export const PutProgramDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutProgramDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutProgramDimensionMutation, PutProgramDimensionMutationVariables>;
export const DeleteProgramDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramDimensionMutation, DeleteProgramDimensionMutationVariables>;
export const PutProgramDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutProgramDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutProgramDimensionValueMutation, PutProgramDimensionValueMutationVariables>;
export const DeleteProgramDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramDimensionValueMutation, DeleteProgramDimensionValueMutationVariables>;
export const ProgramDimensionsListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramDimensionsList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionRowGroup"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ValueFields"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isInitial"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionRowGroup"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ValueFields"}}]}}]}}]} as unknown as DocumentNode<ProgramDimensionsListQuery, ProgramDimensionsListQueryVariables>;
export const UpdateProgramFormLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramFormLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateFormInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramFormLanguageMutation, UpdateProgramFormLanguageMutationVariables>;
export const DeleteProgramFormLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramFormLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramFormLanguageMutation, DeleteProgramFormLanguageMutationVariables>;
export const UpdateFormFieldsMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateFormFieldsMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateFormFieldsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateFormFields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateFormFieldsMutationMutation, UpdateFormFieldsMutationMutationVariables>;
export const EditProgramFormFieldsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditProgramFormFieldsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditProgramFormFields"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramFormFields"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormFieldsPageQuery, EditProgramFormFieldsPageQueryVariables>;
export const EditProgramFormLanguagePageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditProgramFormLanguagePage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditProgramFormLanguage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramFormLanguage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormLanguagePageQuery, EditProgramFormLanguagePageQueryVariables>;
export const CreateProgramFormLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProgramFormLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProgramFormLanguageMutation, CreateProgramFormLanguageMutationVariables>;
export const UpdateProgramFormMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramFormMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProgramForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramFormMutationMutation, UpdateProgramFormMutationMutationVariables>;
export const DeleteProrgamFormMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProrgamFormMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteProrgamFormMutationMutation, DeleteProrgamFormMutationMutationVariables>;
export const EditProgramFormPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditProgramFormPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditProgramForm"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormPageQuery, EditProgramFormPageQueryVariables>;
export const CreateProgramFormDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProgramForm"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateProgramFormInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProgramForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProgramFormMutation, CreateProgramFormMutationVariables>;
export const ProgramFormsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramFormsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"includeInactive"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"OfferForm"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OfferForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<ProgramFormsPageQuery, ProgramFormsPageQueryVariables>;
export const AcceptProgramOfferDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"AcceptProgramOffer"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"AcceptProgramOfferInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"acceptProgramOffer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<AcceptProgramOfferMutation, AcceptProgramOfferMutationVariables>;
export const ProgramOfferPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramOfferPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programOffer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDetail"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramOfferPageQuery, ProgramOfferPageQueryVariables>;
export const ProgramOffersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramOffers"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"listFilters"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isListFilter"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDimension"}}]}},{"kind":"Field","alias":{"kind":"Name","value":"keyDimensions"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDimension"}}]}},{"kind":"Field","name":{"kind":"Name","value":"stateDimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDimension"}}]}},{"kind":"Field","name":{"kind":"Name","value":"countProgramOffers"}},{"kind":"Field","name":{"kind":"Name","value":"programOffers"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOffer"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDimension"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOffer"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramOffersQuery, ProgramOffersQueryVariables>;
export const MarkScheduleItemAsFavoriteDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"MarkScheduleItemAsFavorite"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"FavoriteScheduleItemInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"markScheduleItemAsFavorite"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<MarkScheduleItemAsFavoriteMutation, MarkScheduleItemAsFavoriteMutationVariables>;
export const UnmarkScheduleItemAsFavoriteDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UnmarkScheduleItemAsFavorite"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"FavoriteScheduleItemInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"unmarkScheduleItemAsFavorite"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<UnmarkScheduleItemAsFavoriteMutation, UnmarkScheduleItemAsFavoriteMutationVariables>;
export const ProgramListQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramListQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"hidePast"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Boolean"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"hidePast"},"value":{"kind":"Variable","name":{"kind":"Name","value":"hidePast"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleItemList"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"calendarExportLink"}},{"kind":"Field","alias":{"kind":"Name","value":"listFilters"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isListFilter"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"hidePast"},"value":{"kind":"Variable","name":{"kind":"Name","value":"hidePast"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleItemList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleProgram"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleItemList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullScheduleItemType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"location"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleProgram"}}]}}]}}]} as unknown as DocumentNode<ProgramListQueryQuery, ProgramListQueryQueryVariables>;
export const CreateFeedbackDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateFeedback"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramFeedbackInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProgramFeedback"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<CreateFeedbackMutation, CreateFeedbackMutationVariables>;
export const ProgramFeedbackQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramFeedbackQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"isAcceptingFeedback"}}]}}]}}]}}]}}]} as unknown as DocumentNode<ProgramFeedbackQueryQuery, ProgramFeedbackQueryQueryVariables>;
export const ProgramDetailQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramDetailQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"calendarExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"cachedHosts"}},{"kind":"Field","name":{"kind":"Name","value":"links"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"href"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDetailAnnotation"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"location"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDetailAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<ProgramDetailQueryQuery, ProgramDetailQueryQueryVariables>;
export const UpdateQuotaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateQuota"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateQuotaInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateQuota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quota"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateQuotaMutation, UpdateQuotaMutationVariables>;
export const DeleteQuotaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteQuota"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteQuotaInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteQuota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<DeleteQuotaMutation, DeleteQuotaMutationVariables>;
export const AdminQuotaDetailPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminQuotaDetailPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"quotaId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"quotaId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","alias":{"kind":"Name","value":"quota"},"name":{"kind":"Name","value":"countTotal"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"QuotaProduct"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaProduct"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}}]}}]} as unknown as DocumentNode<AdminQuotaDetailPageQuery, AdminQuotaDetailPageQueryVariables>;
export const CreateQuotaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateQuota"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateQuotaInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createQuota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quota"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateQuotaMutation, CreateQuotaMutationVariables>;
export const QuotaListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"QuotaList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"QuotaList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullQuotaType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","alias":{"kind":"Name","value":"title"},"name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"countTotal"}}]}}]} as unknown as DocumentNode<QuotaListQuery, QuotaListQueryVariables>;
export const PutSurveyDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutSurveyDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutSurveyDimensionMutation, PutSurveyDimensionMutationVariables>;
export const DeleteSurveyDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyDimensionMutation, DeleteSurveyDimensionMutationVariables>;
export const PutSurveyDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutSurveyDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutSurveyDimensionValueMutation, PutSurveyDimensionValueMutationVariables>;
export const DeleteSurveyDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyDimensionValueMutation, DeleteSurveyDimensionValueMutationVariables>;
export const DimensionsListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"DimensionsList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionRowGroup"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ValueFields"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isInitial"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionRowGroup"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ValueFields"}}]}}]}}]} as unknown as DocumentNode<DimensionsListQuery, DimensionsListQueryVariables>;
export const UpdateFormMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateFormMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateFormInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateFormMutationMutation, UpdateFormMutationMutationVariables>;
export const DeleteSurveyLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyLanguageMutation, DeleteSurveyLanguageMutationVariables>;
export const EditSurveyFieldsPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditSurveyFieldsPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditSurveyFieldsPage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyFieldsPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditSurveyFieldsPageQueryQuery, EditSurveyFieldsPageQueryQueryVariables>;
export const EditFormLanguagePageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditFormLanguagePageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"FORMS"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditFormLanguagePage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditFormLanguagePage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditFormLanguagePageQueryQuery, EditFormLanguagePageQueryQueryVariables>;
export const CreateSurveyLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateSurveyLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]} as unknown as DocumentNode<CreateSurveyLanguageMutation, CreateSurveyLanguageMutationVariables>;
export const UpdateSurveyMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateSurveyMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateSurveyMutationMutation, UpdateSurveyMutationMutationVariables>;
export const DeleteSurveyMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyMutationMutation, DeleteSurveyMutationMutationVariables>;
export const EditSurveyPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditSurveyPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"FORMS"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditSurveyPage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"loginRequired"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"maxResponsesPerUser"}},{"kind":"Field","name":{"kind":"Name","value":"countResponsesByCurrentUser"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditSurveyPageQueryQuery, EditSurveyPageQueryQueryVariables>;
export const UpdateResponseDimensionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateResponseDimensions"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateResponseDimensionsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateResponseDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateResponseDimensionsMutation, UpdateResponseDimensionsMutationVariables>;
export const SurveyResponseDetailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyResponseDetail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"canRemoveResponses"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"response"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fields"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveyResponseDetailQuery, SurveyResponseDetailQueryVariables>;
export const SubscribeToSurveyResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"SubscribeToSurveyResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"SubscriptionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"subscribeToSurveyResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<SubscribeToSurveyResponsesMutation, SubscribeToSurveyResponsesMutationVariables>;
export const UnsubscribeFromSurveyResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UnsubscribeFromSurveyResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"SubscriptionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"unsubscribeFromSurveyResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<UnsubscribeFromSurveyResponsesMutation, UnsubscribeFromSurveyResponsesMutationVariables>;
export const DeleteSurveyResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyResponsesInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurveyResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"countDeleted"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyResponsesMutation, DeleteSurveyResponsesMutationVariables>;
export const FormResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"FormResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"relation"},"value":{"kind":"EnumValue","value":"SUBSCRIBED"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}},{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"canRemoveResponses"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"responses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"SurveyResponse"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"SurveyResponse"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"createdBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}]}]}}]} as unknown as DocumentNode<FormResponsesQuery, FormResponsesQueryVariables>;
export const SurveySummaryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveySummary"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"summary"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}]},{"kind":"Field","alias":{"kind":"Name","value":"countFilteredResponses"},"name":{"kind":"Name","value":"countResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}]},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveySummaryQuery, SurveySummaryQueryVariables>;
export const CreateSurveyDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateSurvey"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<CreateSurveyMutation, CreateSurveyMutationVariables>;
export const SurveysDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"Surveys"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"relation"},"value":{"kind":"EnumValue","value":"ACCESSIBLE"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"includeInactive"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"FORMS"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"Survey"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Survey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<SurveysQuery, SurveysQueryVariables>;
export const GenerateKeyPairDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"GenerateKeyPair"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"password"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"generateKeyPair"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"password"},"value":{"kind":"Variable","name":{"kind":"Name","value":"password"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<GenerateKeyPairMutation, GenerateKeyPairMutationVariables>;
export const RevokeKeyPairDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"RevokeKeyPair"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"id"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"revokeKeyPair"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"id"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<RevokeKeyPairMutation, RevokeKeyPairMutationVariables>;
export const ProfileEncryptionKeysDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileEncryptionKeys"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"keypairs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileEncryptionKeys"}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileEncryptionKeys"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"KeyPairType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}}]}}]} as unknown as DocumentNode<ProfileEncryptionKeysQuery, ProfileEncryptionKeysQueryVariables>;
export const ProfileOrderDetailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileOrderDetail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"canPay"}},{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"quantity"}},{"kind":"Field","name":{"kind":"Name","value":"price"}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<ProfileOrderDetailQuery, ProfileOrderDetailQueryVariables>;
export const ConfirmEmailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ConfirmEmail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ConfirmEmailInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"confirmEmail"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"email"}}]}}]}}]}}]} as unknown as DocumentNode<ConfirmEmailMutation, ConfirmEmailMutationVariables>;
export const ProfileOrdersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileOrders"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"orders"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileOrder"}}]}},{"kind":"Field","name":{"kind":"Name","value":"haveUnlinkedOrders"}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileOrder"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"canPay"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]} as unknown as DocumentNode<ProfileOrdersQuery, ProfileOrdersQueryVariables>;
export const ProfileSurveyResponsePageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileSurveyResponsePage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"anonymity"}}]}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ProfileSurveyResponsePageQuery, ProfileSurveyResponsePageQueryVariables>;
export const OwnFormResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"OwnFormResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"responses"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileResponsesTableRow"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponsesTableRow"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]} as unknown as DocumentNode<OwnFormResponsesQuery, OwnFormResponsesQueryVariables>;