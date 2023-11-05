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
   * Allows use of a JSON String for input / output from the GraphQL schema.
   *
   * Use of this type is *not recommended* as you lose the benefits of having a defined, static
   * schema (one of the key benefits of GraphQL).
   */
  JSONString: { input: any; output: any; }
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
  active: Scalars['Boolean']['output'];
  description: Scalars['String']['output'];
  fields?: Maybe<Scalars['JSONString']['output']>;
  layout: FormsEventFormLayoutChoices;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
  title: Scalars['String']['output'];
};

export type EventType = {
  __typename?: 'EventType';
  dimensions?: Maybe<Array<DimensionType>>;
  languages?: Maybe<Array<LanguageType>>;
  name: Scalars['String']['output'];
  offerForm?: Maybe<OfferFormType>;
  offerForms?: Maybe<Array<OfferFormType>>;
  programs?: Maybe<Array<ProgramType>>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
};


export type EventTypeOfferFormArgs = {
  slug: Scalars['String']['input'];
};


export type EventTypeProgramsArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
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

export type OfferFormType = {
  __typename?: 'OfferFormType';
  form?: Maybe<EventFormType>;
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

export type ProgrammeExampleQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  formSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgrammeExampleQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, offerForm?: { __typename?: 'OfferFormType', shortDescription?: string | null, form?: { __typename?: 'EventFormType', title: string, description: string, fields?: any | null } | null } | null } | null };

export type NewProgramFormSelectionQueryQueryVariables = Exact<{
  eventSlug: Scalars['String']['input'];
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type NewProgramFormSelectionQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, slug: string, offerForms?: Array<{ __typename?: 'OfferFormType', slug: string, shortDescription?: string | null, form?: { __typename?: 'EventFormType', title: string, slug: string } | null }> | null } | null };


export const ProgrammeExampleQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgrammeExampleQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"formSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"offerForm"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"formSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"shortDescription"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"fields"}}]}}]}}]}}]}}]} as unknown as DocumentNode<ProgrammeExampleQueryQuery, ProgrammeExampleQueryQueryVariables>;
export const NewProgramFormSelectionQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"NewProgramFormSelectionQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"offerForms"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"shortDescription"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]},{"kind":"Field","name":{"kind":"Name","value":"form"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}}]}}]}}]}}]}}]} as unknown as DocumentNode<NewProgramFormSelectionQueryQuery, NewProgramFormSelectionQueryQueryVariables>;