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
  DateTime: { input: any; output: any; }
  /**
   * The `GenericScalar` scalar type represents a generic
   * GraphQL scalar value that could be:
   * String, Boolean, Int, Float, List or Object.
   */
  GenericScalar: { input: any; output: any; }
  /**
   * Allows use of a JSON String for input / output from the GraphQL schema.
   *
   * Use of this type is *not recommended* as you lose the benefits of having a defined, static
   * schema (one of the key benefits of GraphQL).
   */
  JSONString: { input: any; output: any; }
  /**
   * Leverages the internal Python implementation of UUID (uuid.UUID) to provide native UUID objects
   * in fields, resolvers and input.
   */
  UUID: { input: any; output: any; }
};

export type CreateEventSurveyResponse = {
  __typename?: 'CreateEventSurveyResponse';
  response?: Maybe<EventSurveyResponseType>;
};

export type DimensionFilterInput = {
  dimension?: InputMaybe<Scalars['String']['input']>;
  values?: InputMaybe<Array<InputMaybe<Scalars['String']['input']>>>;
};

export type DimensionType = {
  __typename?: 'DimensionType';
  slug: Scalars['String']['output'];
  title?: Maybe<Scalars['String']['output']>;
  values: Array<DimensionValueType>;
};


export type DimensionTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type DimensionValueType = {
  __typename?: 'DimensionValueType';
  slug: Scalars['String']['output'];
  title?: Maybe<Scalars['String']['output']>;
};


export type DimensionValueTypeTitleArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type EventFormType = {
  __typename?: 'EventFormType';
  description: Scalars['String']['output'];
  fields?: Maybe<Scalars['GenericScalar']['output']>;
  layout: FormsEventFormLayoutChoices;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  thankYouMessage: Scalars['String']['output'];
  title: Scalars['String']['output'];
};


export type EventFormTypeFieldsArgs = {
  enrich?: InputMaybe<Scalars['Boolean']['input']>;
};

export type EventSurveyResponseType = {
  __typename?: 'EventSurveyResponseType';
  createdAt: Scalars['DateTime']['output'];
  formData: Scalars['JSONString']['output'];
  id: Scalars['UUID']['output'];
};

export type EventSurveyType = {
  __typename?: 'EventSurveyType';
  /** The form will be available from this date onwards. If not set, the form will not be available. */
  activeFrom?: Maybe<Scalars['DateTime']['output']>;
  /** The form will be available until this date. If not set, the form will be available indefinitely provided that active_from is set and has passed. */
  activeUntil?: Maybe<Scalars['DateTime']['output']>;
  form?: Maybe<EventFormType>;
  isActive: Scalars['Boolean']['output'];
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
};


export type EventSurveyTypeFormArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type EventType = {
  __typename?: 'EventType';
  dimensions?: Maybe<Array<DimensionType>>;
  languages?: Maybe<Array<LanguageType>>;
  name: Scalars['String']['output'];
  offerForm?: Maybe<OfferFormType>;
  offerForms?: Maybe<Array<OfferFormType>>;
  programs?: Maybe<Array<ProgramType>>;
  skipOfferFormSelection?: Maybe<Scalars['Boolean']['output']>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  survey?: Maybe<EventSurveyType>;
  surveys?: Maybe<Array<EventSurveyType>>;
};


export type EventTypeOfferFormArgs = {
  slug: Scalars['String']['input'];
};


export type EventTypeOfferFormsArgs = {
  includeInactive?: InputMaybe<Scalars['Boolean']['input']>;
};


export type EventTypeProgramsArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
};


export type EventTypeSurveyArgs = {
  slug: Scalars['String']['input'];
};


export type EventTypeSurveysArgs = {
  includeInactive?: InputMaybe<Scalars['Boolean']['input']>;
};

/** An enumeration. */
export enum FormsEventFormLayoutChoices {
  /** Horizontal */
  Horizontal = 'HORIZONTAL',
  /** Vertical */
  Vertical = 'VERTICAL'
}

export type LanguageType = {
  __typename?: 'LanguageType';
  code?: Maybe<Scalars['String']['output']>;
  name?: Maybe<Scalars['String']['output']>;
};


export type LanguageTypeNameArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type Mutation = {
  __typename?: 'Mutation';
  createEventSurveyResponse?: Maybe<CreateEventSurveyResponse>;
};


export type MutationCreateEventSurveyResponseArgs = {
  eventSlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
  surveySlug: Scalars['String']['input'];
};

