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

export type AcceptInvitation = {
  __typename?: 'AcceptInvitation';
  involvement?: Maybe<LimitedInvolvementType>;
};

export type AcceptInvitationInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  invitationId: Scalars['String']['input'];
  locale: Scalars['String']['input'];
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
  Datetime = 'DATETIME',
  Number = 'NUMBER',
  String = 'STRING'
}

export type AnnotationType = {
  __typename?: 'AnnotationType';
  description: Scalars['String']['output'];
  isApplicableToProgramItems: Scalars['Boolean']['output'];
  isApplicableToScheduleItems: Scalars['Boolean']['output'];
  isComputed: Scalars['Boolean']['output'];
  isInternal: Scalars['Boolean']['output'];
  isPublic: Scalars['Boolean']['output'];
  isShownInDetail: Scalars['Boolean']['output'];
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  type: AnnotationDataType;
};


export type AnnotationTypeDescriptionArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type AnnotationTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

/** An enumeration. */
export enum Anonymity {
  FullProfile = 'FULL_PROFILE',
  Hard = 'HARD',
  NameAndEmail = 'NAME_AND_EMAIL',
  Soft = 'SOFT'
}

export type BareQuotaType = {
  __typename?: 'BareQuotaType';
  countTotal: Scalars['Int']['output'];
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
};

export type CancelAndRefundOrder = {
  __typename?: 'CancelAndRefundOrder';
  order?: Maybe<LimitedOrderType>;
};

export type CancelAndRefundOrderInput = {
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
  refundType: RefundType;
};

export type CancelOwnUnpaidOrder = {
  __typename?: 'CancelOwnUnpaidOrder';
  order?: Maybe<LimitedOrderType>;
};

export type CancelOwnUnpaidOrderInput = {
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
};

export type CancelProgram = {
  __typename?: 'CancelProgram';
  programSlug: Scalars['String']['output'];
  /** If the program item was created from a program offer, this is the offer ID. */
  responseId?: Maybe<Scalars['UUID']['output']>;
};

export type CancelProgramInput = {
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  resolution: ProgramItemResolution;
};

export type CancelProgramOffer = {
  __typename?: 'CancelProgramOffer';
  responseId: Scalars['UUID']['output'];
};

export type CancelProgramOfferInput = {
  eventSlug: Scalars['String']['input'];
  resolution: ProgramOfferResolution;
  responseId: Scalars['UUID']['input'];
};

/** An enumeration. */
export enum CodeStatus {
  BeyondLogic = 'BEYOND_LOGIC',
  ManualInterventionRequired = 'MANUAL_INTERVENTION_REQUIRED',
  Unused = 'UNUSED',
  Used = 'USED'
}

export type ColumnType = {
  __typename?: 'ColumnType';
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  totalBy: TotalBy;
  type: TypeOfColumn;
};


export type ColumnTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type ConfirmEmail = {
  __typename?: 'ConfirmEmail';
  user?: Maybe<LimitedUserType>;
};

export type ConfirmEmailInput = {
  locale: Scalars['String']['input'];
};

export type CreateOrder = {
  __typename?: 'CreateOrder';
  order?: Maybe<FullOrderType>;
};

export type CreateOrderInput = {
  customer: CustomerInput;
  eventSlug: Scalars['String']['input'];
  language?: InputMaybe<Scalars['String']['input']>;
  products: Array<OrderProductInput>;
};

export type CreateProduct = {
  __typename?: 'CreateProduct';
  product?: Maybe<LimitedProductType>;
};

export type CreateProductInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
};

export type CreateProgram = {
  __typename?: 'CreateProgram';
  program?: Maybe<FullProgramType>;
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
  purpose?: InputMaybe<SurveyPurpose>;
  surveySlug: Scalars['String']['input'];
};

export type CreateProgramInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
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
  editResponseId?: InputMaybe<Scalars['String']['input']>;
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  surveySlug: Scalars['String']['input'];
};

