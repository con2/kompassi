import { Field } from "../forms/models";
import { graphql } from "@/__generated__";
import {
  AnnotationDataType,
  AnnotationsFormAnnotationFragment,
} from "@/__generated__/graphql";

graphql(`
  fragment AnnotationsFormAnnotation on AnnotationType {
    slug
    type
    title(lang: $locale)
    description(lang: $locale)
    isComputed
  }
`);

export type CachedAnnotations = Record<string, string | boolean | number>;

export function isValidCachedAnnotations(
  schema: AnnotationsFormAnnotationFragment[],
  values: unknown,
): values is CachedAnnotations {
  if (typeof values !== "object" || values === null) {
    console.error("Cached annotations must be an object");
    return false;
  }
  if (Array.isArray(values)) {
    console.error("Cached annotations must not be an array");
    return false;
  }

  for (const pair of Object.entries(values)) {
    const [slug, value] = pair;

    const schemoid = schema.find((s) => s.slug === slug);
    if (!schemoid) {
      console.error(`Annotation ${slug} not found in schema`);
      return false;
    }
    const { type } = schemoid;

    if (type === "BOOLEAN" && typeof value !== "boolean") {
      console.error(
        `Annotation ${slug} must be a boolean, got ${typeof value}`,
      );
      return false;
    }
    if (type === "NUMBER" && typeof value !== "number") {
      console.error(`Annotation ${slug} must be a number, got ${typeof value}`);
      return false;
    }
    if (type === "STRING" && typeof value !== "string") {
      console.error(`Annotation ${slug} must be a string, got ${typeof value}`);
      return false;
    }
  }

  return true;
}

export function validateCachedAnnotations(
  schema: AnnotationsFormAnnotationFragment[],
  values: unknown,
): asserts values is CachedAnnotations {
  if (!isValidCachedAnnotations(schema, values)) {
    throw new Error("Invalid cached annotations");
  }
}

export function mangleAnnotationSlug(slug: string) {
  return slug.replace(":", "__");
}

export function unmangleAnnotationSlug(slug: string) {
  return slug.replace("__", ":");
}

export function getFormFieldForAnnotation(
  annotation: AnnotationsFormAnnotationFragment,
): Field {
  const { slug, title, description, isComputed } = annotation;
  let type: "Tristate" | "NumberField" | "SingleLineText" | "DateTimeField" =
    "SingleLineText";
  switch (annotation.type) {
    case AnnotationDataType.Boolean:
      type = "Tristate";
      break;
    case AnnotationDataType.Number:
      type = "NumberField";
      break;
    case AnnotationDataType.String:
      type = "SingleLineText";
      break;
    case AnnotationDataType.Datetime:
      type = "DateTimeField";
      break;
    default:
      const exhaustiveCheck: never = annotation.type;
      throw new Error(`Unknown annotation type: ${exhaustiveCheck}`);
  }

  return {
    slug: mangleAnnotationSlug(slug),
    title: `${title || slug}${isComputed ? " 🔒" : ""}`,
    helpText: description || "",
    readOnly: isComputed,
    type,
  };
}
