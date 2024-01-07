/* eslint-disable */
import * as types from './graphql';
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 */
const documents = {
    "\n  query NewProgramQuery($eventSlug:String!, $formSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n      program {\n        skipOfferFormSelection\n\n        offerForm(slug: $formSlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n": types.NewProgramQueryDocument,
    "\n  query NewProgramFormSelectionQuery($eventSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      program {\n        skipOfferFormSelection\n\n        offerForms {\n          slug\n          shortDescription(lang: $locale)\n          form(lang: $locale) {\n            title\n            slug\n          }\n        }\n      }\n    }\n  }\n": types.NewProgramFormSelectionQueryDocument,
    "\n  mutation CreateSurveyResponse(\n      $eventSlug: String!,\n      $surveySlug: String!,\n      $formData: GenericScalar!,\n      $locale: String\n  ) {\n    createSurveyResponse(\n      eventSlug: $eventSlug\n      surveySlug: $surveySlug\n      formData: $formData\n      locale: $locale\n    ) {\n      response {\n        id\n      }\n    }\n  }\n": types.CreateSurveyResponseDocument,
    "\n  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n": types.SurveyPageQueryDocument,
    "\n  query SurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n\n          response(id: $responseId) {\n            id\n            createdAt\n            language\n            values\n\n            form {\n              fields\n              layout\n            }\n          }\n        }\n      }\n    }\n  }\n": types.SurveyResponseDetailDocument,
    "\n  fragment SurveyResponse on LimitedResponseType {\n    id\n    createdAt\n    language\n    values\n  }\n": types.SurveyResponseFragmentDoc,
    "\n  query FormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n\n          responses {\n            ...SurveyResponse\n          }\n        }\n      }\n    }\n  }\n": types.FormResponsesDocument,
    "\n  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n": types.SurveyThankYouPageQueryDocument,
    "\n  fragment Survey on SurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n\n    languages {\n      language\n    }\n  }\n": types.SurveyFragmentDoc,
    "\n  query Surveys($eventSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        surveys {\n          ...Survey\n        }\n      }\n    }\n  }\n": types.SurveysDocument,
    "\n  query OwnResponseDetail($responseId: String!) {\n    profile {\n      forms {\n        response(id: $responseId) {\n          id\n          createdAt\n          values\n          form {\n            slug\n            title\n            language\n            fields\n            layout\n            event {\n              slug\n              name\n            }\n          }\n        }\n      }\n    }\n  }\n": types.OwnResponseDetailDocument,
    "\n  fragment OwnResponse on FullResponseType {\n    id\n    createdAt\n    form {\n      slug\n      title\n      event {\n        slug\n        name\n      }\n    }\n  }\n": types.OwnResponseFragmentDoc,
    "\n  query OwnFormResponses {\n    profile {\n      forms {\n        responses {\n          ...OwnResponse\n        }\n      }\n    }\n  }\n": types.OwnFormResponsesDocument,
};

/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = gql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function gql(source: string): unknown;

/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query NewProgramQuery($eventSlug:String!, $formSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n      program {\n        skipOfferFormSelection\n\n        offerForm(slug: $formSlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query NewProgramQuery($eventSlug:String!, $formSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n      program {\n        skipOfferFormSelection\n\n        offerForm(slug: $formSlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query NewProgramFormSelectionQuery($eventSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      program {\n        skipOfferFormSelection\n\n        offerForms {\n          slug\n          shortDescription(lang: $locale)\n          form(lang: $locale) {\n            title\n            slug\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query NewProgramFormSelectionQuery($eventSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      program {\n        skipOfferFormSelection\n\n        offerForms {\n          slug\n          shortDescription(lang: $locale)\n          form(lang: $locale) {\n            title\n            slug\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  mutation CreateSurveyResponse(\n      $eventSlug: String!,\n      $surveySlug: String!,\n      $formData: GenericScalar!,\n      $locale: String\n  ) {\n    createSurveyResponse(\n      eventSlug: $eventSlug\n      surveySlug: $surveySlug\n      formData: $formData\n      locale: $locale\n    ) {\n      response {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateSurveyResponse(\n      $eventSlug: String!,\n      $surveySlug: String!,\n      $formData: GenericScalar!,\n      $locale: String\n  ) {\n    createSurveyResponse(\n      eventSlug: $eventSlug\n      surveySlug: $surveySlug\n      formData: $formData\n      locale: $locale\n    ) {\n      response {\n        id\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query SurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n\n          response(id: $responseId) {\n            id\n            createdAt\n            language\n            values\n\n            form {\n              fields\n              layout\n            }\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n\n          response(id: $responseId) {\n            id\n            createdAt\n            language\n            values\n\n            form {\n              fields\n              layout\n            }\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  fragment SurveyResponse on LimitedResponseType {\n    id\n    createdAt\n    language\n    values\n  }\n"): (typeof documents)["\n  fragment SurveyResponse on LimitedResponseType {\n    id\n    createdAt\n    language\n    values\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query FormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n\n          responses {\n            ...SurveyResponse\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query FormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n\n          responses {\n            ...SurveyResponse\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  fragment Survey on SurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n\n    languages {\n      language\n    }\n  }\n"): (typeof documents)["\n  fragment Survey on SurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n\n    languages {\n      language\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query Surveys($eventSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        surveys {\n          ...Survey\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query Surveys($eventSlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        surveys {\n          ...Survey\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query OwnResponseDetail($responseId: String!) {\n    profile {\n      forms {\n        response(id: $responseId) {\n          id\n          createdAt\n          values\n          form {\n            slug\n            title\n            language\n            fields\n            layout\n            event {\n              slug\n              name\n            }\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query OwnResponseDetail($responseId: String!) {\n    profile {\n      forms {\n        response(id: $responseId) {\n          id\n          createdAt\n          values\n          form {\n            slug\n            title\n            language\n            fields\n            layout\n            event {\n              slug\n              name\n            }\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  fragment OwnResponse on FullResponseType {\n    id\n    createdAt\n    form {\n      slug\n      title\n      event {\n        slug\n        name\n      }\n    }\n  }\n"): (typeof documents)["\n  fragment OwnResponse on FullResponseType {\n    id\n    createdAt\n    form {\n      slug\n      title\n      event {\n        slug\n        name\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query OwnFormResponses {\n    profile {\n      forms {\n        responses {\n          ...OwnResponse\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query OwnFormResponses {\n    profile {\n      forms {\n        responses {\n          ...OwnResponse\n        }\n      }\n    }\n  }\n"];

export function gql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;