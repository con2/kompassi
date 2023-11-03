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

export type EventType = {
  __typename?: 'EventType';
  dimensions?: Maybe<Array<Maybe<DimensionType>>>;
  languages?: Maybe<Array<Maybe<LanguageType>>>;
  name: Scalars['String']['output'];
  programs?: Maybe<Array<Maybe<ProgramType>>>;
  /** Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen. */
  slug: Scalars['String']['output'];
};


export type EventTypeLanguagesArgs = {
  event: Scalars['String']['input'];
};


export type EventTypeProgramsArgs = {
  filters?: InputMaybe<Array<InputMaybe<DimensionFilterInput>>>;
};

export type LanguageType = {
  __typename?: 'LanguageType';
  code?: Maybe<Scalars['String']['output']>;
  name?: Maybe<Scalars['String']['output']>;
};


export type LanguageTypeNameArgs = {
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
  locale?: InputMaybe<Scalars['String']['input']>;
}>;


export type ProgrammeExampleQueryQuery = { __typename?: 'Query', event?: { __typename?: 'EventType', name: string, dimensions?: Array<{ __typename?: 'DimensionType', title?: string | null } | null> | null } | null };


export const ProgrammeExampleQueryDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"ProgrammeExampleQuery"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"locale"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"event"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"slug"},"value":{"kind":"Variable","name":{"kind":"Name","value":"eventSlug"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"dimensions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"title"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"lang"},"value":{"kind":"Variable","name":{"kind":"Name","value":"locale"}}}]}]}}]}}]}}]} as unknown as DocumentNode<ProgrammeExampleQueryQuery, ProgrammeExampleQueryQueryVariables>;