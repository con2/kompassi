import {
  AnnotationDataType,
  AnnotationsFormAnnotationFragment,
} from "@/__generated__/graphql";
import { CachedAnnotations } from "./models";
import { Translations } from "@/translations/en";

interface Props {
  annotations: AnnotationsFormAnnotationFragment[];
  cachedAnnotations: CachedAnnotations;
  className?: string;
  fieldClassName?: string;
  messages: Translations["SchemaForm"];
}

export function AnnotationValue({
  annotation,
  value,
  messages,
}: {
  annotation: AnnotationsFormAnnotationFragment;
  value: string | number | boolean | undefined;
  messages: Translations["SchemaForm"];
}) {
  switch (annotation.type) {
    case AnnotationDataType.Boolean:
      if (value === true) {
        return <div>✅ {messages.boolean.true}</div>;
      } else if (value === false) {
        return <div>❌ {messages.boolean.false}</div>;
      }
  }
  return (
    <div>
      <strong>{annotation.title}</strong>: {value}
    </div>
  );
}

export default function AnnotationValuesReadOnly({
  annotations,
  cachedAnnotations,
  className = `row`,
  fieldClassName = `col-12 mb-3`,
  messages,
}: Props) {
  return (
    <div className={className}>
      {annotations
        .filter(
          (annotation) =>
            cachedAnnotations[annotation.slug] !== undefined &&
            cachedAnnotations[annotation.slug] !== "",
        )
        .map((annotation) => (
          <div key={annotation.slug} className={fieldClassName}>
            <div className="form-label fw-bold">{annotation.title}</div>
            <div>
              <AnnotationValue
                annotation={annotation}
                value={cachedAnnotations[annotation.slug]}
                messages={messages}
              />
            </div>
          </div>
        ))}
    </div>
  );
}