export type CustomerInput = {
  email: Scalars['String']['input'];
  firstName: Scalars['String']['input'];
  lastName: Scalars['String']['input'];
  phone?: InputMaybe<Scalars['String']['input']>;
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

export type DeleteInvitation = {
  __typename?: 'DeleteInvitation';
  invitation?: Maybe<LimitedInvitationType>;
};

export type DeleteInvitationInput = {
  eventSlug: Scalars['String']['input'];
  invitationId: Scalars['String']['input'];
};

export type DeleteProduct = {
  __typename?: 'DeleteProduct';
  id: Scalars['String']['output'];
};

export type DeleteProductInput = {
  eventSlug: Scalars['String']['input'];
  productId: Scalars['String']['input'];
};

export type DeleteProgramHost = {
  __typename?: 'DeleteProgramHost';
  program: FullProgramType;
};

export type DeleteProgramHostInput = {
  eventSlug: Scalars['String']['input'];
  involvementId: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
};

export type DeleteProgramOffers = {
  __typename?: 'DeleteProgramOffers';
  countDeleted: Scalars['Int']['output'];
};

export type DeleteProgramOffersInput = {
  eventSlug: Scalars['String']['input'];
  programOfferIds?: InputMaybe<Array<InputMaybe<Scalars['String']['input']>>>;
};

export type DeleteQuota = {
  __typename?: 'DeleteQuota';
  id: Scalars['String']['output'];
};

export type DeleteQuotaInput = {
  eventSlug: Scalars['String']['input'];
  quotaId: Scalars['String']['input'];
};

export type DeleteScheduleItem = {
  __typename?: 'DeleteScheduleItem';
  slug?: Maybe<Scalars['String']['output']>;
};

export type DeleteScheduleItemInput = {
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  scheduleItemSlug: Scalars['String']['input'];
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

/** An enumeration. */
export enum DimensionApp {
  Forms = 'FORMS',
  Involvement = 'INVOLVEMENT',
  ProgramV2 = 'PROGRAM_V2'
}

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
  canEdit: Scalars['Boolean']['output'];
  canRemove: Scalars['Boolean']['output'];
  color: Scalars['String']['output'];
  /** If set, subjects this value is assigned to can no longer be edited by whomever submitted them. */
  isSubjectLocked: Scalars['Boolean']['output'];
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

/** An enumeration. */
export enum EditMode {
  Admin = 'ADMIN',
  Owner = 'OWNER'
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
  survey: FullSurveyType;
  thankYouMessage: Scalars['String']['output'];
  title: Scalars['String']['output'];
};


export type FormTypeFieldsArgs = {
  enrich?: InputMaybe<Scalars['Boolean']['input']>;
};

export type FormsEventMetaType = {
  __typename?: 'FormsEventMetaType';
  survey?: Maybe<FullSurveyType>;
  surveys: Array<FullSurveyType>;
};


export type FormsEventMetaTypeSurveyArgs = {
  app?: InputMaybe<DimensionApp>;
  purpose?: InputMaybe<SurveyPurpose>;
  slug: Scalars['String']['input'];
};


export type FormsEventMetaTypeSurveysArgs = {
  app: DimensionApp;
  includeInactive?: InputMaybe<Scalars['Boolean']['input']>;
  purpose?: InputMaybe<Array<SurveyPurpose>>;
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
  canAddValues: Scalars['Boolean']['output'];
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
  involvement?: Maybe<InvolvementEventMetaType>;
  name: Scalars['String']['output'];
  program?: Maybe<ProgramV2EventMetaType>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  startTime?: Maybe<Scalars['DateTime']['output']>;
  tickets?: Maybe<TicketsV2EventMetaType>;
  timezone: Scalars['String']['output'];
  timezoneName: Scalars['String']['output'];
};

export type FullInvitationType = {
  __typename?: 'FullInvitationType';
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  createdBy?: Maybe<LimitedUserType>;
  email: Scalars['String']['output'];
  id: Scalars['UUID']['output'];
  isUsed: Scalars['Boolean']['output'];
  /** The language of the invitation. This is used to send the invitation in the correct language. */
  language: InvolvementInvitationLanguageChoices;
  program?: Maybe<LimitedProgramType>;
  survey?: Maybe<FullSurveyType>;
  usedAt?: Maybe<Scalars['DateTime']['output']>;
};

export type FullOrderType = {
  __typename?: 'FullOrderType';
  /** Returns whether the order can be marked as paid. */
  canMarkAsPaid: Scalars['Boolean']['output'];
  canPay: Scalars['Boolean']['output'];
  /** Returns whether a provider refund can be initiated for this order. */
  canRefund: Scalars['Boolean']['output'];
  /** Returns whether the order can be refunded manually. */
  canRefundManually: Scalars['Boolean']['output'];
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
  id: Scalars['Int']['output'];
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

/**
 * Represents a Program Host with access to Person and all their Programs in an Event.
 * This is different from Involvement in that an Involvement is related to a single Program
 * whereas FullProgramHostType groups all Programs for a Person in an Event.
 */
export type FullProgramHostType = {
  __typename?: 'FullProgramHostType';
  person: LimitedProfileType;
  programs: Array<LimitedProgramType>;
};

export type FullProgramType = {
  __typename?: 'FullProgramType';
  /** Program annotation values with schema attached to them. Only public annotations are returned. NOTE: If querying a lot of program items, consider using cachedAnnotations instead for SPEED. */
  annotations: Array<ProgramAnnotationType>;
  /** A mapping of program annotation slug to annotation value. */
  cachedAnnotations: Scalars['GenericScalar']['output'];
  /** Returns a mapping of dimension slugs to lists of value slugs. Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries. The difference is negligible for a single program or schedule item, but when using the plural resolvers like `programs` or `scheduleItems`, the performance difference can be significant. By default, returns both dimensions set on the program itself and those set on its schedule items. If `own_only` is True, only returns dimensions set on this item itself. By default, returns both public and internal dimensions. This will change in near future to only return public dimensions by default and require `publicOnly: false` to get internal dimensions. At that time, the default will change to `publicOnly: true`, and setting `publicOnly: false` will require authentication. To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`). To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`). */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** The earliest start time of any schedule item of this program. NOTE: This is not the same as the program's start time. The intended purpose of this field is to exclude programs that have not yet started. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedEarliestStartTime?: Maybe<Scalars['DateTime']['output']>;
  cachedHosts: Scalars['String']['output'];
  /** The latest end time of any schedule item of this program. NOTE: This is not the same as the program's start end. The intended purpose of this field is to exclude programs that have already ended. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedLatestEndTime?: Maybe<Scalars['DateTime']['output']>;
  canCancel: Scalars['Boolean']['output'];
  canDelete: Scalars['Boolean']['output'];
  canInviteProgramHost: Scalars['Boolean']['output'];
  canRestore: Scalars['Boolean']['output'];
  color: Scalars['String']['output'];
  createdAt: Scalars['DateTime']['output'];
  description: Scalars['String']['output'];
  /** `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  dimensions: Array<ProgramDimensionValueType>;
  event: LimitedEventType;
  invitations: Array<LimitedInvitationType>;
  isAcceptingFeedback: Scalars['Boolean']['output'];
  isCancelled: Scalars['Boolean']['output'];
  /** Get the links associated with the program. If types are not specified, all links are returned. */
  links: Array<ProgramLink>;
  /** Deprecated. Use `scheduleItem.location` instead. */
  location?: Maybe<Scalars['String']['output']>;
  programHosts: Array<LimitedProgramHostType>;
  programOffer?: Maybe<LimitedResponseType>;
  scheduleItems: Array<LimitedScheduleItemType>;
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type FullProgramTypeAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullProgramTypeCachedAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
  slug?: InputMaybe<Array<Scalars['String']['input']>>;
};


export type FullProgramTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  listFiltersOnly?: InputMaybe<Scalars['Boolean']['input']>;
  ownOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullProgramTypeDimensionsArgs = {
  isListFilter?: InputMaybe<Scalars['Boolean']['input']>;
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullProgramTypeLinksArgs = {
  includeExpired?: InputMaybe<Scalars['Boolean']['input']>;
  lang?: InputMaybe<Scalars['String']['input']>;
  types?: InputMaybe<Array<InputMaybe<ProgramLinkType>>>;
};


export type FullProgramTypeLocationArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type FullProgramTypeProgramHostsArgs = {
  includeInactive?: InputMaybe<Scalars['Boolean']['input']>;
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
  /** Returns a mapping of dimension slugs to lists of value slugs. Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries. The difference is negligible for a response, but when operating on the plural resolver `responses`, the performance difference can be significant. By default, returns only public dimensions. If `publicOnly` is set to `false`, both public and internal dimensions will be returned. In this case, authentication is required. To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`). To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`). */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** Returns whether the response can be accepted by the user as an administrator. Not all survey workflows have the notion of accepting a response, in which case this field will always return False. */
  canAccept: Scalars['Boolean']['output'];
  /** Returns whether the response can be cancelled by the user. Not all survey workflows have the notion of cancelling a response, in which case this field will always return False. */
  canCancel: Scalars['Boolean']['output'];
  /** Whether the response can be deleted by the user. */
  canDelete: Scalars['Boolean']['output'];
  /** Returns whether the response can be edited by the user in the given edit mode. The edit mode can be either ADMIN (default) or OWN. ADMIN determines CBAC edit permissions, while OWN determines if the user is the owner of the response and editing it is allowed by the survey. */
  canEdit: Scalars['Boolean']['output'];
  dimensions: Array<ResponseDimensionValueType>;
  form: FormType;
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
  /** Language code of the form used to submit this response. */
  language: Scalars['String']['output'];
  oldVersions: Array<LimitedResponseType>;
  /** The date and time when the response was originally created. */
  originalCreatedAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who originally submitted this response.
   * If response is to an anonymous survey, this information will not be available.
   *
   */
  originalCreatedBy?: Maybe<SelectedProfileType>;
  /** For program offers, returns a list of programs created from the offer. For program host invitation form responses, returns a list containing the program the host was invited to. For forms managed by an app other than Program V2, returns an empty list. */
  programs: Array<LimitedProgramType>;
  revisionCreatedAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who submitted this version of the response.
   * If response is to an anonymous survey, this information will not be available.
   *
   */
  revisionCreatedBy?: Maybe<SelectedProfileType>;
  /** Sequence number of this response within the use case (eg. survey). */
  sequenceNumber: Scalars['Int']['output'];
  supersededBy?: Maybe<LimitedResponseType>;
  values?: Maybe<Scalars['GenericScalar']['output']>;
};


export type FullResponseTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  listFiltersOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullResponseTypeCanEditArgs = {
  mode?: InputMaybe<EditMode>;
};


export type FullResponseTypeDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type FullResponseTypeValuesArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};

export type FullScheduleItemType = {
  __typename?: 'FullScheduleItemType';
  /** A mapping of program annotation slug to annotation value. */
  cachedAnnotations: Scalars['GenericScalar']['output'];
  /** Returns a mapping of dimension slugs to lists of value slugs. Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries. The difference is negligible for a single program or schedule item, but when using the plural resolvers like `programs` or `scheduleItems`, the performance difference can be significant. By default, returns both dimensions set on the program itself and those set on its schedule items. If `own_only` is True, only returns dimensions set on this item itself. By default, returns both public and internal dimensions. This will change in near future to only return public dimensions by default and require `publicOnly: false` to get internal dimensions. At that time, the default will change to `publicOnly: true`, and setting `publicOnly: false` will require authentication. To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`). To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`). */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  durationMinutes: Scalars['Int']['output'];
  endTime: Scalars['DateTime']['output'];
  endTimeUnixSeconds: Scalars['Int']['output'];
  /** Convenience helper to get the freeform location of the schedule item. NOTE: You should usually display `location` to users instead. */
  freeformLocation: Scalars['String']['output'];
  isCancelled: Scalars['Boolean']['output'];
  /** Deprecated alias for `duration_minutes`. */
  lengthMinutes: Scalars['Int']['output'];
  location?: Maybe<Scalars['String']['output']>;
  program: LimitedProgramType;
  reservationsExcelExportLink: Scalars['String']['output'];
  /** Convenience helper to get the value slug of the `room` dimension. NOTE: You should usually display `location` to users instead. */
  room: Scalars['String']['output'];
  /** NOTE: Slug must be unique within Event. It does not suffice to be unique within Program. */
  slug: Scalars['String']['output'];
  startTime: Scalars['DateTime']['output'];
  startTimeUnixSeconds: Scalars['Int']['output'];
  /** Convenience helper to get the subtitle of the schedule item. NOTE: You should usually display `title` to users instead. */
  subtitle: Scalars['String']['output'];
  /** Returns the title of the program, with subtitle if it exists, in the format "Program title – Schedule item subtitle". */
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type FullScheduleItemTypeCachedAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
  slug?: InputMaybe<Array<Scalars['String']['input']>>;
};


export type FullScheduleItemTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  listFiltersOnly?: InputMaybe<Scalars['Boolean']['input']>;
  ownOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
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
  /** Default dimension values that will be set on involvements based on responses. */
  cachedDefaultInvolvementDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** Default dimension values that will be set on new responses. */
  cachedDefaultResponseDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** Surveys that have language versions cannot be removed. Having language versions is also a prerequisite for a survey to have responses. */
  canRemove: Scalars['Boolean']['output'];
  /** Checks that the user has permission to remove responses to this survey. This requires proper CBAC permission and that `survey.protect_responses` is false. */
  canRemoveResponses: Scalars['Boolean']['output'];
  /** Returns the number of responses to this survey regardless of language version used. Authorization required. */
  countResponses: Scalars['Int']['output'];
  /** Returns the number of responses to this survey by the current user. */
  countResponsesByCurrentUser: Scalars['Int']['output'];
  /** `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  dimensions: Array<FullDimensionType>;
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
  profileFieldSelector: ProfileFieldSelectorType;
  /** If enabled, responses cannot be deleted from the UI without disabling this first. */
  protectResponses: Scalars['Boolean']['output'];
  purpose: SurveyPurpose;
  registry?: Maybe<LimitedRegistryType>;
  response?: Maybe<FullResponseType>;
  /** Returns the responses to this survey regardless of language version used. Authorization required. */
  responses?: Maybe<Array<LimitedResponseType>>;
  /** If set, responses to this survey can be edited by whomever sent them until this date, provided that the response is not locked by a dimension value that is set to lock subjects. If unset, responses cannnot be edited at all.  */
  responsesEditableUntil?: Maybe<Scalars['DateTime']['output']>;
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
  isListFilter?: InputMaybe<Scalars['Boolean']['input']>;
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
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

export type InviteProgramHost = {
  __typename?: 'InviteProgramHost';
  invitation: FullInvitationType;
};

export type InviteProgramHostInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  programSlug: Scalars['String']['input'];
};

/** An enumeration. */
export enum InvolvementApp {
  Forms = 'FORMS',
  Involvement = 'INVOLVEMENT',
  Program = 'PROGRAM',
  Volunteers = 'VOLUNTEERS'
}

export type InvolvementEventMetaType = {
  __typename?: 'InvolvementEventMetaType';
  annotations: Array<AnnotationType>;
  defaultRegistry?: Maybe<LimitedRegistryType>;
  /** `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  dimensions: Array<FullDimensionType>;
  event: FullEventType;
  id: Scalars['ID']['output'];
  invitation?: Maybe<FullInvitationType>;
  /** List of people involved in the event, filtered by dimensions. */
  people: Array<ProfileWithInvolvementType>;
  person?: Maybe<ProfileWithInvolvementType>;
  reports: Array<ReportType>;
};


export type InvolvementEventMetaTypeAnnotationsArgs = {
  perksOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type InvolvementEventMetaTypeDimensionsArgs = {
  isListFilter?: InputMaybe<Scalars['Boolean']['input']>;
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type InvolvementEventMetaTypeInvitationArgs = {
  invitationId: Scalars['String']['input'];
};


export type InvolvementEventMetaTypePeopleArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  returnNone?: InputMaybe<Scalars['Boolean']['input']>;
  search?: InputMaybe<Scalars['String']['input']>;
};


export type InvolvementEventMetaTypePersonArgs = {
  id: Scalars['Int']['input'];
};


export type InvolvementEventMetaTypeReportsArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

/** An enumeration. */
export enum InvolvementInvitationLanguageChoices {
  /** English */
  En = 'EN',
  /** Finnish */
  Fi = 'FI',
  /** Swedish */
  Sv = 'SV'
}

/** An enumeration. */
export enum InvolvementType {
  CombinedPerks = 'COMBINED_PERKS',
  LegacySignup = 'LEGACY_SIGNUP',
  ProgramHost = 'PROGRAM_HOST',
  ProgramOffer = 'PROGRAM_OFFER',
  SurveyResponse = 'SURVEY_RESPONSE'
}

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
  endTime?: Maybe<Scalars['DateTime']['output']>;
  name: Scalars['String']['output'];
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  startTime?: Maybe<Scalars['DateTime']['output']>;
  timezone: Scalars['String']['output'];
};

export type LimitedInvitationType = {
  __typename?: 'LimitedInvitationType';
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  email: Scalars['String']['output'];
  id: Scalars['UUID']['output'];
  isUsed: Scalars['Boolean']['output'];
  /** The language of the invitation. This is used to send the invitation in the correct language. */
  language: InvolvementInvitationLanguageChoices;
  survey?: Maybe<LimitedSurveyType>;
};

/** Represent Involvement (and the Person involved) without a way to traverse back to Person. */
export type LimitedInvolvementType = {
  __typename?: 'LimitedInvolvementType';
  adminLink?: Maybe<Scalars['String']['output']>;
  app: InvolvementApp;
  cachedAnnotations: Scalars['GenericScalar']['output'];
  cachedDimensions: Scalars['GenericScalar']['output'];
  createdAt: Scalars['DateTime']['output'];
  id: Scalars['ID']['output'];
  isActive: Scalars['Boolean']['output'];
  program?: Maybe<LimitedProgramType>;
  programOffer?: Maybe<LimitedResponseType>;
  response?: Maybe<LimitedResponseType>;
  title: Scalars['String']['output'];
  type: InvolvementType;
  updatedAt: Scalars['DateTime']['output'];
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

export type LimitedOrganizationType = {
  __typename?: 'LimitedOrganizationType';
  name: Scalars['String']['output'];
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  timezone: Scalars['String']['output'];
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
  id: Scalars['Int']['output'];
  maxPerOrder: Scalars['Int']['output'];
  price: Scalars['Decimal']['output'];
  quotas: Array<Maybe<BareQuotaType>>;
  title: Scalars['String']['output'];
};

/** Represent Person without a way to traverse back to Event. */
export type LimitedProfileType = {
  __typename?: 'LimitedProfileType';
  /** Your Discord username (NOTE: not display name). Events may use this to give you roles based on your participation. */
  discordHandle: Scalars['String']['output'];
  displayName: Scalars['String']['output'];
  /** Email is the primary means of contact for event-related matters. */
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  fullName: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  lastName: Scalars['String']['output'];
  /** If you go by a nick name or handle that you want printed in your badge and programme details, enter it here. */
  nick: Scalars['String']['output'];
  phoneNumber: Scalars['String']['output'];
};

export type LimitedProgramHostType = {
  __typename?: 'LimitedProgramHostType';
  cachedDimensions: Scalars['GenericScalar']['output'];
  createdAt: Scalars['DateTime']['output'];
  id: Scalars['ID']['output'];
  isActive: Scalars['Boolean']['output'];
  person: LimitedProfileType;
  programHostRole?: Maybe<ProgramHostRole>;
  updatedAt: Scalars['DateTime']['output'];
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
  /** A mapping of program annotation slug to annotation value. */
  cachedAnnotations: Scalars['GenericScalar']['output'];
  /** Returns a mapping of dimension slugs to lists of value slugs. Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries. The difference is negligible for a single program or schedule item, but when using the plural resolvers like `programs` or `scheduleItems`, the performance difference can be significant. By default, returns both dimensions set on the program itself and those set on its schedule items. If `own_only` is True, only returns dimensions set on this item itself. By default, returns both public and internal dimensions. This will change in near future to only return public dimensions by default and require `publicOnly: false` to get internal dimensions. At that time, the default will change to `publicOnly: true`, and setting `publicOnly: false` will require authentication. To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`). To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`). */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** The earliest start time of any schedule item of this program. NOTE: This is not the same as the program's start time. The intended purpose of this field is to exclude programs that have not yet started. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedEarliestStartTime?: Maybe<Scalars['DateTime']['output']>;
  cachedHosts: Scalars['String']['output'];
  /** The latest end time of any schedule item of this program. NOTE: This is not the same as the program's start end. The intended purpose of this field is to exclude programs that have already ended. Always use `scheduleItems` for the purpose of displaying program times. */
  cachedLatestEndTime?: Maybe<Scalars['DateTime']['output']>;
  canCancel: Scalars['Boolean']['output'];
  canDelete: Scalars['Boolean']['output'];
  canInviteProgramHost: Scalars['Boolean']['output'];
  canRestore: Scalars['Boolean']['output'];
  color: Scalars['String']['output'];
  createdAt: Scalars['DateTime']['output'];
  description: Scalars['String']['output'];
  isAcceptingFeedback: Scalars['Boolean']['output'];
  isCancelled: Scalars['Boolean']['output'];
  /** Get the links associated with the program. If types are not specified, all links are returned. */
  links: Array<ProgramLink>;
  /** Deprecated. Use `scheduleItem.location` instead. */
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
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
  slug?: InputMaybe<Array<Scalars['String']['input']>>;
};


/**
 * "Limited" program items are returned when queried through ScheduleItem.program so as to
 * limit DoS via deep nesting. It lacks access to `scheduleItems` which might be used to
 * cause a rapid expansion of the response via deep nesting, and also lacks access to
 * some fields that may be expensive to compute such as `dimensions`; however,
 * `cachedDimensions` is still provided.
 */
export type LimitedProgramTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  listFiltersOnly?: InputMaybe<Scalars['Boolean']['input']>;
  ownOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
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

export type LimitedRegistryType = {
  __typename?: 'LimitedRegistryType';
  createdAt: Scalars['DateTime']['output'];
  organization: LimitedOrganizationType;
  policyUrl: Scalars['String']['output'];
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type LimitedRegistryTypePolicyUrlArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type LimitedRegistryTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type LimitedResponseType = {
  __typename?: 'LimitedResponseType';
  /** Returns a mapping of dimension slugs to lists of value slugs. Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries. The difference is negligible for a response, but when operating on the plural resolver `responses`, the performance difference can be significant. By default, returns only public dimensions. If `publicOnly` is set to `false`, both public and internal dimensions will be returned. In this case, authentication is required. To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`). To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`). */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** Returns whether the response can be accepted by the user as an administrator. Not all survey workflows have the notion of accepting a response, in which case this field will always return False. */
  canAccept: Scalars['Boolean']['output'];
  /** Returns whether the response can be cancelled by the user. Not all survey workflows have the notion of cancelling a response, in which case this field will always return False. */
  canCancel: Scalars['Boolean']['output'];
  /** Whether the response can be deleted by the user. */
  canDelete: Scalars['Boolean']['output'];
  /** Returns whether the response can be edited by the user in the given edit mode. The edit mode can be either ADMIN (default) or OWN. ADMIN determines CBAC edit permissions, while OWN determines if the user is the owner of the response and editing it is allowed by the survey. */
  canEdit: Scalars['Boolean']['output'];
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
  /** Language code of the form used to submit this response. */
  language: Scalars['String']['output'];
  /** The date and time when the response was originally created. */
  originalCreatedAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who originally submitted this response.
   * If response is to an anonymous survey, this information will not be available.
   *
   */
  originalCreatedBy?: Maybe<SelectedProfileType>;
  /** For program offers, returns a list of programs created from the offer. For program host invitation form responses, returns a list containing the program the host was invited to. For forms managed by an app other than Program V2, returns an empty list. */
  programs: Array<LimitedProgramType>;
  revisionCreatedAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who submitted this version of the response.
   * If response is to an anonymous survey, this information will not be available.
   *
   */
  revisionCreatedBy?: Maybe<SelectedProfileType>;
  /** Sequence number of this response within the use case (eg. survey). */
  sequenceNumber: Scalars['Int']['output'];
  values?: Maybe<Scalars['GenericScalar']['output']>;
};


export type LimitedResponseTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  listFiltersOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type LimitedResponseTypeCanEditArgs = {
  mode?: InputMaybe<EditMode>;
};


export type LimitedResponseTypeValuesArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};

export type LimitedScheduleItemType = {
  __typename?: 'LimitedScheduleItemType';
  /** A mapping of program annotation slug to annotation value. */
  cachedAnnotations: Scalars['GenericScalar']['output'];
  /** Returns a mapping of dimension slugs to lists of value slugs. Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries. The difference is negligible for a single program or schedule item, but when using the plural resolvers like `programs` or `scheduleItems`, the performance difference can be significant. By default, returns both dimensions set on the program itself and those set on its schedule items. If `own_only` is True, only returns dimensions set on this item itself. By default, returns both public and internal dimensions. This will change in near future to only return public dimensions by default and require `publicOnly: false` to get internal dimensions. At that time, the default will change to `publicOnly: true`, and setting `publicOnly: false` will require authentication. To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`). To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`). */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  createdAt: Scalars['DateTime']['output'];
  durationMinutes: Scalars['Int']['output'];
  endTime: Scalars['DateTime']['output'];
  endTimeUnixSeconds: Scalars['Int']['output'];
  /** Convenience helper to get the freeform location of the schedule item. NOTE: You should usually display `location` to users instead. */
  freeformLocation: Scalars['String']['output'];
  isCancelled: Scalars['Boolean']['output'];
  isPublic: Scalars['Boolean']['output'];
  /** Deprecated alias for `duration_minutes`. */
  lengthMinutes: Scalars['Int']['output'];
  location?: Maybe<Scalars['String']['output']>;
  reservationsExcelExportLink: Scalars['String']['output'];
  /** Convenience helper to get the value slug of the `room` dimension. NOTE: You should usually display `location` to users instead. */
  room: Scalars['String']['output'];
  /** NOTE: Slug must be unique within Event. It does not suffice to be unique within Program. */
  slug: Scalars['String']['output'];
  startTime: Scalars['DateTime']['output'];
  startTimeUnixSeconds: Scalars['Int']['output'];
  /** Convenience helper to get the subtitle of the schedule item. NOTE: You should usually display `title` to users instead. */
  subtitle: Scalars['String']['output'];
  /** Returns the title of the program, with subtitle if it exists, in the format "Program title – Schedule item subtitle". */
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};


export type LimitedScheduleItemTypeCachedAnnotationsArgs = {
  isShownInDetail?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
  slug?: InputMaybe<Array<Scalars['String']['input']>>;
};


export type LimitedScheduleItemTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
  listFiltersOnly?: InputMaybe<Scalars['Boolean']['input']>;
  ownOnly?: InputMaybe<Scalars['Boolean']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
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
  /** Default dimension values that will be set on involvements based on responses. */
  cachedDefaultInvolvementDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** Default dimension values that will be set on new responses. */
  cachedDefaultResponseDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  isActive: Scalars['Boolean']['output'];
  loginRequired: Scalars['Boolean']['output'];
  /** Maximum number of responses per user. 0 = unlimited. Note that if login_required is not set, this only takes effect for logged in users.Has no effect if the survey is hard anonymous. */
  maxResponsesPerUser: Scalars['Int']['output'];
  profileFieldSelector: ProfileFieldSelectorType;
  /** If enabled, responses cannot be deleted from the UI without disabling this first. */
  protectResponses: Scalars['Boolean']['output'];
  purpose: SurveyPurpose;
  registry?: Maybe<LimitedRegistryType>;
  /** If set, responses to this survey can be edited by whomever sent them until this date, provided that the response is not locked by a dimension value that is set to lock subjects. If unset, responses cannnot be edited at all.  */
  responsesEditableUntil?: Maybe<Scalars['DateTime']['output']>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  title?: Maybe<Scalars['String']['output']>;
};


export type LimitedSurveyTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type LimitedUniverseAnnotationType = {
  __typename?: 'LimitedUniverseAnnotationType';
  annotation: AnnotationType;
  formFields?: Maybe<Scalars['GenericScalar']['output']>;
  isActive: Scalars['Boolean']['output'];
};

/** Deprecated. Use ProfileType instead. */
export type LimitedUserType = {
  __typename?: 'LimitedUserType';
  /** User's full name. */
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  lastName: Scalars['String']['output'];
};

export type MarkOrderAsPaid = {
  __typename?: 'MarkOrderAsPaid';
  order?: Maybe<LimitedOrderType>;
};

export type MarkOrderAsPaidInput = {
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
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
  acceptInvitation?: Maybe<AcceptInvitation>;
  acceptProgramOffer?: Maybe<AcceptProgramOffer>;
  cancelAndRefundOrder?: Maybe<CancelAndRefundOrder>;
  cancelOwnUnpaidOrder?: Maybe<CancelOwnUnpaidOrder>;
  cancelProgram?: Maybe<CancelProgram>;
  cancelProgramOffer?: Maybe<CancelProgramOffer>;
  confirmEmail?: Maybe<ConfirmEmail>;
  createOrder?: Maybe<CreateOrder>;
  createProduct?: Maybe<CreateProduct>;
  createProgram?: Maybe<CreateProgram>;
  createProgramFeedback?: Maybe<CreateProgramFeedback>;
  createProgramForm?: Maybe<CreateProgramForm>;
  createQuota?: Maybe<CreateQuota>;
  createSurvey?: Maybe<CreateSurvey>;
  createSurveyLanguage?: Maybe<CreateSurveyLanguage>;
  createSurveyResponse?: Maybe<CreateSurveyResponse>;
  deleteDimension?: Maybe<DeleteDimension>;
  deleteDimensionValue?: Maybe<DeleteDimensionValue>;
  deleteInvitation?: Maybe<DeleteInvitation>;
  deleteProduct?: Maybe<DeleteProduct>;
  deleteProgramHost?: Maybe<DeleteProgramHost>;
  deleteProgramOffers?: Maybe<DeleteProgramOffers>;
  deleteQuota?: Maybe<DeleteQuota>;
  deleteScheduleItem?: Maybe<DeleteScheduleItem>;
  deleteSurvey?: Maybe<DeleteSurvey>;
  deleteSurveyLanguage?: Maybe<DeleteSurveyLanguage>;
  deleteSurveyResponses?: Maybe<DeleteSurveyResponses>;
  generateKeyPair?: Maybe<GenerateKeyPair>;
  initFileUpload?: Maybe<InitFileUploadResponse>;
  inviteProgramHost?: Maybe<InviteProgramHost>;
  markOrderAsPaid?: Maybe<MarkOrderAsPaid>;
  /** Deprecated. Use MarkScheduleItemAsFavorite instead. */
  markProgramAsFavorite?: Maybe<MarkProgramAsFavorite>;
  markScheduleItemAsFavorite?: Maybe<MarkScheduleItemAsFavorite>;
  /**
   * Promotes a Single Select or Multiple Select field to a dimension.
   *
   * This is used when a field is created as a Single Select or Multiple Select
   * and later discovered that it should be a dimension.
   */
  promoteFieldToDimension?: Maybe<PromoteFieldToDimension>;
  putDimension?: Maybe<PutDimension>;
  putDimensionValue?: Maybe<PutDimensionValue>;
  putScheduleItem?: Maybe<PutScheduleItem>;
  putUniverseAnnotation?: Maybe<PutUniverseAnnotation>;
  reorderProducts?: Maybe<ReorderProducts>;
  resendInvitation?: Maybe<ResendInvitation>;
  resendOrderConfirmation?: Maybe<ResendOrderConfirmation>;
  /** Restore a program item that was previously cancelled. */
  restoreProgram?: Maybe<RestoreProgram>;
  revokeKeyPair?: Maybe<RevokeKeyPair>;
  subscribeToSurveyResponses?: Maybe<SubscribeToSurveyResponses>;
  /** Deprecated. Use UnmarkScheduleItemAsFavorite instead. */
  unmarkProgramAsFavorite?: Maybe<UnmarkProgramAsFavorite>;
  unmarkScheduleItemAsFavorite?: Maybe<UnmarkScheduleItemAsFavorite>;
  unsubscribeFromSurveyResponses?: Maybe<UnsubscribeFromSurveyResponses>;
  updateForm?: Maybe<UpdateForm>;
  updateFormFields?: Maybe<UpdateFormFields>;
  updateInvolvementDimensions?: Maybe<UpdateInvolvementDimensions>;
  updateOrder?: Maybe<UpdateOrder>;
  updateProduct?: Maybe<UpdateProduct>;
  updateProgram?: Maybe<UpdateProgram>;
  updateProgramAnnotations?: Maybe<UpdateProgramAnnotations>;
  updateProgramDimensions?: Maybe<UpdateProgramDimensions>;
  updateProgramForm?: Maybe<UpdateProgramForm>;
  updateQuota?: Maybe<UpdateQuota>;
  updateResponseDimensions?: Maybe<UpdateResponseDimensions>;
  updateSurvey?: Maybe<UpdateSurvey>;
  updateSurveyDefaultDimensions?: Maybe<UpdateSurveyDefaultDimensions>;
};


export type MutationAcceptInvitationArgs = {
  input: AcceptInvitationInput;
};


export type MutationAcceptProgramOfferArgs = {
  input: AcceptProgramOfferInput;
};


export type MutationCancelAndRefundOrderArgs = {
  input: CancelAndRefundOrderInput;
};


export type MutationCancelOwnUnpaidOrderArgs = {
  input: CancelOwnUnpaidOrderInput;
};


export type MutationCancelProgramArgs = {
  input: CancelProgramInput;
};


export type MutationCancelProgramOfferArgs = {
  input: CancelProgramOfferInput;
};


export type MutationConfirmEmailArgs = {
  input: ConfirmEmailInput;
};


export type MutationCreateOrderArgs = {
  input: CreateOrderInput;
};


export type MutationCreateProductArgs = {
  input: CreateProductInput;
};


export type MutationCreateProgramArgs = {
  input: CreateProgramInput;
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


export type MutationDeleteInvitationArgs = {
  input: DeleteInvitationInput;
};


export type MutationDeleteProductArgs = {
  input: DeleteProductInput;
};


export type MutationDeleteProgramHostArgs = {
  input: DeleteProgramHostInput;
};


export type MutationDeleteProgramOffersArgs = {
  input: DeleteProgramOffersInput;
};


export type MutationDeleteQuotaArgs = {
  input: DeleteQuotaInput;
};


export type MutationDeleteScheduleItemArgs = {
  input: DeleteScheduleItemInput;
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


export type MutationInviteProgramHostArgs = {
  input: InviteProgramHostInput;
};


export type MutationMarkOrderAsPaidArgs = {
  input: MarkOrderAsPaidInput;
};


export type MutationMarkProgramAsFavoriteArgs = {
  input: FavoriteInput;
};


export type MutationMarkScheduleItemAsFavoriteArgs = {
  input: FavoriteScheduleItemInput;
};


export type MutationPromoteFieldToDimensionArgs = {
  input: PromoteFieldToDimensionInput;
};


export type MutationPutDimensionArgs = {
  input: PutDimensionInput;
};


export type MutationPutDimensionValueArgs = {
  input: PutDimensionValueInput;
};


export type MutationPutScheduleItemArgs = {
  input: PutScheduleItemInput;
};


export type MutationPutUniverseAnnotationArgs = {
  input: PutUniverseAnnotationInput;
};


export type MutationReorderProductsArgs = {
  input: ReorderProductsInput;
};


export type MutationResendInvitationArgs = {
  input: ResendInvitationInput;
};


export type MutationResendOrderConfirmationArgs = {
  input: ResendOrderConfirmationInput;
};


export type MutationRestoreProgramArgs = {
  input: RestoreProgramInput;
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


export type MutationUpdateInvolvementDimensionsArgs = {
  input: UpdateInvolvementDimensionsInput;
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


export type MutationUpdateProgramAnnotationsArgs = {
  input: UpdateProgramAnnotationsInput;
};


export type MutationUpdateProgramDimensionsArgs = {
  input: UpdateProgramDimensionsInput;
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


export type MutationUpdateSurveyDefaultDimensionsArgs = {
  input: UpdateSurveyDefaultDimensionsInput;
};

export type OrderProductInput = {
  productId: Scalars['Int']['input'];
  quantity: Scalars['Int']['input'];
};

export type OrderProductType = {
  __typename?: 'OrderProductType';
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Int']['output'];
  title: Scalars['String']['output'];
};

export type OwnProfileType = {
  __typename?: 'OwnProfileType';
  /** Your Discord username (NOTE: not display name). Events may use this to give you roles based on your participation. */
  discordHandle: Scalars['String']['output'];
  displayName: Scalars['String']['output'];
  /** Email is the primary means of contact for event-related matters. */
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  /** Namespace for queries related to forms and the current user. */
  forms: FormsProfileMetaType;
  fullName: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  keypairs?: Maybe<Array<KeyPairType>>;
  lastName: Scalars['String']['output'];
  /** If you go by a nick name or handle that you want printed in your badge and programme details, enter it here. */
  nick: Scalars['String']['output'];
  phoneNumber: Scalars['String']['output'];
  /** Namespace for queries related to programs and the current user. */
  program: ProgramV2ProfileMetaType;
  /** Namespace for queries related to tickets and the current user. */
  tickets: TicketsV2ProfileMetaType;
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

/**
 * Used to determine which profile fields are transferred from registry to another.
 * NOTE: Must match ProfileFieldSelector in frontend/src/components/involvement/models.ts.
 *
 * For "no fields selected", use the default constructor.
 * For "all fields selected", use `ProfileFieldSelector.all_fields()`.
 */
export type ProfileFieldSelectorType = {
  __typename?: 'ProfileFieldSelectorType';
  discordHandle: Scalars['Boolean']['output'];
  email: Scalars['Boolean']['output'];
  firstName: Scalars['Boolean']['output'];
  id: Scalars['Boolean']['output'];
  lastName: Scalars['Boolean']['output'];
  nick: Scalars['Boolean']['output'];
  phoneNumber: Scalars['Boolean']['output'];
};

export type ProfileOrderType = {
  __typename?: 'ProfileOrderType';
  canCancel: Scalars['Boolean']['output'];
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

export type ProfileResponseType = {
  __typename?: 'ProfileResponseType';
  /** Returns the dimensions of the response as a dict of dimension slug -> list of dimension value slugs. If the response is not related to a survey, there will be no dimensions and an empty dict will always be returned. Using this field is more efficient than querying the dimensions field on the response, as the dimensions are cached on the response object. The respondent will only see values of dimensions that are designated as being shown to the respondent. */
  cachedDimensions?: Maybe<Scalars['GenericScalar']['output']>;
  /** Returns whether the response can be accepted by the user as an administrator. Not all survey workflows have the notion of accepting a response, in which case this field will always return False. */
  canAccept: Scalars['Boolean']['output'];
  /** Returns whether the response can be cancelled by the user. Not all survey workflows have the notion of cancelling a response, in which case this field will always return False. */
  canCancel: Scalars['Boolean']['output'];
  /** Whether the response can be deleted by the user. */
  canDelete: Scalars['Boolean']['output'];
  /** Returns whether the response can be edited by the user in the given edit mode. The edit mode can be either ADMIN (default) or OWN. ADMIN determines CBAC edit permissions, while OWN determines if the user is the owner of the response and editing it is allowed by the survey. */
  canEdit: Scalars['Boolean']['output'];
  dimensions: Array<ResponseDimensionValueType>;
  form: FormType;
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
  /** Language code of the form used to submit this response. */
  language: Scalars['String']['output'];
  oldVersions: Array<LimitedResponseType>;
  /** The date and time when the response was originally created. */
  originalCreatedAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who originally submitted this response.
   * If response is to an anonymous survey, this information will not be available.
   *
   */
  originalCreatedBy?: Maybe<SelectedProfileType>;
  /** For program offers, returns a list of programs created from the offer. For program host invitation form responses, returns a list containing the program the host was invited to. For forms managed by an app other than Program V2, returns an empty list. */
  programs: Array<LimitedProgramType>;
  revisionCreatedAt: Scalars['DateTime']['output'];
  /**
   *
   * Returns the user who submitted this version of the response.
   * If response is to an anonymous survey, this information will not be available.
   *
   */
  revisionCreatedBy?: Maybe<SelectedProfileType>;
  /** If this response is an old version, this field will point to the current version. */
  supersededBy?: Maybe<LimitedResponseType>;
  values?: Maybe<Scalars['GenericScalar']['output']>;
};


export type ProfileResponseTypeCachedDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type ProfileResponseTypeCanEditArgs = {
  mode?: InputMaybe<EditMode>;
};


export type ProfileResponseTypeDimensionsArgs = {
  keyDimensionsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};


export type ProfileResponseTypeValuesArgs = {
  keyFieldsOnly?: InputMaybe<Scalars['Boolean']['input']>;
};

/**
 * Represents a user profile with fields describing the involvement
 * of the user with an event.
 */
export type ProfileWithInvolvementType = {
  __typename?: 'ProfileWithInvolvementType';
  discordHandle: Scalars['String']['output'];
  /** The display name generally follows the format Firstname "Nickname" Lastname. If some parts are missing or the user has requested not to display them, we will adjust the format accordingly. */
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  /** The full name is similar to display name, but includes the last name if it is available. The full name generally should not be displayed to the public (use display name instead), but is used internally for identification purposes. */
  fullName: Scalars['String']['output'];
  id: Scalars['Int']['output'];
  involvements: Array<LimitedInvolvementType>;
  /** Returns True if the user has at least one active involvement in the event. */
  isActive: Scalars['Boolean']['output'];
  lastName: Scalars['String']['output'];
  nick: Scalars['String']['output'];
  phoneNumber: Scalars['String']['output'];
  profileFieldSelector: ProfileFieldSelectorType;
};

export type ProgramAnnotationType = {
  __typename?: 'ProgramAnnotationType';
  annotation: AnnotationType;
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

/** An enumeration. */
export enum ProgramHostRole {
  Invited = 'INVITED',
  Offerer = 'OFFERER'
}

/** An enumeration. */
export enum ProgramItemResolution {
  Cancel = 'CANCEL',
  CancelAndHide = 'CANCEL_AND_HIDE',
  Delete = 'DELETE'
}

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

/** An enumeration. */
export enum ProgramOfferResolution {
  Cancel = 'CANCEL',
  Delete = 'DELETE',
  Reject = 'REJECT'
}

/** An enumeration. */
export enum ProgramUserRelation {
  Favorited = 'FAVORITED',
  Hosting = 'HOSTING'
}

/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaType = {
  __typename?: 'ProgramV2EventMetaType';
  annotations: Array<AnnotationType>;
  /** Returns a link to the calendar export view for the event. The calendar export view accepts the following GET parameters, all optional: `favorited` - set to a truthy value to receive only favorites, `slug` - include only these programmes (can be multi-valued or separated by commas), `language` - the language to use when resolving dimensions. Further GET parameters are used to filter by dimensions. */
  calendarExportLink: Scalars['String']['output'];
  canDeleteProgramOffers: Scalars['Boolean']['output'];
  /** Returns the total number of program offers (not taking into account filters). */
  countProgramOffers: Scalars['Int']['output'];
  /** `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  dimensions: Array<FullDimensionType>;
  /** Used for admin purposes changing settings of annotations in events. Usually you should use `event.program.annotations` instead. */
  eventAnnotations: Array<LimitedUniverseAnnotationType>;
  invitations: Array<FullInvitationType>;
  /** Like `dimensions` but returns dimensions from the Involvement universe. Differs from `event.involvement.dimensions` in that permissions are checked based on the Program V2 application privileges, not Involvement. `is_list_filter` - only return dimensions that are shown in the list filter. `is_shown_in_detail` - only return dimensions that are shown in the detail view. If you supply both, you only get their intersection. */
  involvementDimensions: Array<FullDimensionType>;
  program?: Maybe<FullProgramType>;
  programHosts: Array<FullProgramHostType>;
  programHostsExcelExportLink: Scalars['String']['output'];
  /** Returns a single program offer. Also old versions of program offers can be retrieved by their ID. */
  programOffer?: Maybe<FullResponseType>;
  /** Returns all responses to all program offer forms of this event. */
  programOffers: Array<FullResponseType>;
  /** Returns a link to the the program offers Excel export view for the event. The program offers Excel export view returns all or filtered program offers in an Excel file, grouped into worksheets by the program form. `favorited` - set to a truthy value to receive only favorites, `slug` - include only these programmes (can be multi-valued or separated by commas), `language` - the language to use when resolving dimensions. Further GET parameters are used to filter by dimensions. */
  programOffersExcelExportLink: Scalars['String']['output'];
  programs: Array<FullProgramType>;
  reports: Array<ReportType>;
  scheduleItem?: Maybe<FullScheduleItemType>;
  scheduleItems: Array<FullScheduleItemType>;
  scheduleItemsExcelExportLink: Scalars['String']['output'];
  /** Returns the state dimension of the event, if there is one. */
  stateDimension?: Maybe<FullDimensionType>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeAnnotationsArgs = {
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
  slug?: InputMaybe<Array<Scalars['String']['input']>>;
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
export type ProgramV2EventMetaTypeInvolvementDimensionsArgs = {
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
export type ProgramV2EventMetaTypeProgramHostsArgs = {
  programFilters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
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
export type ProgramV2EventMetaTypeReportsArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


/**
 * NOTE: There is no `programForms` because a program form is a Survey with `app: PROGRAM_V2`.
 * Use `event.forms.surveys(app: PROGRAM_V2)` for that instead.
 */
export type ProgramV2EventMetaTypeScheduleItemArgs = {
  slug: Scalars['String']['input'];
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
  /** Returns all current responses to all program offer forms of this event. */
  programOffers: Array<ProfileResponseType>;
  /** Get programs that relate to this user in some way. Currently only favorites are implemented, but in the future also signed up and hosting. Dimension filter may only be specified when event_slug is given. */
  programs?: Maybe<Array<FullProgramType>>;
  /** Get programs that relate to this user in some way. Currently only favorites are implemented, but in the future also signed up and hosting. Dimension filter may only be specified when event_slug is given. */
  scheduleItems?: Maybe<Array<FullScheduleItemType>>;
};


export type ProgramV2ProfileMetaTypeProgramOffersArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
};


export type ProgramV2ProfileMetaTypeProgramsArgs = {
  eventSlug?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
  userRelation?: InputMaybe<ProgramUserRelation>;
};


export type ProgramV2ProfileMetaTypeScheduleItemsArgs = {
  eventSlug?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
  userRelation?: InputMaybe<ProgramUserRelation>;
};

/**
 * Promotes a Single Select or Multiple Select field to a dimension.
 *
 * This is used when a field is created as a Single Select or Multiple Select
 * and later discovered that it should be a dimension.
 */
export type PromoteFieldToDimension = {
  __typename?: 'PromoteFieldToDimension';
  survey?: Maybe<FullSurveyType>;
};

export type PromoteFieldToDimensionInput = {
  eventSlug: Scalars['String']['input'];
  fieldSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
};

export type PutDimension = {
  __typename?: 'PutDimension';
  dimension?: Maybe<FullDimensionType>;
};

export type PutDimensionInput = {
  dimensionSlug: Scalars['String']['input'];
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
  valueSlug: Scalars['String']['input'];
};

export type PutScheduleItem = {
  __typename?: 'PutScheduleItem';
  scheduleItem?: Maybe<FullScheduleItemType>;
};

export type PutScheduleItemInput = {
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  scheduleItem: ScheduleItemInput;
};

export type PutUniverseAnnotation = {
  __typename?: 'PutUniverseAnnotation';
  universeAnnotation?: Maybe<LimitedUniverseAnnotationType>;
};

/** An enumeration. */
export enum PutUniverseAnnotationAction {
  SaveAndRefresh = 'SAVE_AND_REFRESH',
  SaveWithoutRefresh = 'SAVE_WITHOUT_REFRESH'
}

export type PutUniverseAnnotationInput = {
  action?: InputMaybe<PutUniverseAnnotationAction>;
  annotationSlug: Scalars['String']['input'];
  formFields: Array<Scalars['String']['input']>;
  isActive: Scalars['Boolean']['input'];
  scopeSlug: Scalars['String']['input'];
  universeSlug: Scalars['String']['input'];
};

export type Query = {
  __typename?: 'Query';
  event?: Maybe<FullEventType>;
  profile?: Maybe<OwnProfileType>;
  /** Returns the registry that hosts the personal data of all users of Kompassi. */
  userRegistry: LimitedRegistryType;
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
  productIds: Array<Scalars['Int']['input']>;
};

export type ReportType = {
  __typename?: 'ReportType';
  columns: Array<ColumnType>;
  footer: Scalars['String']['output'];
  hasTotalRow: Scalars['Boolean']['output'];
  lang: Scalars['String']['output'];
  rows: Array<Array<Maybe<Scalars['GenericScalar']['output']>>>;
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
  totalRow?: Maybe<Array<Maybe<Scalars['GenericScalar']['output']>>>;
};


export type ReportTypeFooterArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type ReportTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type ResendInvitation = {
  __typename?: 'ResendInvitation';
  invitation?: Maybe<LimitedInvitationType>;
};

export type ResendInvitationInput = {
  eventSlug: Scalars['String']['input'];
  invitationId: Scalars['String']['input'];
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

/** Restore a program item that was previously cancelled. */
export type RestoreProgram = {
  __typename?: 'RestoreProgram';
  programSlug: Scalars['String']['output'];
};

export type RestoreProgramInput = {
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
};

export type RevokeKeyPair = {
  __typename?: 'RevokeKeyPair';
  id: Scalars['String']['output'];
};

export type ScheduleItemInput = {
  durationMinutes: Scalars['Int']['input'];
  freeformLocation?: InputMaybe<Scalars['String']['input']>;
  isPublic?: InputMaybe<Scalars['Boolean']['input']>;
  room?: InputMaybe<Scalars['String']['input']>;
  slug: Scalars['String']['input'];
  startTime: Scalars['DateTime']['input'];
  subtitle: Scalars['String']['input'];
};

/**
 * Represents a user profile with fields that can be selected for transfer.
 * NOTE: Must match Profile in frontend/src/components/involvement/models.ts.
 */
export type SelectedProfileType = {
  __typename?: 'SelectedProfileType';
  discordHandle: Scalars['String']['output'];
  /** The display name generally follows the format Firstname "Nickname" Lastname. If some parts are missing or the user has requested not to display them, we will adjust the format accordingly. */
  displayName: Scalars['String']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  /** The full name is similar to display name, but includes the last name if it is available. The full name generally should not be displayed to the public (use display name instead), but is used internally for identification purposes. */
  fullName: Scalars['String']['output'];
  id: Scalars['Int']['output'];
  lastName: Scalars['String']['output'];
  nick: Scalars['String']['output'];
  phoneNumber: Scalars['String']['output'];
  profileFieldSelector: ProfileFieldSelectorType;
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
export enum SurveyDefaultDimensionsUniverse {
  Involvement = 'INVOLVEMENT',
  Response = 'RESPONSE'
}

/** An enumeration. */
export enum SurveyPurpose {
  Default = 'DEFAULT',
  Invite = 'INVITE'
}

/** An enumeration. */
export enum SurveyRelation {
  Accessible = 'ACCESSIBLE',
  Subscribed = 'SUBSCRIBED'
}

export type TicketsV2EventMetaType = {
  __typename?: 'TicketsV2EventMetaType';
  /** Returns the total number of orders made to this event. Admin oriented view; customers will access order information through `profile.tickets`. */
  countTotalOrders: Scalars['Int']['output'];
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
  /** Get single report. For available reports, see `getReports.slug`. */
  report?: Maybe<ReportType>;
  /** Get all the reports. */
  reports: Array<ReportType>;
};


export type TicketsV2EventMetaTypeOrderArgs = {
  id: Scalars['String']['input'];
};


export type TicketsV2EventMetaTypeOrdersArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
  returnNone?: InputMaybe<Scalars['Boolean']['input']>;
  search?: InputMaybe<Scalars['String']['input']>;
};


export type TicketsV2EventMetaTypeProductArgs = {
  id: Scalars['String']['input'];
};


export type TicketsV2EventMetaTypeQuotaArgs = {
  id: Scalars['Int']['input'];
};


export type TicketsV2EventMetaTypeReportArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
  slug: Scalars['String']['input'];
};


export type TicketsV2EventMetaTypeReportsArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
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

/** An enumeration. */
export enum TotalBy {
  Average = 'AVERAGE',
  None = 'NONE',
  Sum = 'SUM'
}

/** An enumeration. */
export enum TypeOfColumn {
  Currency = 'CURRENCY',
  Datetime = 'DATETIME',
  Int = 'INT',
  Percentage = 'PERCENTAGE',
  String = 'STRING'
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

export type UpdateInvolvementDimensions = {
  __typename?: 'UpdateInvolvementDimensions';
  involvement?: Maybe<LimitedInvolvementType>;
};

export type UpdateInvolvementDimensionsInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  involvementId: Scalars['String']['input'];
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
  productId: Scalars['Int']['input'];
};

export type UpdateProgram = {
  __typename?: 'UpdateProgram';
  program?: Maybe<FullProgramType>;
};

export type UpdateProgramAnnotations = {
  __typename?: 'UpdateProgramAnnotations';
  program?: Maybe<FullProgramType>;
};

export type UpdateProgramAnnotationsInput = {
  annotations: Scalars['GenericScalar']['input'];
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
};

export type UpdateProgramDimensions = {
  __typename?: 'UpdateProgramDimensions';
  program?: Maybe<FullProgramType>;
};

export type UpdateProgramDimensionsInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  programSlug: Scalars['String']['input'];
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

export type UpdateSurveyDefaultDimensions = {
  __typename?: 'UpdateSurveyDefaultDimensions';
  survey?: Maybe<FullSurveyType>;
};

export type UpdateSurveyDefaultDimensionsInput = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  surveySlug: Scalars['String']['input'];
  universe: SurveyDefaultDimensionsUniverse;
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


export type SurveyPageQueryQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, userRegistry: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } }, event?: { __typename?: 'FullEventType', slug: string, name: string, timezone: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', loginRequired: boolean, anonymity: Anonymity, maxResponsesPerUser: number, countResponsesByCurrentUser: number, isActive: boolean, purpose: SurveyPurpose, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean }, registry?: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } } | null, form?: { __typename?: 'FormType', language: FormsFormLanguageChoices, title: string, description: string, fields?: unknown | null } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type SurveyThankYouPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyThankYouPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', form?: { __typename?: 'FormType', title: string, thankYouMessage: string } | null } | null } | null } | null };

export type AcceptInvitationMutationVariables = Exact<{
  input: AcceptInvitationInput;
}>;


export type AcceptInvitationMutation = { __typename?: 'Mutation', acceptInvitation?: { __typename?: 'AcceptInvitation', involvement?: { __typename?: 'LimitedInvolvementType', program?: { __typename?: 'LimitedProgramType', slug: string } | null } | null } | null };

export type TransferConsentFormRegistryFragment = { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } };

export type AcceptInvitationPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  invitationId: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type AcceptInvitationPageQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, userRegistry: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } }, event?: { __typename?: 'FullEventType', slug: string, name: string, timezone: string, involvement?: { __typename?: 'InvolvementEventMetaType', invitation?: { __typename?: 'FullInvitationType', isUsed: boolean, program?: { __typename?: 'LimitedProgramType', slug: string, title: string, description: string } | null, survey?: { __typename?: 'FullSurveyType', slug: string, isActive: boolean, purpose: SurveyPurpose, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean }, registry?: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } } | null, form?: { __typename?: 'FormType', language: FormsFormLanguageChoices, title: string, description: string, fields?: unknown | null } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null } | null };

export type PutInvolvementDimensionMutationVariables = Exact<{
  input: PutDimensionInput;
}>;


export type PutInvolvementDimensionMutation = { __typename?: 'Mutation', putDimension?: { __typename?: 'PutDimension', dimension?: { __typename?: 'FullDimensionType', slug: string } | null } | null };

export type DeleteInvolvementDimensionMutationVariables = Exact<{
  input: DeleteDimensionInput;
}>;


export type DeleteInvolvementDimensionMutation = { __typename?: 'Mutation', deleteDimension?: { __typename?: 'DeleteDimension', slug?: string | null } | null };

export type PutInvolvementDimensionValueMutationVariables = Exact<{
  input: PutDimensionValueInput;
}>;


export type PutInvolvementDimensionValueMutation = { __typename?: 'Mutation', putDimensionValue?: { __typename?: 'PutDimensionValue', value?: { __typename?: 'DimensionValueType', slug: string } | null } | null };

export type DeleteInvolvementDimensionValueMutationVariables = Exact<{
  input: DeleteDimensionValueInput;
}>;


export type DeleteInvolvementDimensionValueMutation = { __typename?: 'Mutation', deleteDimensionValue?: { __typename?: 'DeleteDimensionValue', slug?: string | null } | null };

export type InvolvementDimensionsListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale: Scalars['String']['input'];
}>;


export type InvolvementDimensionsListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, involvement?: { __typename?: 'InvolvementEventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }> } | null } | null };

export type InvolvementAdminReportsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type InvolvementAdminReportsPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, involvement?: { __typename?: 'InvolvementEventMetaType', reports: Array<{ __typename?: 'ReportType', slug: string, title: string, footer: string, rows: Array<Array<unknown | null>>, totalRow?: Array<unknown | null> | null, columns: Array<{ __typename?: 'ColumnType', slug: string, title: string, type: TypeOfColumn }> }> } | null } | null };

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

export type MarkOrderAsPaidMutationVariables = Exact<{
  input: MarkOrderAsPaidInput;
}>;


export type MarkOrderAsPaidMutation = { __typename?: 'Mutation', markOrderAsPaid?: { __typename?: 'MarkOrderAsPaid', order?: { __typename?: 'LimitedOrderType', id: string } | null } | null };

export type AdminOrderPaymentStampFragment = { __typename?: 'LimitedPaymentStampType', id: string, createdAt: string, correlationId: string, provider: PaymentProvider, type: PaymentStampType, status: PaymentStatus, data: unknown };

export type AdminOrderReceiptFragment = { __typename?: 'LimitedReceiptType', correlationId: string, createdAt: string, email: string, type: ReceiptType, status: ReceiptStatus };

export type AdminOrderCodeFragment = { __typename?: 'LimitedCodeType', code: string, literateCode: string, status: CodeStatus, usedOn?: string | null, productText: string };

export type AdminOrderDetailQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
}>;


export type AdminOrderDetailQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, tickets?: { __typename?: 'TicketsV2EventMetaType', order?: { __typename?: 'FullOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, firstName: string, lastName: string, email: string, phone: string, canRefund: boolean, canRefundManually: boolean, canMarkAsPaid: boolean, products: Array<{ __typename?: 'OrderProductType', title: string, quantity: number, price: any }>, paymentStamps: Array<{ __typename?: 'LimitedPaymentStampType', id: string, createdAt: string, correlationId: string, provider: PaymentProvider, type: PaymentStampType, status: PaymentStatus, data: unknown }>, receipts: Array<{ __typename?: 'LimitedReceiptType', correlationId: string, createdAt: string, email: string, type: ReceiptType, status: ReceiptStatus }>, codes: Array<{ __typename?: 'LimitedCodeType', code: string, literateCode: string, status: CodeStatus, usedOn?: string | null, productText: string }> } | null } | null } | null };

export type AdminCreateOrderMutationVariables = Exact<{
  input: CreateOrderInput;
}>;


export type AdminCreateOrderMutation = { __typename?: 'Mutation', createOrder?: { __typename?: 'CreateOrder', order?: { __typename?: 'FullOrderType', id: string, event: { __typename?: 'LimitedEventType', slug: string } } | null } | null };

export type NewOrderProductFragment = { __typename?: 'FullProductType', id: number, title: string, description: string, price: any, isAvailable: boolean, availableFrom?: string | null, availableUntil?: string | null, countPaid: number, countReserved: number, countAvailable?: number | null, maxPerOrder: number };

export type NewOrderPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
}>;


export type NewOrderPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', products: Array<{ __typename?: 'FullProductType', id: number, title: string, description: string, price: any, isAvailable: boolean, availableFrom?: string | null, availableUntil?: string | null, countPaid: number, countReserved: number, countAvailable?: number | null, maxPerOrder: number }> } | null } | null };

export type OrderListFragment = { __typename?: 'FullOrderType', id: string, formattedOrderNumber: string, displayName: string, email: string, createdAt: string, totalPrice: any, status: PaymentStatus };

export type ProductChoiceFragment = { __typename?: 'FullProductType', id: number, title: string };

export type AdminOrderListWithOrdersQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
  search?: InputMaybe<Scalars['String']['input']>;
  returnNone?: InputMaybe<Scalars['Boolean']['input']>;
}>;


export type AdminOrderListWithOrdersQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', countTotalOrders: number, products: Array<{ __typename?: 'FullProductType', id: number, title: string }>, orders: Array<{ __typename?: 'FullOrderType', id: string, formattedOrderNumber: string, displayName: string, email: string, createdAt: string, totalPrice: any, status: PaymentStatus }> } | null } | null };

export type CancelOwnOrderMutationVariables = Exact<{
  input: CancelOwnUnpaidOrderInput;
}>;


export type CancelOwnOrderMutation = { __typename?: 'Mutation', cancelOwnUnpaidOrder?: { __typename?: 'CancelOwnUnpaidOrder', order?: { __typename?: 'LimitedOrderType', id: string } | null } | null };

export type InvolvedPersonDetailInvolvementFragment = { __typename?: 'LimitedInvolvementType', id: string, type: InvolvementType, title: string, adminLink?: string | null, isActive: boolean, cachedDimensions: unknown, cachedAnnotations: unknown };

export type InvolvedPersonDetailFragment = { __typename?: 'ProfileWithInvolvementType', id: number, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string, fullName: string, isActive: boolean, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean }, involvements: Array<{ __typename?: 'LimitedInvolvementType', id: string, type: InvolvementType, title: string, adminLink?: string | null, isActive: boolean, cachedDimensions: unknown, cachedAnnotations: unknown }> };

