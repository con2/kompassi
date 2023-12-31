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
    "\n  mutation CreateEventSurveyResponse(\n      $eventSlug: String!,\n      $surveySlug: String!,\n      $formData: GenericScalar!,\n      $locale: String\n  ) {\n    createEventSurveyResponse(\n      eventSlug: $eventSlug\n      surveySlug: $surveySlug\n      formData: $formData\n      locale: $locale\n    ) {\n      response {\n        id\n      }\n    }\n  }\n": types.CreateEventSurveyResponseDocument,
    "\n  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n": types.SurveyPageQueryDocument,
    "\n  query EventSurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n\n          response(id: $responseId) {\n            id\n            createdAt\n            language\n            values\n\n            form {\n              fields\n              layout\n            }\n          }\n        }\n      }\n    }\n  }\n": types.EventSurveyResponseDetailDocument,
    "\n  fragment EventSurveyResponse on EventFormResponseType {\n    id\n    createdAt\n    language\n    values\n  }\n": types.EventSurveyResponseFragmentDoc,
    "\n  query EventFormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n\n          responses {\n            ...EventSurveyResponse\n          }\n        }\n      }\n    }\n  }\n": types.EventFormResponsesDocument,
    "\n  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n": types.SurveyThankYouPageQueryDocument,
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
export function gql(source: "\n  mutation CreateEventSurveyResponse(\n      $eventSlug: String!,\n      $surveySlug: String!,\n      $formData: GenericScalar!,\n      $locale: String\n  ) {\n    createEventSurveyResponse(\n      eventSlug: $eventSlug\n      surveySlug: $surveySlug\n      formData: $formData\n      locale: $locale\n    ) {\n      response {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateEventSurveyResponse(\n      $eventSlug: String!,\n      $surveySlug: String!,\n      $formData: GenericScalar!,\n      $locale: String\n  ) {\n    createEventSurveyResponse(\n      eventSlug: $eventSlug\n      surveySlug: $surveySlug\n      formData: $formData\n      locale: $locale\n    ) {\n      response {\n        id\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            description\n            fields\n            layout\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query EventSurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n\n          response(id: $responseId) {\n            id\n            createdAt\n            language\n            values\n\n            form {\n              fields\n              layout\n            }\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EventSurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n\n          response(id: $responseId) {\n            id\n            createdAt\n            language\n            values\n\n            form {\n              fields\n              layout\n            }\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  fragment EventSurveyResponse on EventFormResponseType {\n    id\n    createdAt\n    language\n    values\n  }\n"): (typeof documents)["\n  fragment EventSurveyResponse on EventFormResponseType {\n    id\n    createdAt\n    language\n    values\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query EventFormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n\n          responses {\n            ...EventSurveyResponse\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EventFormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n\n          responses {\n            ...EventSurveyResponse\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(source: "\n  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n"];

export function gql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;