import { SchemaForm } from "../forms/SchemaForm";
import {
  CachedAnnotations,
  getFormFieldForAnnotationSchemoid,
  mangleAnnotationSlug,
} from "./models";
import { AnnotationsFormAnnotationFragment } from "@/__generated__/graphql";
import { Translations } from "@/translations/en";

interface Props {
  schema: AnnotationsFormAnnotationFragment[];
  values: CachedAnnotations;
  messages: Translations["SchemaForm"];
}

export default function AnnotationsForm({ schema, values, messages }: Props) {
  const fields = schema.map(getFormFieldForAnnotationSchemoid);
  const mangledValues = Object.fromEntries(
    schema.map((annotation) => [
      mangleAnnotationSlug(annotation.slug),
      values[annotation.slug],
    ]),
  );
  return (
    <SchemaForm fields={fields} values={mangledValues} messages={messages} />
  );
}