export type PersonPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  personId: Scalars['Int']['input'];
}>;


export type PersonPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, timezone: string, involvement?: { __typename?: 'InvolvementEventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', isKeyDimension: boolean, isShownInDetail: boolean, slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, annotations: Array<{ __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string, description: string, isComputed: boolean }>, person?: { __typename?: 'ProfileWithInvolvementType', id: number, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string, fullName: string, isActive: boolean, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean }, involvements: Array<{ __typename?: 'LimitedInvolvementType', id: string, type: InvolvementType, title: string, adminLink?: string | null, isActive: boolean, cachedDimensions: unknown, cachedAnnotations: unknown }> } | null } | null } | null };

export type InvolvedPersonInvolvementFragment = { __typename?: 'LimitedInvolvementType', id: string, type: InvolvementType, title: string, adminLink?: string | null, isActive: boolean, cachedDimensions: unknown, cachedAnnotations: unknown };

export type InvolvedPersonFragment = { __typename?: 'ProfileWithInvolvementType', firstName: string, lastName: string, nick: string, isActive: boolean, involvements: Array<{ __typename?: 'LimitedInvolvementType', id: string, type: InvolvementType, title: string, adminLink?: string | null, isActive: boolean, cachedDimensions: unknown, cachedAnnotations: unknown }> };