export type OfferFormType = {
  __typename?: 'OfferFormType';
  form?: Maybe<EventFormType>;
  isActive: Scalars['Boolean']['output'];
  shortDescription?: Maybe<Scalars['String']['output']>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
};


export type OfferFormTypeFormArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};


export type OfferFormTypeShortDescriptionArgs = {
  lang?: InputMaybe<Scalars['String']['input']>;
};

export type ProgramDimensionValueType = {
  __typename?: 'ProgramDimensionValueType';
  dimension: DimensionType;
  value: DimensionValueType;
};

export type ProgramType = {
  __typename?: 'ProgramType';
  cachedDimensions: Scalars['JSONString']['output'];
  dimensions: Array<ProgramDimensionValueType>;
  scheduleItems: Array<ScheduleItemType>;
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
};

export type Query = {
  __typename?: 'Query';
  event?: Maybe<EventType>;
};


export type QueryEventArgs = {
  slug: Scalars['String']['input'];
};

export type ScheduleItemType = {
  __typename?: 'ScheduleItemType';
  endTime?: Maybe<Scalars['DateTime']['output']>;
  lengthMinutes?: Maybe<Scalars['Int']['output']>;
  startTime: Scalars['DateTime']['output'];
  subtitle: Scalars['String']['output'];
};

export type NewProgramQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  formSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type NewProgramQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, skipOfferFormSelection?: boolean | null, offerForm?: { __typename?: 'OfferFormType', form?: { __typename?: 'EventFormType', title: string, description: string, fields?: any | null, layout: FormsEventFormLayoutChoices } | null } | null } | null };

export type NewProgramFormSelectionQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type NewProgramFormSelectionQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, slug: string, skipOfferFormSelection?: boolean | null, offerForms?: Array<{ __typename?: 'OfferFormType', slug: string, shortDescription?: string | null, form?: { __typename?: 'EventFormType', title: string, slug: string } | null }> | null } | null };

export type CreateEventSurveyResponseMutationVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  formData: Scalars['GenericScalar']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type CreateEventSurveyResponseMutation = { __typename?: 'Mutation', createEventSurveyResponse?: { __typename?: 'CreateEventSurveyResponse', response?: { __typename?: 'EventSurveyResponseType', id: any } | null } | null };

export type SurveyPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, survey?: { __typename?: 'EventSurveyType', form?: { __typename?: 'EventFormType', title: string, description: string, fields?: any | null, layout: FormsEventFormLayoutChoices } | null } | null } | null };

export type SurveyThankYouPageQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  surveySlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type SurveyThankYouPageQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, survey?: { __typename?: 'EventSurveyType', form?: { __typename?: 'EventFormType', title: string, thankYouMessage: string } | null } | null } | null };


export const NewProgramQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"NewProgramQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"formSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"skipOfferFormSelection"}},{"kind":"Field","name":{"kind":"Name","value":"offerForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"formSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"layout"}}]}}]}}]}}]}}]} as unknown as DocumentNode<NewProgramQueryQuery, NewProgramQueryQueryVariables>;
export const NewProgramFormSelectionQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"NewProgramFormSelectionQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"skipOfferFormSelection"}},{"kind":"Field","name":{"kind":"Name","value":"offerForms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"shortDescription"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]}}]} as unknown as DocumentNode<NewProgramFormSelectionQueryQuery, NewProgramFormSelectionQueryQueryVariables>;
export const CreateEventSurveyResponseDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateEventSurveyResponse"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"formData"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"GenericScalar"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createEventSurveyResponse"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"eventSlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"surveySlug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}},{"kind":"Argument","name":{"kind":"Name","value":"formData"},"value":{"kind":"Variable","name":{"kind":"Name","value":"formData"}}},{"kind":"Argument","name":{"kind":"Name","value":"locale"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"response"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}}]}}]}}]}}]} as unknown as DocumentNode<CreateEventSurveyResponseMutation, CreateEventSurveyResponseMutationVariables>;
export const SurveyPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}},{"kind":"Field","name":{"kind":"Name","value":"layout"}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveyPageQueryQuery, SurveyPageQueryQueryVariables>;
export const SurveyThankYouPageQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"SurveyThankYouPageQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"survey"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"surveySlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"thankYouMessage"}}]}}]}}]}}]}}]} as unknown as DocumentNode<SurveyThankYouPageQueryQuery, SurveyThankYouPageQueryQueryVariables>;