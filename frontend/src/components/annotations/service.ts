import processFormData from "../forms/processFormData";
import {
  getFormFieldForAnnotationSchemoid,
  unmangleAnnotationSlug,
} from "./models";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { defaultLanguage } from "@/translations";

const updateProgramAnnotationsMutation = graphql(`
  mutation UpdateProgramAnnotations($input: UpdateProgramAnnotationsInput!) {
    updateProgramAnnotations(input: $input) {
      program {
        slug
        cachedAnnotations
      }
    }
  }
`);

export async function updateProgramAnnotations(
  eventSlug: string,
  programSlug: string,
  annotations: Record<string, unknown>,
) {
  const { data, errors } = await getClient().mutate({
    mutation: updateProgramAnnotationsMutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        annotations,
      },
    },
  });

  if (errors) {
    console.error(errors);
    throw new Error(errors.map((e) => e.message).join(", "));
  }

  if (!data?.updateProgramAnnotations?.program) {
    throw new Error("No program found");
  }

  return data.updateProgramAnnotations.program;
}

const getProgramAnnotationSchemaQuery = graphql(`
  query GetProgramAnnotationSchema(
    $locale: String!
    $eventSlug: String!
    $annotationSlugs: [String!]
  ) {
    event(slug: $eventSlug) {
      program {
        annotations(slug: $annotationSlugs) {
          ...AnnotationsFormAnnotation
        }
      }
    }
  }
`);

export async function getProgramAnnotationSchema(
  locale: string,
  eventSlug: string,
  annotationSlugs?: string[],
) {
  const { data, errors } = await getClient().query({
    query: getProgramAnnotationSchemaQuery,
    variables: {
      locale,
      eventSlug,
      annotationSlugs,
    },
  });

  if (errors) {
    console.error(errors);
    throw new Error(errors.map((e) => e.message).join(", "));
  }

  const annotations = data?.event?.program?.annotations;
  if (!annotations) {
    throw new Error("No annotations found");
  }

  return annotations;
}

/// Update program annotations based on AnnotationsForm responses
export async function updateProgramAnnotationsFromFormData(
  eventSlug: string,
  programSlug: string,
  formData: FormData,
  /// Slugs of the annotations to update. If not provided, all annotations will be updated.
  annotationSlugs?: string[],
) {
  const schema = await getProgramAnnotationSchema(
    defaultLanguage, // we do not need human readable titles here
    eventSlug,
    annotationSlugs,
  );
  const schemaMap = Object.fromEntries(schema.map((s) => [s.slug, s]));
  const fields = schema.map(getFormFieldForAnnotationSchemoid);
  const mangledValues = processFormData(fields, formData);
  const values = Object.fromEntries(
    Object.entries(mangledValues)
      .map(([slug, value]) => [unmangleAnnotationSlug(slug), value] as const)
      .filter(([slug]) => !schemaMap[slug].isComputed),
  );
  return updateProgramAnnotations(eventSlug, programSlug, values);
}