export type PeoplePageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
  locale?: InputMaybe<Scalars['String']['input']>;
  search?: InputMaybe<Scalars['String']['input']>;
  returnNone?: InputMaybe<Scalars['Boolean']['input']>;
}>;


export type PeoplePageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, timezone: string, involvement?: { __typename?: 'InvolvementEventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, people: Array<{ __typename?: 'ProfileWithInvolvementType', firstName: string, lastName: string, nick: string, isActive: boolean, involvements: Array<{ __typename?: 'LimitedInvolvementType', id: string, type: InvolvementType, title: string, adminLink?: string | null, isActive: boolean, cachedDimensions: unknown, cachedAnnotations: unknown }> }> } | null } | null };

export type UpdateProductMutationVariables = Exact<{
  input: UpdateProductInput;
}>;


export type UpdateProductMutation = { __typename?: 'Mutation', updateProduct?: { __typename?: 'UpdateProduct', product?: { __typename?: 'LimitedProductType', id: number } | null } | null };

export type DeleteProductMutationVariables = Exact<{
  input: DeleteProductInput;
}>;


export type DeleteProductMutation = { __typename?: 'Mutation', deleteProduct?: { __typename?: 'DeleteProduct', id: string } | null };

export type AdminProductOldVersionFragment = { __typename?: 'LimitedProductType', createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number };

export type AdminProductDetailFragment = { __typename?: 'FullProductType', id: number, createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number, availableFrom?: string | null, availableUntil?: string | null, canDelete: boolean, quotas: Array<{ __typename?: 'LimitedQuotaType', id: string }>, supersededBy?: { __typename?: 'LimitedProductType', id: number } | null, oldVersions: Array<{ __typename?: 'LimitedProductType', createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number }> };

export type AdminProductDetailPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  productId: Scalars['String']['input'];
}>;


export type AdminProductDetailPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', quotas: Array<{ __typename?: 'FullQuotaType', id: string, name: string, countTotal: number }>, product: { __typename?: 'FullProductType', id: number, createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number, availableFrom?: string | null, availableUntil?: string | null, canDelete: boolean, quotas: Array<{ __typename?: 'LimitedQuotaType', id: string }>, supersededBy?: { __typename?: 'LimitedProductType', id: number } | null, oldVersions: Array<{ __typename?: 'LimitedProductType', createdAt: string, title: string, description: string, price: any, eticketsPerProduct: number, maxPerOrder: number }> } } | null } | null };

export type CreateProductMutationVariables = Exact<{
  input: CreateProductInput;
}>;


export type CreateProductMutation = { __typename?: 'Mutation', createProduct?: { __typename?: 'CreateProduct', product?: { __typename?: 'LimitedProductType', id: number } | null } | null };

export type ReorderProductsMutationVariables = Exact<{
  input: ReorderProductsInput;
}>;


export type ReorderProductsMutation = { __typename?: 'Mutation', reorderProducts?: { __typename?: 'ReorderProducts', products: Array<{ __typename?: 'LimitedProductType', id: number }> } | null };

export type ProductListFragment = { __typename?: 'FullProductType', id: number, title: string, description: string, price: any, isAvailable: boolean, availableFrom?: string | null, availableUntil?: string | null, countPaid: number, countReserved: number, countAvailable?: number | null };

export type ProductListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
}>;


export type ProductListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', products: Array<{ __typename?: 'FullProductType', id: number, title: string, description: string, price: any, isAvailable: boolean, availableFrom?: string | null, availableUntil?: string | null, countPaid: number, countReserved: number, countAvailable?: number | null }> } | null } | null };

export type UpdateProgramBasicInfoMutationVariables = Exact<{
  input: UpdateProgramInput;
}>;


export type UpdateProgramBasicInfoMutation = { __typename?: 'Mutation', updateProgram?: { __typename?: 'UpdateProgram', program?: { __typename?: 'FullProgramType', slug: string } | null } | null };

export type CancelProgramItemMutationVariables = Exact<{
  input: CancelProgramInput;
}>;


export type CancelProgramItemMutation = { __typename?: 'Mutation', cancelProgram?: { __typename?: 'CancelProgram', responseId?: string | null } | null };

export type RestoreProgramItemMutationVariables = Exact<{
  input: RestoreProgramInput;
}>;


export type RestoreProgramItemMutation = { __typename?: 'Mutation', restoreProgram?: { __typename?: 'RestoreProgram', programSlug: string } | null };

export type ProgramAdminDetailAnnotationsQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminDetailAnnotationsQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, program?: { __typename?: 'ProgramV2EventMetaType', annotations: Array<{ __typename?: 'AnnotationType', isApplicableToProgramItems: boolean, slug: string, type: AnnotationDataType, title: string, description: string, isComputed: boolean }>, program?: { __typename?: 'FullProgramType', slug: string, title: string, cachedAnnotations: unknown, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }> } | null } | null } | null };

export type UpdateProgramDimensionsMutationVariables = Exact<{
  input: UpdateProgramDimensionsInput;
}>;


export type UpdateProgramDimensionsMutation = { __typename?: 'Mutation', updateProgramDimensions?: { __typename?: 'UpdateProgramDimensions', program?: { __typename?: 'FullProgramType', slug: string } | null } | null };

export type ProgramAdminDetailDimensionsQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminDetailDimensionsQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, program?: { __typename?: 'ProgramV2EventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }>, program?: { __typename?: 'FullProgramType', slug: string, title: string, cachedDimensions?: unknown | null, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }> } | null } | null } | null };

export type InviteProgramHostMutationVariables = Exact<{
  input: InviteProgramHostInput;
}>;


export type InviteProgramHostMutation = { __typename?: 'Mutation', inviteProgramHost?: { __typename?: 'InviteProgramHost', invitation: { __typename?: 'FullInvitationType', id: string } } | null };

export type DeleteProgramHostMutationVariables = Exact<{
  input: DeleteProgramHostInput;
}>;


export type DeleteProgramHostMutation = { __typename?: 'Mutation', deleteProgramHost?: { __typename?: 'DeleteProgramHost', program: { __typename?: 'FullProgramType', slug: string } } | null };

export type UpdateProgramHostDimensionsMutationVariables = Exact<{
  input: UpdateInvolvementDimensionsInput;
}>;


export type UpdateProgramHostDimensionsMutation = { __typename?: 'Mutation', updateInvolvementDimensions?: { __typename?: 'UpdateInvolvementDimensions', involvement?: { __typename?: 'LimitedInvolvementType', program?: { __typename?: 'LimitedProgramType', slug: string } | null } | null } | null };

export type DeleteInvitationMutationVariables = Exact<{
  input: DeleteInvitationInput;
}>;


export type DeleteInvitationMutation = { __typename?: 'Mutation', deleteInvitation?: { __typename?: 'DeleteInvitation', invitation?: { __typename?: 'LimitedInvitationType', id: string } | null } | null };

export type ResendInvitationMutationVariables = Exact<{
  input: ResendInvitationInput;
}>;


export type ResendInvitationMutation = { __typename?: 'Mutation', resendInvitation?: { __typename?: 'ResendInvitation', invitation?: { __typename?: 'LimitedInvitationType', id: string } | null } | null };

export type ProgramAdminDetailHostFragment = { __typename?: 'LimitedProgramHostType', id: string, cachedDimensions: unknown, programHostRole?: ProgramHostRole | null, person: { __typename?: 'LimitedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } };

export type ProgramAdminDetailInvitationFragment = { __typename?: 'LimitedInvitationType', id: string, email: string, createdAt: string, cachedDimensions?: unknown | null };

export type ProgramAdminDetailHostsQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  annotationSlugs: Array<Scalars['String']['input']> | Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminDetailHostsQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, forms?: { __typename?: 'FormsEventMetaType', inviteForms: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, cachedDefaultInvolvementDimensions?: unknown | null }> } | null, program?: { __typename?: 'ProgramV2EventMetaType', involvementDimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, annotations: Array<{ __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string, description: string, isComputed: boolean }>, program?: { __typename?: 'FullProgramType', slug: string, title: string, canInviteProgramHost: boolean, cachedAnnotations: unknown, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, programHosts: Array<{ __typename?: 'LimitedProgramHostType', id: string, cachedDimensions: unknown, programHostRole?: ProgramHostRole | null, person: { __typename?: 'LimitedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } }>, invitations: Array<{ __typename?: 'LimitedInvitationType', id: string, email: string, createdAt: string, cachedDimensions?: unknown | null }> } | null } | null } | null };

export type ProgramAdminDetailQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminDetailQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', calendarExportLink: string, program?: { __typename?: 'FullProgramType', slug: string, title: string, description: string, cachedHosts: string, canCancel: boolean, canDelete: boolean, canRestore: boolean, programOffer?: { __typename?: 'LimitedResponseType', id: string, values?: unknown | null } | null, links: Array<{ __typename?: 'ProgramLink', type: ProgramLinkType, href: string, title: string }>, annotations: Array<{ __typename?: 'ProgramAnnotationType', value?: unknown | null, annotation: { __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string } }>, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, subtitle: string, location?: string | null, startTime: string, endTime: string }> } | null } | null } | null };

export type PutScheduleItemMutationVariables = Exact<{
  input: PutScheduleItemInput;
}>;


export type PutScheduleItemMutation = { __typename?: 'Mutation', putScheduleItem?: { __typename?: 'PutScheduleItem', scheduleItem?: { __typename?: 'FullScheduleItemType', slug: string } | null } | null };

export type DeleteScheduleItemMutationVariables = Exact<{
  input: DeleteScheduleItemInput;
}>;


export type DeleteScheduleItemMutation = { __typename?: 'Mutation', deleteScheduleItem?: { __typename?: 'DeleteScheduleItem', slug?: string | null } | null };

export type ProgramAdminDetailScheduleItemFragment = { __typename?: 'LimitedScheduleItemType', slug: string, title: string, subtitle: string, location?: string | null, startTime: string, durationMinutes: number, room: string, freeformLocation: string, isPublic: boolean };

export type ProgramAdminDetailScheduleQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminDetailScheduleQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, program?: { __typename?: 'FullProgramType', slug: string, title: string, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, title: string, subtitle: string, location?: string | null, startTime: string, durationMinutes: number, room: string, freeformLocation: string, isPublic: boolean }> } | null } | null } | null };

export type CreateProgramMutationVariables = Exact<{
  input: CreateProgramInput;
}>;


export type CreateProgramMutation = { __typename?: 'Mutation', createProgram?: { __typename?: 'CreateProgram', program?: { __typename?: 'FullProgramType', slug: string } | null } | null };

export type ProgramAdminFragment = { __typename?: 'FullProgramType', slug: string, title: string, cachedDimensions?: unknown | null, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', startTime: string }> };

export type ProgramAdminListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type ProgramAdminListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, program?: { __typename?: 'ProgramV2EventMetaType', scheduleItemsExcelExportLink: string, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, isKeyDimension: boolean, isListFilter: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, programs: Array<{ __typename?: 'FullProgramType', slug: string, title: string, cachedDimensions?: unknown | null, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', startTime: string }> }> } | null } | null };

export type PutEventAnnotationMutationVariables = Exact<{
  input: PutUniverseAnnotationInput;
}>;


export type PutEventAnnotationMutation = { __typename?: 'Mutation', putUniverseAnnotation?: { __typename?: 'PutUniverseAnnotation', universeAnnotation?: { __typename?: 'LimitedUniverseAnnotationType', annotation: { __typename?: 'AnnotationType', slug: string } } | null } | null };

export type ProgramAdminEventAnnotationFragment = { __typename?: 'LimitedUniverseAnnotationType', isActive: boolean, formFields?: unknown | null, annotation: { __typename?: 'AnnotationType', slug: string, title: string, description: string, type: AnnotationDataType, isComputed: boolean, isPublic: boolean, isShownInDetail: boolean, isInternal: boolean, isApplicableToProgramItems: boolean, isApplicableToScheduleItems: boolean } };

export type ProgramAdminEventAnnotationsQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminEventAnnotationsQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', eventAnnotations: Array<{ __typename?: 'LimitedUniverseAnnotationType', isActive: boolean, formFields?: unknown | null, annotation: { __typename?: 'AnnotationType', slug: string, title: string, description: string, type: AnnotationDataType, isComputed: boolean, isPublic: boolean, isShownInDetail: boolean, isInternal: boolean, isApplicableToProgramItems: boolean, isApplicableToScheduleItems: boolean } }> } | null } | null };

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


export type ProgramDimensionsListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, program?: { __typename?: 'ProgramV2EventMetaType', dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }> } | null } | null };

export type UpdateProgramFormDefaultDimensionsMutationVariables = Exact<{
  input: UpdateSurveyDefaultDimensionsInput;
}>;


export type UpdateProgramFormDefaultDimensionsMutation = { __typename?: 'Mutation', updateSurveyDefaultDimensions?: { __typename?: 'UpdateSurveyDefaultDimensions', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type DimensionDefaultsQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale: Scalars['String']['input'];
}>;


export type DimensionDefaultsQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, program?: { __typename?: 'ProgramV2EventMetaType', involvementDimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }> } | null, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, cachedDefaultResponseDimensions?: unknown | null, cachedDefaultInvolvementDimensions?: unknown | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }>, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }> } | null } | null } | null };

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

export type PromoteProgramFormFieldToDimensionMutationVariables = Exact<{
  input: PromoteFieldToDimensionInput;
}>;


export type PromoteProgramFormFieldToDimensionMutation = { __typename?: 'Mutation', promoteFieldToDimension?: { __typename?: 'PromoteFieldToDimension', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type EditProgramFormFieldsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditProgramFormFieldsPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }>, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type EditProgramFormLanguageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditProgramFormLanguagePageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditProgramFormLanguagePageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

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

export type EditProgramFormFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, activeFrom?: string | null, activeUntil?: string | null, canRemove: boolean, purpose: SurveyPurpose, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> };

export type EditProgramFormPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditProgramFormPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, activeFrom?: string | null, activeUntil?: string | null, canRemove: boolean, purpose: SurveyPurpose, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> } | null } | null } | null };

export type ProgramFormResponseFragment = { __typename?: 'LimitedResponseType', id: string, sequenceNumber: number, revisionCreatedAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> };

export type ProgramFormResponsesQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type ProgramFormResponsesQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, anonymity: Anonymity, fields?: unknown | null, countResponses: number, canRemoveResponses: boolean, protectResponses: boolean, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, responses?: Array<{ __typename?: 'LimitedResponseType', id: string, sequenceNumber: number, revisionCreatedAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> }> | null } | null } | null } | null };

export type CreateProgramFormMutationVariables = Exact<{
  input: CreateProgramFormInput;
}>;


export type CreateProgramFormMutation = { __typename?: 'Mutation', createProgramForm?: { __typename?: 'CreateProgramForm', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type OfferFormFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, purpose: SurveyPurpose, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type ProgramFormsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramFormsPageQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', forms: { __typename?: 'FormsProfileMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, event: { __typename?: 'LimitedEventType', slug: string, name: string } }> } } | null, event?: { __typename?: 'FullEventType', slug: string, name: string, forms?: { __typename?: 'FormsEventMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, purpose: SurveyPurpose, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> }> } | null } | null };

export type ProgramAdminHostFragment = { __typename?: 'FullProgramHostType', person: { __typename?: 'LimitedProfileType', firstName: string, lastName: string, nick: string }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null }> };

export type ProgramAdminHostsQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminHostsQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', programHostsExcelExportLink: string, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, programHosts: Array<{ __typename?: 'FullProgramHostType', person: { __typename?: 'LimitedProfileType', firstName: string, lastName: string, nick: string }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null }> }> } | null } | null };

export type ProgramAdminInvitationFragment = { __typename?: 'FullInvitationType', id: string, email: string, createdAt: string, cachedDimensions?: unknown | null, program?: { __typename?: 'LimitedProgramType', slug: string, title: string } | null };

export type ProgramAdminInvitationsQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
}>;


export type ProgramAdminInvitationsQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', invitations: Array<{ __typename?: 'FullInvitationType', id: string, email: string, createdAt: string, cachedDimensions?: unknown | null, program?: { __typename?: 'LimitedProgramType', slug: string, title: string } | null }> } | null } | null };

export type AcceptProgramOfferMutationVariables = Exact<{
  input: AcceptProgramOfferInput;
}>;


export type AcceptProgramOfferMutation = { __typename?: 'Mutation', acceptProgramOffer?: { __typename?: 'AcceptProgramOffer', program: { __typename?: 'FullProgramType', slug: string } } | null };

export type CancelProgramOfferMutationVariables = Exact<{
  input: CancelProgramOfferInput;
}>;


export type CancelProgramOfferMutation = { __typename?: 'Mutation', cancelProgramOffer?: { __typename?: 'CancelProgramOffer', responseId: string } | null };

export type EditProgramOfferMutationVariables = Exact<{
  input: CreateSurveyResponseInput;
}>;


export type EditProgramOfferMutation = { __typename?: 'Mutation', createSurveyResponse?: { __typename?: 'CreateSurveyResponse', response?: { __typename?: 'ProfileResponseType', id: string } | null } | null };

export type ProgramOfferEditFragment = { __typename?: 'FullResponseType', id: string, revisionCreatedAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, canEdit: boolean, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, form: { __typename?: 'FormType', title: string, description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', slug: string, cachedDefaultResponseDimensions?: unknown | null, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export type ProgramOfferEditPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
}>;


export type ProgramOfferEditPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', programOffer?: { __typename?: 'FullResponseType', id: string, revisionCreatedAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, canEdit: boolean, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, form: { __typename?: 'FormType', title: string, description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', slug: string, cachedDefaultResponseDimensions?: unknown | null, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> } | null } | null } | null };

export type ProgramOfferDetailFragment = { __typename?: 'FullResponseType', values?: unknown | null, cachedDimensions?: unknown | null, canEdit: boolean, canAccept: boolean, canCancel: boolean, canDelete: boolean, id: string, originalCreatedAt: string, revisionCreatedAt: string, language: string, form: { __typename?: 'FormType', description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', title?: string | null, slug: string, cachedDefaultResponseDimensions?: unknown | null, cachedDefaultInvolvementDimensions?: unknown | null, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null }>, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export type ProgramOfferPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramOfferPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', involvementDimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, programOffer?: { __typename?: 'FullResponseType', values?: unknown | null, cachedDimensions?: unknown | null, canEdit: boolean, canAccept: boolean, canCancel: boolean, canDelete: boolean, id: string, originalCreatedAt: string, revisionCreatedAt: string, language: string, form: { __typename?: 'FormType', description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', title?: string | null, slug: string, cachedDefaultResponseDimensions?: unknown | null, cachedDefaultInvolvementDimensions?: unknown | null, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null }>, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> } | null } | null } | null };

export type DeleteProgramOffersMutationVariables = Exact<{
  input: DeleteProgramOffersInput;
}>;


export type DeleteProgramOffersMutation = { __typename?: 'Mutation', deleteProgramOffers?: { __typename?: 'DeleteProgramOffers', countDeleted: number } | null };

export type ProgramOfferFragment = { __typename?: 'FullResponseType', id: string, originalCreatedAt: string, sequenceNumber: number, values?: unknown | null, cachedDimensions?: unknown | null, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, form: { __typename?: 'FormType', language: FormsFormLanguageChoices, survey: { __typename?: 'FullSurveyType', title?: string | null } }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> };

export type ProgramOfferDimensionFragment = { __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> };

export type ProgramOffersQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type ProgramOffersQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, program?: { __typename?: 'ProgramV2EventMetaType', programOffersExcelExportLink: string, canDeleteProgramOffers: boolean, countProgramOffers: number, listFilters: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, keyDimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, stateDimension?: { __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> } | null, programOffers: Array<{ __typename?: 'FullResponseType', id: string, originalCreatedAt: string, sequenceNumber: number, values?: unknown | null, cachedDimensions?: unknown | null, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, form: { __typename?: 'FormType', language: FormsFormLanguageChoices, survey: { __typename?: 'FullSurveyType', title?: string | null } }, programs: Array<{ __typename?: 'LimitedProgramType', slug: string, title: string }> }> } | null } | null };

export type ProgramAdminReportsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramAdminReportsPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', reports: Array<{ __typename?: 'ReportType', slug: string, title: string, footer: string, rows: Array<Array<unknown | null>>, totalRow?: Array<unknown | null> | null, columns: Array<{ __typename?: 'ColumnType', slug: string, title: string, type: TypeOfColumn }> }> } | null } | null };

export type MarkScheduleItemAsFavoriteMutationVariables = Exact<{
  input: FavoriteScheduleItemInput;
}>;


export type MarkScheduleItemAsFavoriteMutation = { __typename?: 'Mutation', markScheduleItemAsFavorite?: { __typename?: 'MarkScheduleItemAsFavorite', success: boolean } | null };

export type UnmarkScheduleItemAsFavoriteMutationVariables = Exact<{
  input: FavoriteScheduleItemInput;
}>;


export type UnmarkScheduleItemAsFavoriteMutation = { __typename?: 'Mutation', unmarkScheduleItemAsFavorite?: { __typename?: 'UnmarkScheduleItemAsFavorite', success: boolean } | null };

export type ScheduleProgramFragment = { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string, isCancelled: boolean };

export type ScheduleItemListFragment = { __typename?: 'FullScheduleItemType', slug: string, location?: string | null, subtitle: string, startTime: string, endTime: string, program: { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string, isCancelled: boolean } };

export type ProgramListQueryQueryVariables = Exact<{
  locale?: InputMaybe<Scalars['String']['input']>;
  eventSlug: Scalars['String']['input'];
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
  hidePast?: InputMaybe<Scalars['Boolean']['input']>;
}>;


export type ProgramListQueryQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', program: { __typename?: 'ProgramV2ProfileMetaType', scheduleItems?: Array<{ __typename?: 'FullScheduleItemType', slug: string, location?: string | null, subtitle: string, startTime: string, endTime: string, program: { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string, isCancelled: boolean } }> | null } } | null, event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', calendarExportLink: string, listFilters: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, scheduleItems: Array<{ __typename?: 'FullScheduleItemType', slug: string, location?: string | null, subtitle: string, startTime: string, endTime: string, program: { __typename?: 'LimitedProgramType', slug: string, title: string, cachedDimensions?: unknown | null, color: string, isCancelled: boolean } }> } | null } | null };

export type CreateFeedbackMutationVariables = Exact<{
  input: ProgramFeedbackInput;
}>;


export type CreateFeedbackMutation = { __typename?: 'Mutation', createProgramFeedback?: { __typename?: 'CreateProgramFeedback', success: boolean } | null };

export type ProgramFeedbackQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
}>;


export type ProgramFeedbackQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, program?: { __typename?: 'ProgramV2EventMetaType', program?: { __typename?: 'FullProgramType', title: string, isAcceptingFeedback: boolean } | null } | null } | null };

export type ProgramDetailAnnotationFragment = { __typename?: 'ProgramAnnotationType', value?: unknown | null, annotation: { __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string } };

export type ProgramDetailQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  programSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgramDetailQueryQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', program: { __typename?: 'ProgramV2ProfileMetaType', scheduleItems?: Array<{ __typename?: 'FullScheduleItemType', slug: string }> | null } } | null, event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, program?: { __typename?: 'ProgramV2EventMetaType', calendarExportLink: string, program?: { __typename?: 'FullProgramType', title: string, description: string, cachedHosts: string, isCancelled: boolean, links: Array<{ __typename?: 'ProgramLink', type: ProgramLinkType, href: string, title: string }>, annotations: Array<{ __typename?: 'ProgramAnnotationType', value?: unknown | null, annotation: { __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string } }>, dimensions: Array<{ __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null } }>, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, subtitle: string, location?: string | null, startTime: string, endTime: string }> } | null } | null } | null };

export type UpdateQuotaMutationVariables = Exact<{
  input: UpdateQuotaInput;
}>;


export type UpdateQuotaMutation = { __typename?: 'Mutation', updateQuota?: { __typename?: 'UpdateQuota', quota?: { __typename?: 'LimitedQuotaType', id: string } | null } | null };

export type DeleteQuotaMutationVariables = Exact<{
  input: DeleteQuotaInput;
}>;


export type DeleteQuotaMutation = { __typename?: 'Mutation', deleteQuota?: { __typename?: 'DeleteQuota', id: string } | null };

export type QuotaProductFragment = { __typename?: 'LimitedProductType', id: number, title: string, price: any, countReserved: number };

export type AdminQuotaDetailPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  quotaId: Scalars['Int']['input'];
}>;


export type AdminQuotaDetailPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', quota: { __typename?: 'FullQuotaType', id: string, name: string, countReserved: number, canDelete: boolean, quota: number, products: Array<{ __typename?: 'LimitedProductType', id: number, title: string, price: any, countReserved: number }> } } | null } | null };

export type CreateQuotaMutationVariables = Exact<{
  input: CreateQuotaInput;
}>;


export type CreateQuotaMutation = { __typename?: 'Mutation', createQuota?: { __typename?: 'CreateQuota', quota?: { __typename?: 'LimitedQuotaType', id: string } | null } | null };

export type QuotaListFragment = { __typename?: 'FullQuotaType', id: string, countPaid: number, countReserved: number, countAvailable: number, countTotal: number, title: string };

export type QuotaListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
}>;


export type QuotaListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, tickets?: { __typename?: 'TicketsV2EventMetaType', quotas: Array<{ __typename?: 'FullQuotaType', id: string, countPaid: number, countReserved: number, countAvailable: number, countTotal: number, title: string }> } | null } | null };

export type UpdateSurveyDefaultDimensionsMutationVariables = Exact<{
  input: UpdateSurveyDefaultDimensionsInput;
}>;


export type UpdateSurveyDefaultDimensionsMutation = { __typename?: 'Mutation', updateSurveyDefaultDimensions?: { __typename?: 'UpdateSurveyDefaultDimensions', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type SurveyDimensionDefaultsQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale: Scalars['String']['input'];
}>;


export type SurveyDimensionDefaultsQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, purpose: SurveyPurpose, canRemove: boolean, cachedDefaultResponseDimensions?: unknown | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }>, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }> } | null } | null } | null };

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

export type DimensionsListQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale: Scalars['String']['input'];
}>;


export type DimensionsListQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }>, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }> } | null } | null } | null };

export type UpdateFormMutationMutationVariables = Exact<{
  input: UpdateFormInput;
}>;


export type UpdateFormMutationMutation = { __typename?: 'Mutation', updateForm?: { __typename?: 'UpdateForm', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type DeleteSurveyLanguageMutationVariables = Exact<{
  input: DeleteSurveyLanguageInput;
}>;


export type DeleteSurveyLanguageMutation = { __typename?: 'Mutation', deleteSurveyLanguage?: { __typename?: 'DeleteSurveyLanguage', language?: string | null } | null };

export type PromoteSurveyFieldToDimensionMutationVariables = Exact<{
  input: PromoteFieldToDimensionInput;
}>;


export type PromoteSurveyFieldToDimensionMutation = { __typename?: 'Mutation', promoteFieldToDimension?: { __typename?: 'PromoteFieldToDimension', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type EditSurveyFieldsPageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }>, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditSurveyFieldsPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditSurveyFieldsPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> }>, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

export type EditFormLanguagePageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type EditFormLanguagePageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  language: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditFormLanguagePageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, canRemove: boolean, purpose: SurveyPurpose, form?: { __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, description: string, thankYouMessage: string, fields?: unknown | null, canRemove: boolean } | null, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> } | null } | null } | null };

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

export type EditSurveyPageFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, loginRequired: boolean, anonymity: Anonymity, maxResponsesPerUser: number, countResponsesByCurrentUser: number, activeFrom?: string | null, activeUntil?: string | null, responsesEditableUntil?: string | null, canRemove: boolean, purpose: SurveyPurpose, protectResponses: boolean, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> };

export type EditSurveyPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type EditSurveyPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, loginRequired: boolean, anonymity: Anonymity, maxResponsesPerUser: number, countResponsesByCurrentUser: number, activeFrom?: string | null, activeUntil?: string | null, responsesEditableUntil?: string | null, canRemove: boolean, purpose: SurveyPurpose, protectResponses: boolean, languages: Array<{ __typename?: 'FormType', title: string, language: FormsFormLanguageChoices, canRemove: boolean }> } | null } | null } | null };

export type UpdateResponseDimensionsMutationVariables = Exact<{
  input: UpdateResponseDimensionsInput;
}>;


export type UpdateResponseDimensionsMutation = { __typename?: 'Mutation', updateResponseDimensions?: { __typename?: 'UpdateResponseDimensions', response?: { __typename?: 'FullResponseType', id: string } | null } | null };

export type EditSurveyResponseMutationVariables = Exact<{
  input: CreateSurveyResponseInput;
}>;


export type EditSurveyResponseMutation = { __typename?: 'Mutation', createSurveyResponse?: { __typename?: 'CreateSurveyResponse', response?: { __typename?: 'ProfileResponseType', id: string } | null } | null };

export type EditSurveyResponsePageFragment = { __typename?: 'FullResponseType', id: string, language: string, values?: unknown | null, revisionCreatedAt: string, canEdit: boolean, originalCreatedAt: string, form: { __typename?: 'FormType', title: string, description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', slug: string, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export type EditSurveyResponsePageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
}>;


export type EditSurveyResponsePageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', response?: { __typename?: 'FullResponseType', id: string, language: string, values?: unknown | null, revisionCreatedAt: string, canEdit: boolean, originalCreatedAt: string, form: { __typename?: 'FormType', title: string, description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', slug: string, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> } | null } | null } | null } | null };

export type SurveyResponseDetailFragment = { __typename?: 'FullResponseType', values?: unknown | null, cachedDimensions?: unknown | null, canEdit: boolean, canAccept: boolean, canCancel: boolean, canDelete: boolean, id: string, originalCreatedAt: string, revisionCreatedAt: string, language: string, form: { __typename?: 'FormType', description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', title?: string | null, slug: string, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export type SurveyResponseDetailQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyResponseDetailQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', slug: string, name: string, timezone: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', title?: string | null, slug: string, anonymity: Anonymity, canRemoveResponses: boolean, protectResponses: boolean, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }>, response?: { __typename?: 'FullResponseType', values?: unknown | null, cachedDimensions?: unknown | null, canEdit: boolean, canAccept: boolean, canCancel: boolean, canDelete: boolean, id: string, originalCreatedAt: string, revisionCreatedAt: string, language: string, form: { __typename?: 'FormType', description: string, fields?: unknown | null, survey: { __typename?: 'FullSurveyType', title?: string | null, slug: string, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> } | null } | null } | null } | null };

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

export type SurveyResponseFragment = { __typename?: 'LimitedResponseType', id: string, sequenceNumber: number, revisionCreatedAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null };

export type FormResponsesQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type FormResponsesQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', forms: { __typename?: 'FormsProfileMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string }> } } | null, event?: { __typename?: 'FullEventType', name: string, slug: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', slug: string, title?: string | null, anonymity: Anonymity, fields?: unknown | null, countResponses: number, canRemoveResponses: boolean, protectResponses: boolean, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, isTechnical: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> }>, responses?: Array<{ __typename?: 'LimitedResponseType', id: string, sequenceNumber: number, revisionCreatedAt: string, language: string, values?: unknown | null, cachedDimensions?: unknown | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> | null } | null } | null } | null };

export type SurveySummaryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  filters?: InputMaybe<Array<DimensionFilterInput> | DimensionFilterInput>;
}>;


export type SurveySummaryQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', survey?: { __typename?: 'FullSurveyType', title?: string | null, fields?: unknown | null, summary?: unknown | null, countResponses: number, countFilteredResponses: number, dimensions: Array<{ __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> }> } | null } | null } | null };

export type CreateSurveyMutationVariables = Exact<{
  input: CreateSurveyInput;
}>;


export type CreateSurveyMutation = { __typename?: 'Mutation', createSurvey?: { __typename?: 'CreateSurvey', survey?: { __typename?: 'FullSurveyType', slug: string } | null } | null };

export type SurveyFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> };

export type ProfileSurveyFragment = { __typename?: 'FullSurveyType', slug: string, title?: string | null, event: { __typename?: 'LimitedEventType', slug: string, name: string } };

export type SurveysQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveysQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', forms: { __typename?: 'FormsProfileMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, event: { __typename?: 'LimitedEventType', slug: string, name: string } }> } } | null, event?: { __typename?: 'FullEventType', name: string, forms?: { __typename?: 'FormsEventMetaType', surveys: Array<{ __typename?: 'FullSurveyType', slug: string, title?: string | null, isActive: boolean, activeFrom?: string | null, activeUntil?: string | null, countResponses: number, languages: Array<{ __typename?: 'FormType', language: FormsFormLanguageChoices }> }> } | null } | null };

export type TicketsAdminReportsPageQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type TicketsAdminReportsPageQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', name: string, slug: string, timezone: string, tickets?: { __typename?: 'TicketsV2EventMetaType', reports: Array<{ __typename?: 'ReportType', slug: string, title: string, footer: string, rows: Array<Array<unknown | null>>, totalRow?: Array<unknown | null> | null, columns: Array<{ __typename?: 'ColumnType', slug: string, title: string, type: TypeOfColumn }> }> } | null } | null };

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


export type ProfileEncryptionKeysQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', keypairs?: Array<{ __typename?: 'KeyPairType', id: string, createdAt: string }> | null } | null };

export type ProfileOrderDetailQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  orderId: Scalars['String']['input'];
}>;


export type ProfileOrderDetailQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', tickets: { __typename?: 'TicketsV2ProfileMetaType', order?: { __typename?: 'ProfileOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, canPay: boolean, canCancel: boolean, products: Array<{ __typename?: 'OrderProductType', title: string, quantity: number, price: any }>, event: { __typename?: 'LimitedEventType', slug: string, name: string } } | null } } | null };

export type ConfirmEmailMutationVariables = Exact<{
  input: ConfirmEmailInput;
}>;


export type ConfirmEmailMutation = { __typename?: 'Mutation', confirmEmail?: { __typename?: 'ConfirmEmail', user?: { __typename?: 'LimitedUserType', email: string } | null } | null };

export type ProfileOrderFragment = { __typename?: 'ProfileOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, canPay: boolean, canCancel: boolean, event: { __typename?: 'LimitedEventType', slug: string, name: string } };

export type ProfileOrdersQueryVariables = Exact<{ [key: string]: never; }>;


export type ProfileOrdersQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', tickets: { __typename?: 'TicketsV2ProfileMetaType', haveUnlinkedOrders: boolean, orders: Array<{ __typename?: 'ProfileOrderType', id: string, formattedOrderNumber: string, createdAt: string, totalPrice: any, status: PaymentStatus, eticketsLink?: string | null, canPay: boolean, canCancel: boolean, event: { __typename?: 'LimitedEventType', slug: string, name: string } }> } } | null };

export type ProfileProgramItemFragment = { __typename?: 'FullProgramType', slug: string, title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string, timezone: string }, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, startTime: string, endTime: string, durationMinutes: number, location?: string | null, subtitle: string }> };

export type ProfileProgramItemListQueryVariables = Exact<{
  locale: Scalars['String']['input'];
}>;


export type ProfileProgramItemListQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', program: { __typename?: 'ProgramV2ProfileMetaType', programs?: Array<{ __typename?: 'FullProgramType', slug: string, title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string, timezone: string }, scheduleItems: Array<{ __typename?: 'LimitedScheduleItemType', slug: string, startTime: string, endTime: string, durationMinutes: number, location?: string | null, subtitle: string }> }> | null, programOffers: Array<{ __typename?: 'ProfileResponseType', id: string, revisionCreatedAt: string, canEdit: boolean, values?: unknown | null, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, form: { __typename?: 'FormType', title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string }, survey: { __typename?: 'FullSurveyType', slug: string } } }> } } | null };

export type ProfileSurveyEditResponseQueryVariables = Exact<{
  locale: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
}>;


export type ProfileSurveyEditResponseQuery = { __typename?: 'Query', userRegistry: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } }, profile?: { __typename?: 'OwnProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string, forms: { __typename?: 'FormsProfileMetaType', response?: { __typename?: 'ProfileResponseType', id: string, revisionCreatedAt: string, canEdit: boolean, values?: unknown | null, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, form: { __typename?: 'FormType', title: string, description: string, language: FormsFormLanguageChoices, fields?: unknown | null, event: { __typename?: 'LimitedEventType', slug: string, name: string, timezone: string }, survey: { __typename?: 'FullSurveyType', slug: string, registry?: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } } | null, profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } } } | null } } | null };

export type ProfileSurveyResponsePageQueryVariables = Exact<{
  locale: Scalars['String']['input'];
  responseId: Scalars['String']['input'];
}>;


export type ProfileSurveyResponsePageQuery = { __typename?: 'Query', userRegistry: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } }, profile?: { __typename?: 'OwnProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string, forms: { __typename?: 'FormsProfileMetaType', response?: { __typename?: 'ProfileResponseType', id: string, revisionCreatedAt: string, canEdit: boolean, values?: unknown | null, originalCreatedAt: string, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, form: { __typename?: 'FormType', title: string, description: string, language: FormsFormLanguageChoices, fields?: unknown | null, event: { __typename?: 'LimitedEventType', slug: string, name: string, timezone: string }, survey: { __typename?: 'FullSurveyType', profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean }, registry?: { __typename?: 'LimitedRegistryType', slug: string, title: string, policyUrl: string, organization: { __typename?: 'LimitedOrganizationType', slug: string, name: string } } | null } }, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> } | null } } | null };

export type ProfileResponsesTableRowFragment = { __typename?: 'ProfileResponseType', id: string, revisionCreatedAt: string, canEdit: boolean, values?: unknown | null, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, form: { __typename?: 'FormType', title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string }, survey: { __typename?: 'FullSurveyType', slug: string } } };

export type OwnFormResponsesQueryVariables = Exact<{
  locale: Scalars['String']['input'];
}>;


export type OwnFormResponsesQuery = { __typename?: 'Query', profile?: { __typename?: 'OwnProfileType', forms: { __typename?: 'FormsProfileMetaType', responses: Array<{ __typename?: 'ProfileResponseType', id: string, revisionCreatedAt: string, canEdit: boolean, values?: unknown | null, dimensions: Array<{ __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } }>, form: { __typename?: 'FormType', title: string, event: { __typename?: 'LimitedEventType', slug: string, name: string }, survey: { __typename?: 'FullSurveyType', slug: string } } }> } } | null };

export type AnnotationsFormAnnotationFragment = { __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string, description: string, isComputed: boolean };

export type UpdateProgramAnnotationsMutationVariables = Exact<{
  input: UpdateProgramAnnotationsInput;
}>;


export type UpdateProgramAnnotationsMutation = { __typename?: 'Mutation', updateProgramAnnotations?: { __typename?: 'UpdateProgramAnnotations', program?: { __typename?: 'FullProgramType', slug: string, cachedAnnotations: unknown } | null } | null };

export type GetProgramAnnotationSchemaQueryVariables = Exact<{
  locale: Scalars['String']['input'];
  eventSlug: Scalars['String']['input'];
  annotationSlugs?: InputMaybe<Array<Scalars['String']['input']> | Scalars['String']['input']>;
  publicOnly?: InputMaybe<Scalars['Boolean']['input']>;
}>;


export type GetProgramAnnotationSchemaQuery = { __typename?: 'Query', event?: { __typename?: 'FullEventType', program?: { __typename?: 'ProgramV2EventMetaType', annotations: Array<{ __typename?: 'AnnotationType', slug: string, type: AnnotationDataType, title: string, description: string, isComputed: boolean }> } | null } | null };

export type CachedDimensionsBadgesFragment = { __typename?: 'FullDimensionType', slug: string, title?: string | null, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> };

export type ColoredDimensionTableCellFragment = { __typename?: 'FullDimensionType', slug: string, title?: string | null, isKeyDimension: boolean, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string }> };

export type DimensionBadgeFragment = { __typename?: 'ResponseDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } };

export type DimensionEditorValueFragment = { __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string };

export type DimensionEditorFragment = { __typename?: 'FullDimensionType', slug: string, canRemove: boolean, canAddValues: boolean, title?: string | null, isPublic: boolean, isKeyDimension: boolean, isMultiValue: boolean, isListFilter: boolean, isShownInDetail: boolean, isNegativeSelection: boolean, isTechnical: boolean, valueOrdering: DimensionsDimensionValueOrderingChoices, titleFi: string, titleEn: string, titleSv: string, values: Array<{ __typename?: 'DimensionValueType', slug: string, color: string, isTechnical: boolean, isSubjectLocked: boolean, canRemove: boolean, title?: string | null, titleFi: string, titleEn: string, titleSv: string }> };

export type DimensionValueSelectFragment = { __typename?: 'FullDimensionType', slug: string, title?: string | null, isTechnical: boolean, isMultiValue: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> };

export type DimensionFilterValueFragment = { __typename?: 'DimensionValueType', slug: string, title?: string | null };

export type DimensionFilterFragment = { __typename?: 'FullDimensionType', slug: string, title?: string | null, isMultiValue: boolean, isListFilter: boolean, isKeyDimension: boolean, values: Array<{ __typename?: 'DimensionValueType', slug: string, title?: string | null }> };

export type FullOwnProfileFragment = { __typename?: 'OwnProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string };

export type FullSelectedProfileFragment = { __typename?: 'SelectedProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string };

export type FullLimitedProfileFragment = { __typename?: 'LimitedProfileType', firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string };

export type FullProfileFieldSelectorFragment = { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean };

export type ProgramDimensionBadgeFragment = { __typename?: 'ProgramDimensionValueType', dimension: { __typename?: 'FullDimensionType', slug: string, title?: string | null }, value: { __typename?: 'DimensionValueType', slug: string, title?: string | null, color: string } };

export type ReportFragment = { __typename?: 'ReportType', slug: string, title: string, footer: string, rows: Array<Array<unknown | null>>, totalRow?: Array<unknown | null> | null, columns: Array<{ __typename?: 'ColumnType', slug: string, title: string, type: TypeOfColumn }> };

export type ResponseRevisionFragment = { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null };

export type ResponseHistoryBannerFragment = { __typename?: 'FullResponseType', id: string, originalCreatedAt: string, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export type ProfileResponseHistoryBannerFragment = { __typename?: 'ProfileResponseType', id: string, originalCreatedAt: string, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export type ResponseHistorySidebarFragment = { __typename?: 'FullResponseType', id: string, originalCreatedAt: string, revisionCreatedAt: string, language: string, originalCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string, firstName: string, lastName: string, nick: string, email: string, phoneNumber: string, discordHandle: string } | null, revisionCreatedBy?: { __typename?: 'SelectedProfileType', fullName: string } | null, form: { __typename?: 'FormType', survey: { __typename?: 'FullSurveyType', profileFieldSelector: { __typename?: 'ProfileFieldSelectorType', firstName: boolean, lastName: boolean, nick: boolean, email: boolean, phoneNumber: boolean, discordHandle: boolean } } }, supersededBy?: { __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null } | null, oldVersions: Array<{ __typename?: 'LimitedResponseType', id: string, revisionCreatedAt: string, revisionCreatedBy?: { __typename?: 'SelectedProfileType', displayName: string } | null }> };

export const TransferConsentFormRegistryFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"TransferConsentFormRegistry"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedRegistryType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"organization"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"policyUrl"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<TransferConsentFormRegistryFragment, unknown>;
export const AdminOrderPaymentStampFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderPaymentStamp"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedPaymentStampType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"provider"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"data"}}]}}]} as unknown as DocumentNode<AdminOrderPaymentStampFragment, unknown>;
export const AdminOrderReceiptFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderReceipt"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedReceiptType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}}]} as unknown as DocumentNode<AdminOrderReceiptFragment, unknown>;
export const AdminOrderCodeFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderCode"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedCodeType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"literateCode"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"usedOn"}},{"kind":"Field","name":{"kind":"Name","value":"productText"}}]}}]} as unknown as DocumentNode<AdminOrderCodeFragment, unknown>;
export const NewOrderProductFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"NewOrderProduct"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"isAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}}]} as unknown as DocumentNode<NewOrderProductFragment, unknown>;
export const OrderListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OrderList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}}]} as unknown as DocumentNode<OrderListFragment, unknown>;
export const ProductChoiceFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductChoice"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]} as unknown as DocumentNode<ProductChoiceFragment, unknown>;
export const FullProfileFieldSelectorFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<FullProfileFieldSelectorFragment, unknown>;
export const InvolvedPersonDetailInvolvementFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonDetailInvolvement"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"adminLink"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}}]} as unknown as DocumentNode<InvolvedPersonDetailInvolvementFragment, unknown>;
export const InvolvedPersonDetailFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileWithInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"involvements"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"InvolvedPersonDetailInvolvement"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonDetailInvolvement"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"adminLink"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}}]} as unknown as DocumentNode<InvolvedPersonDetailFragment, unknown>;
export const InvolvedPersonInvolvementFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonInvolvement"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"adminLink"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}}]} as unknown as DocumentNode<InvolvedPersonInvolvementFragment, unknown>;
export const InvolvedPersonFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPerson"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileWithInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"involvements"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"InvolvedPersonInvolvement"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonInvolvement"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"adminLink"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}}]} as unknown as DocumentNode<InvolvedPersonFragment, unknown>;
export const AdminProductOldVersionFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductOldVersion"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}}]} as unknown as DocumentNode<AdminProductOldVersionFragment, unknown>;
export const AdminProductDetailFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminProductOldVersion"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductOldVersion"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}}]} as unknown as DocumentNode<AdminProductDetailFragment, unknown>;
export const ProductListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"isAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}}]}}]} as unknown as DocumentNode<ProductListFragment, unknown>;
export const ProgramAdminDetailHostFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminDetailHost"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramHostType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"programHostRole"}},{"kind":"Field","name":{"kind":"Name","value":"person"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminDetailHostFragment, unknown>;
export const ProgramAdminDetailInvitationFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminDetailInvitation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvitationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramAdminDetailInvitationFragment, unknown>;
export const ProgramAdminDetailScheduleItemFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminDetailScheduleItem"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedScheduleItemType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"durationMinutes"}},{"kind":"Field","name":{"kind":"Name","value":"room"}},{"kind":"Field","name":{"kind":"Name","value":"freeformLocation"}},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}}]}}]} as unknown as DocumentNode<ProgramAdminDetailScheduleItemFragment, unknown>;
export const ProgramAdminFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdmin"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"startTime"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramAdminFragment, unknown>;
export const ProgramAdminEventAnnotationFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminEventAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedUniverseAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isInternal"}},{"kind":"Field","name":{"kind":"Name","value":"isApplicableToProgramItems"}},{"kind":"Field","name":{"kind":"Name","value":"isApplicableToScheduleItems"}}]}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"formFields"}}]}}]} as unknown as DocumentNode<ProgramAdminEventAnnotationFragment, unknown>;
export const EditProgramFormLanguageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramFormLanguage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormLanguageFragment, unknown>;
export const EditProgramFormFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormFragment, unknown>;
export const ProgramFormResponseFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramFormResponse"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramFormResponseFragment, unknown>;
export const OfferFormFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OfferForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<OfferFormFragment, unknown>;
export const ProgramAdminHostFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminHost"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramHostType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"person"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminHostFragment, unknown>;
export const ProgramAdminInvitationFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminInvitation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullInvitationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminInvitationFragment, unknown>;
export const FullSelectedProfileFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<FullSelectedProfileFragment, unknown>;
export const ResponseRevisionFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}}]} as unknown as DocumentNode<ResponseRevisionFragment, unknown>;
export const ProgramOfferEditFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferEdit"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultResponseDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}}]} as unknown as DocumentNode<ProgramOfferEditFragment, unknown>;
export const ResponseHistorySidebarFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistorySidebar"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}}]} as unknown as DocumentNode<ResponseHistorySidebarFragment, unknown>;
export const DimensionBadgeFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<DimensionBadgeFragment, unknown>;
export const ProgramOfferDetailFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseHistorySidebar"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultResponseDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultInvolvementDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]},{"kind":"Field","name":{"kind":"Name","value":"canAccept"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistorySidebar"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ProgramOfferDetailFragment, unknown>;
export const ProgramOfferFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOffer"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramOfferFragment, unknown>;
export const DimensionFilterValueFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<DimensionFilterValueFragment, unknown>;
export const DimensionFilterFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<DimensionFilterFragment, unknown>;
export const ColoredDimensionTableCellFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ColoredDimensionTableCell"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ColoredDimensionTableCellFragment, unknown>;
export const DimensionValueSelectFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}}]} as unknown as DocumentNode<DimensionValueSelectFragment, unknown>;
export const ProgramOfferDimensionFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDimension"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"ColoredDimensionTableCell"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ColoredDimensionTableCell"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}}]} as unknown as DocumentNode<ProgramOfferDimensionFragment, unknown>;
export const ScheduleProgramFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleProgram"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"listFiltersOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isCancelled"}}]}}]} as unknown as DocumentNode<ScheduleProgramFragment, unknown>;
export const ScheduleItemListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleItemList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullScheduleItemType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleProgram"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleProgram"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"listFiltersOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isCancelled"}}]}}]} as unknown as DocumentNode<ScheduleItemListFragment, unknown>;
export const ProgramDetailAnnotationFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDetailAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<ProgramDetailAnnotationFragment, unknown>;
export const QuotaProductFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaProduct"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}}]}}]} as unknown as DocumentNode<QuotaProductFragment, unknown>;
export const QuotaListFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullQuotaType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","alias":{"kind":"Name","value":"title"},"name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"countTotal"}}]}}]} as unknown as DocumentNode<QuotaListFragment, unknown>;
export const DimensionEditorValueFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}}]} as unknown as DocumentNode<DimensionEditorValueFragment, unknown>;
export const DimensionEditorFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}}]} as unknown as DocumentNode<DimensionEditorFragment, unknown>;
export const EditSurveyFieldsPageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyFieldsPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}}]} as unknown as DocumentNode<EditSurveyFieldsPageFragment, unknown>;
export const EditFormLanguagePageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditFormLanguagePage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditFormLanguagePageFragment, unknown>;
export const EditSurveyPageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"loginRequired"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"maxResponsesPerUser"}},{"kind":"Field","name":{"kind":"Name","value":"countResponsesByCurrentUser"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"responsesEditableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditSurveyPageFragment, unknown>;
export const ResponseHistoryBannerFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistoryBanner"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}}]} as unknown as DocumentNode<ResponseHistoryBannerFragment, unknown>;
export const EditSurveyResponsePageFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyResponsePage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseHistoryBanner"}},{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistoryBanner"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<EditSurveyResponsePageFragment, unknown>;
export const SurveyResponseDetailFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"SurveyResponseDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseHistorySidebar"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]},{"kind":"Field","name":{"kind":"Name","value":"canAccept"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistorySidebar"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}}]}}]} as unknown as DocumentNode<SurveyResponseDetailFragment, unknown>;
export const SurveyResponseFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"SurveyResponse"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}]}]}}]} as unknown as DocumentNode<SurveyResponseFragment, unknown>;
export const SurveyFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Survey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<SurveyFragment, unknown>;
export const ProfileSurveyFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileSurvey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<ProfileSurveyFragment, unknown>;
export const ProfileEncryptionKeysFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileEncryptionKeys"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"KeyPairType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}}]}}]} as unknown as DocumentNode<ProfileEncryptionKeysFragment, unknown>;
export const ProfileOrderFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileOrder"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"canPay"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]} as unknown as DocumentNode<ProfileOrderFragment, unknown>;
export const ProfileProgramItemFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileProgramItem"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}},{"kind":"Field","name":{"kind":"Name","value":"durationMinutes"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}}]}}]}}]} as unknown as DocumentNode<ProfileProgramItemFragment, unknown>;
export const ProfileResponsesTableRowFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponsesTableRow"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"OWNER"}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<ProfileResponsesTableRowFragment, unknown>;
export const AnnotationsFormAnnotationFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AnnotationsFormAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}}]}}]} as unknown as DocumentNode<AnnotationsFormAnnotationFragment, unknown>;
export const CachedDimensionsBadgesFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"CachedDimensionsBadges"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<CachedDimensionsBadgesFragment, unknown>;
export const FullOwnProfileFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullOwnProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"OwnProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<FullOwnProfileFragment, unknown>;
export const FullLimitedProfileFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullLimitedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<FullLimitedProfileFragment, unknown>;
export const ProgramDimensionBadgeFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ProgramDimensionBadgeFragment, unknown>;
export const ReportFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Report"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ReportType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"footer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"columns"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"type"}}]}},{"kind":"Field","name":{"kind":"Name","value":"rows"}},{"kind":"Field","name":{"kind":"Name","value":"totalRow"}}]}}]} as unknown as DocumentNode<ReportFragment, unknown>;
export const ProfileResponseHistoryBannerFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponseHistoryBanner"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}}]} as unknown as DocumentNode<ProfileResponseHistoryBannerFragment, unknown>;
export const CreateSurveyResponseDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateSurveyResponse"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyResponseInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyResponse"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateSurveyResponseMutation, CreateSurveyResponseMutationVariables>;
export const InitFileUploadMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"InitFileUploadMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"InitFileUploadInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"initFileUpload"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"uploadUrl"}},{"kind":"Field","name":{"kind":"Name","value":"fileUrl"}}]}}]}}]} as unknown as DocumentNode<InitFileUploadMutationMutation, InitFileUploadMutationMutationVariables>;
export const SurveyPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullOwnProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"userRegistry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"NullValue"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"loginRequired"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"maxResponsesPerUser"}},{"kind":"Field","name":{"kind":"Name","value":"countResponsesByCurrentUser"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}},{"kind":"Field","name":{"kind":"Name","value":"registry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullOwnProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"OwnProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"TransferConsentFormRegistry"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedRegistryType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"organization"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"policyUrl"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<SurveyPageQueryQuery, SurveyPageQueryQueryVariables>;
export const SurveyThankYouPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyThankYouPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveyThankYouPageQueryQuery, SurveyThankYouPageQueryQueryVariables>;
export const AcceptInvitationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"AcceptInvitation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"AcceptInvitationInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"acceptInvitation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]}}]} as unknown as DocumentNode<AcceptInvitationMutation, AcceptInvitationMutationVariables>;
export const AcceptInvitationPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AcceptInvitationPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"invitationId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullOwnProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"userRegistry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"invitation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"invitationId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"invitationId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"isUsed"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}},{"kind":"Field","name":{"kind":"Name","value":"registry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullOwnProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"OwnProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"TransferConsentFormRegistry"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedRegistryType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"organization"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"policyUrl"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<AcceptInvitationPageQuery, AcceptInvitationPageQueryVariables>;
export const PutInvolvementDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutInvolvementDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutInvolvementDimensionMutation, PutInvolvementDimensionMutationVariables>;
export const DeleteInvolvementDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteInvolvementDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteInvolvementDimensionMutation, DeleteInvolvementDimensionMutationVariables>;
export const PutInvolvementDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutInvolvementDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutInvolvementDimensionValueMutation, PutInvolvementDimensionValueMutationVariables>;
export const DeleteInvolvementDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteInvolvementDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteInvolvementDimensionValueMutation, DeleteInvolvementDimensionValueMutationVariables>;
export const InvolvementDimensionsListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"InvolvementDimensionsList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}}]} as unknown as DocumentNode<InvolvementDimensionsListQuery, InvolvementDimensionsListQueryVariables>;
export const InvolvementAdminReportsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"InvolvementAdminReportsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"reports"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"Report"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Report"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ReportType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"footer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"columns"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"type"}}]}},{"kind":"Field","name":{"kind":"Name","value":"rows"}},{"kind":"Field","name":{"kind":"Name","value":"totalRow"}}]}}]} as unknown as DocumentNode<InvolvementAdminReportsPageQuery, InvolvementAdminReportsPageQueryVariables>;
export const ResendOrderConfirmationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ResendOrderConfirmation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ResendOrderConfirmationInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"resendOrderConfirmation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<ResendOrderConfirmationMutation, ResendOrderConfirmationMutationVariables>;
export const UpdateOrderDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateOrder"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateOrderInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateOrder"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateOrderMutation, UpdateOrderMutationVariables>;
export const CancelAndRefundOrderDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CancelAndRefundOrder"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CancelAndRefundOrderInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"cancelAndRefundOrder"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CancelAndRefundOrderMutation, CancelAndRefundOrderMutationVariables>;
export const MarkOrderAsPaidDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"MarkOrderAsPaid"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"MarkOrderAsPaidInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"markOrderAsPaid"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<MarkOrderAsPaidMutation, MarkOrderAsPaidMutationVariables>;
export const AdminOrderDetailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminOrderDetail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phone"}},{"kind":"Field","name":{"kind":"Name","value":"canRefund"}},{"kind":"Field","name":{"kind":"Name","value":"canRefundManually"}},{"kind":"Field","name":{"kind":"Name","value":"canMarkAsPaid"}},{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"quantity"}},{"kind":"Field","name":{"kind":"Name","value":"price"}}]}},{"kind":"Field","name":{"kind":"Name","value":"paymentStamps"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminOrderPaymentStamp"}}]}},{"kind":"Field","name":{"kind":"Name","value":"receipts"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminOrderReceipt"}}]}},{"kind":"Field","name":{"kind":"Name","value":"codes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminOrderCode"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderPaymentStamp"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedPaymentStampType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"provider"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"data"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderReceipt"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedReceiptType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"correlationId"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminOrderCode"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedCodeType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"literateCode"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"usedOn"}},{"kind":"Field","name":{"kind":"Name","value":"productText"}}]}}]} as unknown as DocumentNode<AdminOrderDetailQuery, AdminOrderDetailQueryVariables>;
export const AdminCreateOrderDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"AdminCreateOrder"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateOrderInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createOrder"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}},{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<AdminCreateOrderMutation, AdminCreateOrderMutationVariables>;
export const NewOrderPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"NewOrderPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"NewOrderProduct"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"NewOrderProduct"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"isAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}}]} as unknown as DocumentNode<NewOrderPageQuery, NewOrderPageQueryVariables>;
export const AdminOrderListWithOrdersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminOrderListWithOrders"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"search"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"returnNone"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Boolean"}},"defaultValue":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProductChoice"}}]}},{"kind":"Field","name":{"kind":"Name","value":"orders"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"search"},"value":{"kind":"Variable","name":{"kind":"Name","value":"search"}}},{"kind":"Argument","name":{"kind":"Name","value":"returnNone"},"value":{"kind":"Variable","name":{"kind":"Name","value":"returnNone"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"OrderList"}}]}},{"kind":"Field","name":{"kind":"Name","value":"countTotalOrders"}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductChoice"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OrderList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}}]}}]} as unknown as DocumentNode<AdminOrderListWithOrdersQuery, AdminOrderListWithOrdersQueryVariables>;
export const CancelOwnOrderDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CancelOwnOrder"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CancelOwnUnpaidOrderInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"cancelOwnUnpaidOrder"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CancelOwnOrderMutation, CancelOwnOrderMutationVariables>;
export const PersonPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"PersonPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"personId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"CachedDimensionsBadges"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}}]}},{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}},{"kind":"Argument","name":{"kind":"Name","value":"perksOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AnnotationsFormAnnotation"}}]}},{"kind":"Field","name":{"kind":"Name","value":"person"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"personId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"InvolvedPersonDetail"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonDetailInvolvement"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"adminLink"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"CachedDimensionsBadges"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AnnotationsFormAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileWithInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"involvements"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"InvolvedPersonDetailInvolvement"}}]}}]}}]} as unknown as DocumentNode<PersonPageQuery, PersonPageQueryVariables>;
export const PeoplePageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"PeoplePage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"search"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"returnNone"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Boolean"}},"defaultValue":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"CachedDimensionsBadges"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"people"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"search"},"value":{"kind":"Variable","name":{"kind":"Name","value":"search"}}},{"kind":"Argument","name":{"kind":"Name","value":"returnNone"},"value":{"kind":"Variable","name":{"kind":"Name","value":"returnNone"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"InvolvedPerson"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPersonInvolvement"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"adminLink"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"CachedDimensionsBadges"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"InvolvedPerson"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileWithInvolvementType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"involvements"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"InvolvedPersonInvolvement"}}]}}]}}]} as unknown as DocumentNode<PeoplePageQuery, PeoplePageQueryVariables>;
export const UpdateProductDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProduct"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateProductInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProduct"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"product"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProductMutation, UpdateProductMutationVariables>;
export const DeleteProductDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProduct"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteProductInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteProduct"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<DeleteProductMutation, DeleteProductMutationVariables>;
export const AdminProductDetailPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminProductDetailPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"productId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countTotal"}}]}},{"kind":"Field","name":{"kind":"Name","value":"product"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"productId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminProductDetail"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductOldVersion"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AdminProductDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsPerProduct"}},{"kind":"Field","name":{"kind":"Name","value":"maxPerOrder"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AdminProductOldVersion"}}]}}]}}]} as unknown as DocumentNode<AdminProductDetailPageQuery, AdminProductDetailPageQueryVariables>;
export const CreateProductDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProduct"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateProductInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProduct"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"product"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProductMutation, CreateProductMutationVariables>;
export const ReorderProductsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ReorderProducts"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ReorderProductsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"reorderProducts"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<ReorderProductsMutation, ReorderProductsMutationVariables>;
export const ProductListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProductList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProductList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProductList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"isAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"availableFrom"}},{"kind":"Field","name":{"kind":"Name","value":"availableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}}]}}]} as unknown as DocumentNode<ProductListQuery, ProductListQueryVariables>;
export const UpdateProgramBasicInfoDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramBasicInfo"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateProgramInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProgram"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramBasicInfoMutation, UpdateProgramBasicInfoMutationVariables>;
export const CancelProgramItemDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CancelProgramItem"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CancelProgramInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"cancelProgram"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"responseId"}}]}}]}}]} as unknown as DocumentNode<CancelProgramItemMutation, CancelProgramItemMutationVariables>;
export const RestoreProgramItemDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"RestoreProgramItem"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"RestoreProgramInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"restoreProgram"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"programSlug"}}]}}]}}]} as unknown as DocumentNode<RestoreProgramItemMutation, RestoreProgramItemMutationVariables>;
export const ProgramAdminDetailAnnotationsQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminDetailAnnotationsQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AnnotationsFormAnnotation"}},{"kind":"Field","name":{"kind":"Name","value":"isApplicableToProgramItems"}}]}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDimensionBadge"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AnnotationsFormAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminDetailAnnotationsQueryQuery, ProgramAdminDetailAnnotationsQueryQueryVariables>;
export const UpdateProgramDimensionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramDimensions"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateProgramDimensionsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProgramDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramDimensionsMutation, UpdateProgramDimensionsMutationVariables>;
export const ProgramAdminDetailDimensionsQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminDetailDimensionsQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDimensionBadge"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminDetailDimensionsQueryQuery, ProgramAdminDetailDimensionsQueryQueryVariables>;
export const InviteProgramHostDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"InviteProgramHost"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"InviteProgramHostInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"inviteProgramHost"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"invitation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<InviteProgramHostMutation, InviteProgramHostMutationVariables>;
export const DeleteProgramHostDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramHost"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteProgramHostInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteProgramHost"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<DeleteProgramHostMutation, DeleteProgramHostMutationVariables>;
export const UpdateProgramHostDimensionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramHostDimensions"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateInvolvementDimensionsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateInvolvementDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"involvement"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramHostDimensionsMutation, UpdateProgramHostDimensionsMutationVariables>;
export const DeleteInvitationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteInvitation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteInvitationInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteInvitation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"invitation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<DeleteInvitationMutation, DeleteInvitationMutationVariables>;
export const ResendInvitationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ResendInvitation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ResendInvitationInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"resendInvitation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"invitation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<ResendInvitationMutation, ResendInvitationMutationVariables>;
export const ProgramAdminDetailHostsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminDetailHosts"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"annotationSlugs"}},"type":{"kind":"NonNullType","type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"inviteForms"},"name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"includeInactive"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}},{"kind":"Argument","name":{"kind":"Name","value":"purpose"},"value":{"kind":"EnumValue","value":"INVITE"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultInvolvementDimensions"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"involvementDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ColoredDimensionTableCell"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"annotationSlugs"}}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AnnotationsFormAnnotation"}}]}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"canInviteProgramHost"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"annotationSlugs"}}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"programHosts"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"includeInactive"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdminDetailHost"}}]}},{"kind":"Field","name":{"kind":"Name","value":"invitations"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdminDetailInvitation"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ColoredDimensionTableCell"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AnnotationsFormAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminDetailHost"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramHostType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"programHostRole"}},{"kind":"Field","name":{"kind":"Name","value":"person"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminDetailInvitation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedInvitationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramAdminDetailHostsQuery, ProgramAdminDetailHostsQueryVariables>;
export const ProgramAdminDetailQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminDetailQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"calendarExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"cachedHosts"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"canRestore"}},{"kind":"Field","name":{"kind":"Name","value":"programOffer"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"values"}}]}},{"kind":"Field","name":{"kind":"Name","value":"links"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"href"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDetailAnnotation"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"location"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDetailAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminDetailQueryQuery, ProgramAdminDetailQueryQueryVariables>;
export const PutScheduleItemDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutScheduleItem"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutScheduleItemInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putScheduleItem"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"scheduleItem"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutScheduleItemMutation, PutScheduleItemMutationVariables>;
export const DeleteScheduleItemDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteScheduleItem"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteScheduleItemInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteScheduleItem"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteScheduleItemMutation, DeleteScheduleItemMutationVariables>;
export const ProgramAdminDetailScheduleDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminDetailSchedule"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdminDetailScheduleItem"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminDetailScheduleItem"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedScheduleItemType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"durationMinutes"}},{"kind":"Field","name":{"kind":"Name","value":"room"}},{"kind":"Field","name":{"kind":"Name","value":"freeformLocation"}},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}}]}}]} as unknown as DocumentNode<ProgramAdminDetailScheduleQuery, ProgramAdminDetailScheduleQueryVariables>;
export const CreateProgramDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProgram"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateProgramInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProgram"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProgramMutation, CreateProgramMutationVariables>;
export const ProgramAdminListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"scheduleItemsExcelExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdmin"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdmin"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"startTime"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]} as unknown as DocumentNode<ProgramAdminListQuery, ProgramAdminListQueryVariables>;
export const PutEventAnnotationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutEventAnnotation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutUniverseAnnotationInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putUniverseAnnotation"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"universeAnnotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]}}]} as unknown as DocumentNode<PutEventAnnotationMutation, PutEventAnnotationMutationVariables>;
export const ProgramAdminEventAnnotationsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminEventAnnotations"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"eventAnnotations"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdminEventAnnotation"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminEventAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedUniverseAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isInternal"}},{"kind":"Field","name":{"kind":"Name","value":"isApplicableToProgramItems"}},{"kind":"Field","name":{"kind":"Name","value":"isApplicableToScheduleItems"}}]}},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"formFields"}}]}}]} as unknown as DocumentNode<ProgramAdminEventAnnotationsQuery, ProgramAdminEventAnnotationsQueryVariables>;
export const PutProgramDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutProgramDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutProgramDimensionMutation, PutProgramDimensionMutationVariables>;
export const DeleteProgramDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramDimensionMutation, DeleteProgramDimensionMutationVariables>;
export const PutProgramDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutProgramDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutProgramDimensionValueMutation, PutProgramDimensionValueMutationVariables>;
export const DeleteProgramDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramDimensionValueMutation, DeleteProgramDimensionValueMutationVariables>;
export const ProgramDimensionsListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramDimensionsList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}}]} as unknown as DocumentNode<ProgramDimensionsListQuery, ProgramDimensionsListQueryVariables>;
export const UpdateProgramFormDefaultDimensionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramFormDefaultDimensions"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateSurveyDefaultDimensionsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateSurveyDefaultDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramFormDefaultDimensionsMutation, UpdateProgramFormDefaultDimensionsMutationVariables>;
export const DimensionDefaultsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"DimensionDefaults"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"involvementDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultResponseDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultInvolvementDimensions"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}}]} as unknown as DocumentNode<DimensionDefaultsQuery, DimensionDefaultsQueryVariables>;
export const UpdateProgramFormLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramFormLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateFormInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramFormLanguageMutation, UpdateProgramFormLanguageMutationVariables>;
export const DeleteProgramFormLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramFormLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramFormLanguageMutation, DeleteProgramFormLanguageMutationVariables>;
export const UpdateFormFieldsMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateFormFieldsMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateFormFieldsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateFormFields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateFormFieldsMutationMutation, UpdateFormFieldsMutationMutationVariables>;
export const PromoteProgramFormFieldToDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PromoteProgramFormFieldToDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PromoteFieldToDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"promoteFieldToDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PromoteProgramFormFieldToDimensionMutation, PromoteProgramFormFieldToDimensionMutationVariables>;
export const EditProgramFormFieldsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditProgramFormFieldsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditSurveyFieldsPage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyFieldsPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormFieldsPageQuery, EditProgramFormFieldsPageQueryVariables>;
export const EditProgramFormLanguagePageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditProgramFormLanguagePage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditProgramFormLanguage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramFormLanguage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormLanguagePageQuery, EditProgramFormLanguagePageQueryVariables>;
export const CreateProgramFormLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProgramFormLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProgramFormLanguageMutation, CreateProgramFormLanguageMutationVariables>;
export const UpdateProgramFormMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramFormMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProgramForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramFormMutationMutation, UpdateProgramFormMutationMutationVariables>;
export const DeleteProrgamFormMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProrgamFormMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteProrgamFormMutationMutation, DeleteProrgamFormMutationMutationVariables>;
export const EditProgramFormPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditProgramFormPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditProgramForm"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditProgramForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditProgramFormPageQuery, EditProgramFormPageQueryVariables>;
export const ProgramFormResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramFormResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}},{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"ColoredDimensionTableCell"}}]}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"canRemoveResponses"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"responses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramFormResponse"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ColoredDimensionTableCell"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramFormResponse"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramFormResponsesQuery, ProgramFormResponsesQueryVariables>;
export const CreateProgramFormDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateProgramForm"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateProgramFormInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProgramForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<CreateProgramFormMutation, CreateProgramFormMutationVariables>;
export const ProgramFormsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramFormsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"relation"},"value":{"kind":"EnumValue","value":"ACCESSIBLE"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileSurvey"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"includeInactive"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"PROGRAM_V2"}},{"kind":"Argument","name":{"kind":"Name","value":"purpose"},"value":{"kind":"ListValue","values":[{"kind":"EnumValue","value":"DEFAULT"},{"kind":"EnumValue","value":"INVITE"}]}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"OfferForm"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileSurvey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"OfferForm"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<ProgramFormsPageQuery, ProgramFormsPageQueryVariables>;
export const ProgramAdminHostsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminHosts"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"programHostsExcelExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isListFilter"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}}]}},{"kind":"Field","name":{"kind":"Name","value":"programHosts"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"programFilters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdminHost"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminHost"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramHostType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"person"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminHostsQuery, ProgramAdminHostsQueryVariables>;
export const ProgramAdminInvitationsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminInvitations"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"invitations"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramAdminInvitation"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramAdminInvitation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullInvitationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramAdminInvitationsQuery, ProgramAdminInvitationsQueryVariables>;
export const AcceptProgramOfferDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"AcceptProgramOffer"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"AcceptProgramOfferInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"acceptProgramOffer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<AcceptProgramOfferMutation, AcceptProgramOfferMutationVariables>;
export const CancelProgramOfferDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CancelProgramOffer"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CancelProgramOfferInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"cancelProgramOffer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"responseId"}}]}}]}}]} as unknown as DocumentNode<CancelProgramOfferMutation, CancelProgramOfferMutationVariables>;
export const EditProgramOfferDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"EditProgramOffer"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyResponseInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyResponse"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<EditProgramOfferMutation, EditProgramOfferMutationVariables>;
export const ProgramOfferEditPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramOfferEditPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"programOffer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferEdit"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferEdit"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultResponseDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]}]}}]} as unknown as DocumentNode<ProgramOfferEditPageQuery, ProgramOfferEditPageQueryVariables>;
export const ProgramOfferPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramOfferPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"involvementDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"programOffer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDetail"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistorySidebar"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseHistorySidebar"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultResponseDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultInvolvementDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]},{"kind":"Field","name":{"kind":"Name","value":"canAccept"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}}]}}]} as unknown as DocumentNode<ProgramOfferPageQuery, ProgramOfferPageQueryVariables>;
export const DeleteProgramOffersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteProgramOffers"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteProgramOffersInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteProgramOffers"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"countDeleted"}}]}}]}}]} as unknown as DocumentNode<DeleteProgramOffersMutation, DeleteProgramOffersMutationVariables>;
export const ProgramOffersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramOffers"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"programOffersExcelExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"canDeleteProgramOffers"}},{"kind":"Field","alias":{"kind":"Name","value":"listFilters"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isListFilter"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDimension"}}]}},{"kind":"Field","alias":{"kind":"Name","value":"keyDimensions"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDimension"}}]}},{"kind":"Field","name":{"kind":"Name","value":"stateDimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOfferDimension"}}]}},{"kind":"Field","name":{"kind":"Name","value":"countProgramOffers"}},{"kind":"Field","name":{"kind":"Name","value":"programOffers"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramOffer"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ColoredDimensionTableCell"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOfferDimension"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"ColoredDimensionTableCell"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramOffer"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"programs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}}]}}]} as unknown as DocumentNode<ProgramOffersQuery, ProgramOffersQueryVariables>;
export const ProgramAdminReportsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramAdminReportsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"reports"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"Report"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Report"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ReportType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"footer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"columns"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"type"}}]}},{"kind":"Field","name":{"kind":"Name","value":"rows"}},{"kind":"Field","name":{"kind":"Name","value":"totalRow"}}]}}]} as unknown as DocumentNode<ProgramAdminReportsPageQuery, ProgramAdminReportsPageQueryVariables>;
export const MarkScheduleItemAsFavoriteDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"MarkScheduleItemAsFavorite"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"FavoriteScheduleItemInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"markScheduleItemAsFavorite"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<MarkScheduleItemAsFavoriteMutation, MarkScheduleItemAsFavoriteMutationVariables>;
export const UnmarkScheduleItemAsFavoriteDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UnmarkScheduleItemAsFavorite"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"FavoriteScheduleItemInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"unmarkScheduleItemAsFavorite"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<UnmarkScheduleItemAsFavoriteMutation, UnmarkScheduleItemAsFavoriteMutationVariables>;
export const ProgramListQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramListQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"hidePast"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Boolean"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"hidePast"},"value":{"kind":"Variable","name":{"kind":"Name","value":"hidePast"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleItemList"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"calendarExportLink"}},{"kind":"Field","alias":{"kind":"Name","value":"listFilters"},"name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isListFilter"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}},{"kind":"Argument","name":{"kind":"Name","value":"hidePast"},"value":{"kind":"Variable","name":{"kind":"Name","value":"hidePast"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleItemList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleProgram"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"listFiltersOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isCancelled"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ScheduleItemList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullScheduleItemType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ScheduleProgram"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}}]} as unknown as DocumentNode<ProgramListQueryQuery, ProgramListQueryQueryVariables>;
export const CreateFeedbackDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateFeedback"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramFeedbackInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createProgramFeedback"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<CreateFeedbackMutation, CreateFeedbackMutationVariables>;
export const ProgramFeedbackQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramFeedbackQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"isAcceptingFeedback"}}]}}]}}]}}]}}]} as unknown as DocumentNode<ProgramFeedbackQueryQuery, ProgramFeedbackQueryQueryVariables>;
export const ProgramDetailQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgramDetailQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"calendarExportLink"}},{"kind":"Field","name":{"kind":"Name","value":"program"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"programSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"cachedHosts"}},{"kind":"Field","name":{"kind":"Name","value":"isCancelled"}},{"kind":"Field","name":{"kind":"Name","value":"links"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"href"}},{"kind":"Field","name":{"kind":"Name","value":"title"}}]}},{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProgramDetailAnnotation"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"isShownInDetail"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProgramDetailAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProgramAnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]} as unknown as DocumentNode<ProgramDetailQueryQuery, ProgramDetailQueryQueryVariables>;
export const UpdateQuotaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateQuota"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateQuotaInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateQuota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quota"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateQuotaMutation, UpdateQuotaMutationVariables>;
export const DeleteQuotaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteQuota"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteQuotaInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteQuota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<DeleteQuotaMutation, DeleteQuotaMutationVariables>;
export const AdminQuotaDetailPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"AdminQuotaDetailPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"quotaId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"quotaId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","alias":{"kind":"Name","value":"quota"},"name":{"kind":"Name","value":"countTotal"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}},{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"QuotaProduct"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaProduct"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedProductType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"price"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}}]}}]} as unknown as DocumentNode<AdminQuotaDetailPageQuery, AdminQuotaDetailPageQueryVariables>;
export const CreateQuotaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateQuota"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateQuotaInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createQuota"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quota"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateQuotaMutation, CreateQuotaMutationVariables>;
export const QuotaListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"QuotaList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"quotas"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"QuotaList"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"QuotaList"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullQuotaType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","alias":{"kind":"Name","value":"title"},"name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"countPaid"}},{"kind":"Field","name":{"kind":"Name","value":"countReserved"}},{"kind":"Field","name":{"kind":"Name","value":"countAvailable"}},{"kind":"Field","name":{"kind":"Name","value":"countTotal"}}]}}]} as unknown as DocumentNode<QuotaListQuery, QuotaListQueryVariables>;
export const UpdateSurveyDefaultDimensionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateSurveyDefaultDimensions"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateSurveyDefaultDimensionsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateSurveyDefaultDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateSurveyDefaultDimensionsMutation, UpdateSurveyDefaultDimensionsMutationVariables>;
export const SurveyDimensionDefaultsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyDimensionDefaults"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}},{"kind":"Field","name":{"kind":"Name","value":"cachedDefaultResponseDimensions"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}}]} as unknown as DocumentNode<SurveyDimensionDefaultsQuery, SurveyDimensionDefaultsQueryVariables>;
export const PutSurveyDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutSurveyDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutSurveyDimensionMutation, PutSurveyDimensionMutationVariables>;
export const DeleteSurveyDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyDimensionMutation, DeleteSurveyDimensionMutationVariables>;
export const PutSurveyDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PutSurveyDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PutDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"putDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PutSurveyDimensionValueMutation, PutSurveyDimensionValueMutationVariables>;
export const DeleteSurveyDimensionValueDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyDimensionValue"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteDimensionValueInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteDimensionValue"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyDimensionValueMutation, DeleteSurveyDimensionValueMutationVariables>;
export const DimensionsListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"DimensionsList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}}]} as unknown as DocumentNode<DimensionsListQuery, DimensionsListQueryVariables>;
export const UpdateFormMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateFormMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateFormInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateFormMutationMutation, UpdateFormMutationMutationVariables>;
export const DeleteSurveyLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyLanguageMutation, DeleteSurveyLanguageMutationVariables>;
export const PromoteSurveyFieldToDimensionDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"PromoteSurveyFieldToDimension"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"PromoteFieldToDimensionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"promoteFieldToDimension"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<PromoteSurveyFieldToDimensionMutation, PromoteSurveyFieldToDimensionMutationVariables>;
export const EditSurveyFieldsPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditSurveyFieldsPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditSurveyFieldsPage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditorValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isSubjectLocked"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionEditor"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"canAddValues"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isPublic"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isShownInDetail"}},{"kind":"Field","name":{"kind":"Name","value":"isNegativeSelection"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"valueOrdering"}},{"kind":"Field","name":{"kind":"Name","value":"titleFi"}},{"kind":"Field","name":{"kind":"Name","value":"titleEn"}},{"kind":"Field","name":{"kind":"Name","value":"titleSv"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditorValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyFieldsPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionEditor"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"enrich"},"value":{"kind":"BooleanValue","value":false}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditSurveyFieldsPageQueryQuery, EditSurveyFieldsPageQueryQueryVariables>;
export const EditFormLanguagePageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditFormLanguagePageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"language"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"FORMS"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditFormLanguagePage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditFormLanguagePage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"language"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<EditFormLanguagePageQueryQuery, EditFormLanguagePageQueryQueryVariables>;
export const CreateSurveyLanguageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateSurveyLanguage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyLanguageInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyLanguage"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]}}]} as unknown as DocumentNode<CreateSurveyLanguageMutation, CreateSurveyLanguageMutationVariables>;
export const UpdateSurveyMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateSurveyMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateSurveyMutationMutation, UpdateSurveyMutationMutationVariables>;
export const DeleteSurveyMutationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyMutation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyMutationMutation, DeleteSurveyMutationMutationVariables>;
export const EditSurveyPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditSurveyPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"FORMS"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditSurveyPage"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyPage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"loginRequired"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"maxResponsesPerUser"}},{"kind":"Field","name":{"kind":"Name","value":"countResponsesByCurrentUser"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"responsesEditableUntil"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}},{"kind":"Field","name":{"kind":"Name","value":"purpose"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"canRemove"}}]}}]}}]} as unknown as DocumentNode<EditSurveyPageQueryQuery, EditSurveyPageQueryQueryVariables>;
export const UpdateResponseDimensionsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateResponseDimensions"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateResponseDimensionsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateResponseDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateResponseDimensionsMutation, UpdateResponseDimensionsMutationVariables>;
export const EditSurveyResponseDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"EditSurveyResponse"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyResponseInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurveyResponse"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<EditSurveyResponseMutation, EditSurveyResponseMutationVariables>;
export const EditSurveyResponsePageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"EditSurveyResponsePage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"EditSurveyResponsePage"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistoryBanner"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"EditSurveyResponsePage"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseHistoryBanner"}},{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]}]}}]} as unknown as DocumentNode<EditSurveyResponsePageQuery, EditSurveyResponsePageQueryVariables>;
export const SurveyResponseDetailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyResponseDetail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"canRemoveResponses"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"BooleanValue","value":false}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionValueSelect"}}]}},{"kind":"Field","name":{"kind":"Name","value":"response"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"SurveyResponseDetail"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullSelectedProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"SelectedProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseHistorySidebar"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullSelectedProfile"}}]}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionValueSelect"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"SurveyResponseDetail"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseHistorySidebar"}},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"ADMIN"}}]},{"kind":"Field","name":{"kind":"Name","value":"canAccept"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"canDelete"}}]}}]} as unknown as DocumentNode<SurveyResponseDetailQuery, SurveyResponseDetailQueryVariables>;
export const SubscribeToSurveyResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"SubscribeToSurveyResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"SubscriptionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"subscribeToSurveyResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<SubscribeToSurveyResponsesMutation, SubscribeToSurveyResponsesMutationVariables>;
export const UnsubscribeFromSurveyResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UnsubscribeFromSurveyResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"SubscriptionInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"unsubscribeFromSurveyResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]} as unknown as DocumentNode<UnsubscribeFromSurveyResponsesMutation, UnsubscribeFromSurveyResponsesMutationVariables>;
export const DeleteSurveyResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"DeleteSurveyResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DeleteSurveyResponsesInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"deleteSurveyResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"countDeleted"}}]}}]}}]} as unknown as DocumentNode<DeleteSurveyResponsesMutation, DeleteSurveyResponsesMutationVariables>;
export const FormResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"FormResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"relation"},"value":{"kind":"EnumValue","value":"SUBSCRIBED"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"anonymity"}},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}},{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}},{"kind":"FragmentSpread","name":{"kind":"Name","value":"ColoredDimensionTableCell"}}]}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"canRemoveResponses"}},{"kind":"Field","name":{"kind":"Name","value":"protectResponses"}},{"kind":"Field","name":{"kind":"Name","value":"responses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"SurveyResponse"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ColoredDimensionTableCell"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"isTechnical"}},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"SurveyResponse"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"sequenceNumber"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"cachedDimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}]}]}}]} as unknown as DocumentNode<FormResponsesQuery, FormResponsesQueryVariables>;
export const SurveySummaryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveySummary"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filters"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionFilterInput"}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"fields"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"summary"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}]},{"kind":"Field","alias":{"kind":"Name","value":"countFilteredResponses"},"name":{"kind":"Name","value":"countResponses"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filters"}}}]},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilter"}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilterValue"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"DimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionFilter"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullDimensionType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isMultiValue"}},{"kind":"Field","name":{"kind":"Name","value":"isListFilter"}},{"kind":"Field","name":{"kind":"Name","value":"isKeyDimension"}},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionFilterValue"}}]}}]}}]} as unknown as DocumentNode<SurveySummaryQuery, SurveySummaryQueryVariables>;
export const CreateSurveyDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateSurvey"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateSurveyInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createSurvey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<CreateSurveyMutation, CreateSurveyMutationVariables>;
export const SurveysDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"Surveys"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"relation"},"value":{"kind":"EnumValue","value":"ACCESSIBLE"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileSurvey"}}]}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"surveys"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"includeInactive"},"value":{"kind":"BooleanValue","value":true}},{"kind":"Argument","name":{"kind":"Name","value":"app"},"value":{"kind":"EnumValue","value":"FORMS"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"Survey"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileSurvey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Survey"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullSurveyType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isActive"}},{"kind":"Field","name":{"kind":"Name","value":"activeFrom"}},{"kind":"Field","name":{"kind":"Name","value":"activeUntil"}},{"kind":"Field","name":{"kind":"Name","value":"countResponses"}},{"kind":"Field","name":{"kind":"Name","value":"languages"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"language"}}]}}]}}]} as unknown as DocumentNode<SurveysQuery, SurveysQueryVariables>;
export const TicketsAdminReportsPageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"TicketsAdminReportsPage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}},{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"reports"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"Report"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"Report"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ReportType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"footer"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"columns"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"type"}}]}},{"kind":"Field","name":{"kind":"Name","value":"rows"}},{"kind":"Field","name":{"kind":"Name","value":"totalRow"}}]}}]} as unknown as DocumentNode<TicketsAdminReportsPageQuery, TicketsAdminReportsPageQueryVariables>;
export const GenerateKeyPairDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"GenerateKeyPair"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"password"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"generateKeyPair"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"password"},"value":{"kind":"Variable","name":{"kind":"Name","value":"password"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<GenerateKeyPairMutation, GenerateKeyPairMutationVariables>;
export const RevokeKeyPairDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"RevokeKeyPair"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"id"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"revokeKeyPair"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"id"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]} as unknown as DocumentNode<RevokeKeyPairMutation, RevokeKeyPairMutationVariables>;
export const ProfileEncryptionKeysDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileEncryptionKeys"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"keypairs"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileEncryptionKeys"}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileEncryptionKeys"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"KeyPairType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}}]}}]} as unknown as DocumentNode<ProfileEncryptionKeysQuery, ProfileEncryptionKeysQueryVariables>;
export const ProfileOrderDetailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileOrderDetail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"order"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"orderId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"canPay"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"products"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"quantity"}},{"kind":"Field","name":{"kind":"Name","value":"price"}}]}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<ProfileOrderDetailQuery, ProfileOrderDetailQueryVariables>;
export const ConfirmEmailDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"ConfirmEmail"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ConfirmEmailInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"confirmEmail"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"email"}}]}}]}}]}}]} as unknown as DocumentNode<ConfirmEmailMutation, ConfirmEmailMutationVariables>;
export const ProfileOrdersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileOrders"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"tickets"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"orders"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileOrder"}}]}},{"kind":"Field","name":{"kind":"Name","value":"haveUnlinkedOrders"}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileOrder"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileOrderType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"formattedOrderNumber"}},{"kind":"Field","name":{"kind":"Name","value":"createdAt"}},{"kind":"Field","name":{"kind":"Name","value":"totalPrice"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"eticketsLink"}},{"kind":"Field","name":{"kind":"Name","value":"canPay"}},{"kind":"Field","name":{"kind":"Name","value":"canCancel"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]} as unknown as DocumentNode<ProfileOrdersQuery, ProfileOrdersQueryVariables>;
export const ProfileProgramItemListDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileProgramItemList"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"programs"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"userRelation"},"value":{"kind":"EnumValue","value":"HOSTING"}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileProgramItem"}}]}},{"kind":"Field","name":{"kind":"Name","value":"programOffers"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"filters"},"value":{"kind":"ListValue","values":[{"kind":"ObjectValue","fields":[{"kind":"ObjectField","name":{"kind":"Name","value":"dimension"},"value":{"kind":"StringValue","value":"state","block":false}},{"kind":"ObjectField","name":{"kind":"Name","value":"values"},"value":{"kind":"StringValue","value":"new","block":false}}]}]}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileResponsesTableRow"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileProgramItem"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"FullProgramType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduleItems"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"startTime"}},{"kind":"Field","name":{"kind":"Name","value":"endTime"}},{"kind":"Field","name":{"kind":"Name","value":"durationMinutes"}},{"kind":"Field","name":{"kind":"Name","value":"location"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"subtitle"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponsesTableRow"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"OWNER"}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<ProfileProgramItemListQuery, ProfileProgramItemListQueryVariables>;
export const ProfileSurveyEditResponseDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileSurveyEditResponse"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"userRegistry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullOwnProfile"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"OWNER"}}]},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"registry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}}]}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"TransferConsentFormRegistry"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedRegistryType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"organization"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"policyUrl"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullOwnProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"OwnProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<ProfileSurveyEditResponseQuery, ProfileSurveyEditResponseQueryVariables>;
export const ProfileSurveyResponsePageDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProfileSurveyResponsePage"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"userRegistry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}},{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullOwnProfile"}},{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"responseId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileResponseHistoryBanner"}},{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"OWNER"}}]},{"kind":"Field","name":{"kind":"Name","value":"values"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"DimensionBadge"}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"language"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"timezone"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profileFieldSelector"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"FullProfileFieldSelector"}}]}},{"kind":"Field","name":{"kind":"Name","value":"registry"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"TransferConsentFormRegistry"}}]}}]}}]}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ResponseRevision"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"displayName"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"TransferConsentFormRegistry"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"LimitedRegistryType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"organization"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"policyUrl"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullOwnProfile"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"OwnProfileType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponseHistoryBanner"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"supersededBy"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"oldVersions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ResponseRevision"}}]}},{"kind":"Field","name":{"kind":"Name","value":"originalCreatedAt"}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"DimensionBadge"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ResponseDimensionValueType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"FullProfileFieldSelector"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileFieldSelectorType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"nick"}},{"kind":"Field","name":{"kind":"Name","value":"email"}},{"kind":"Field","name":{"kind":"Name","value":"phoneNumber"}},{"kind":"Field","name":{"kind":"Name","value":"discordHandle"}}]}}]} as unknown as DocumentNode<ProfileSurveyResponsePageQuery, ProfileSurveyResponsePageQueryVariables>;
export const OwnFormResponsesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"OwnFormResponses"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"profile"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"forms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"responses"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"ProfileResponsesTableRow"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"ProfileResponsesTableRow"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"ProfileResponseType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"revisionCreatedAt"}},{"kind":"Field","name":{"kind":"Name","value":"canEdit"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"mode"},"value":{"kind":"EnumValue","value":"OWNER"}}]},{"kind":"Field","name":{"kind":"Name","value":"values"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyFieldsOnly"},"value":{"kind":"BooleanValue","value":true}}]},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"keyDimensionsOnly"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dimension"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"value"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"form"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"event"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]} as unknown as DocumentNode<OwnFormResponsesQuery, OwnFormResponsesQueryVariables>;
export const UpdateProgramAnnotationsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateProgramAnnotations"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateProgramAnnotationsInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateProgramAnnotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"cachedAnnotations"}}]}}]}}]}}]} as unknown as DocumentNode<UpdateProgramAnnotationsMutation, UpdateProgramAnnotationsMutationVariables>;
export const GetProgramAnnotationSchemaDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetProgramAnnotationSchema"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"annotationSlugs"}},"type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"publicOnly"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Boolean"}},"defaultValue":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"program"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"annotations"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"annotationSlugs"}}},{"kind":"Argument","name":{"kind":"Name","value":"publicOnly"},"value":{"kind":"Variable","name":{"kind":"Name","value":"publicOnly"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"AnnotationsFormAnnotation"}}]}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"AnnotationsFormAnnotation"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AnnotationType"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"description"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"isComputed"}}]}}]} as unknown as DocumentNode<GetProgramAnnotationSchemaQuery, GetProgramAnnotationSchemaQueryVariables>;