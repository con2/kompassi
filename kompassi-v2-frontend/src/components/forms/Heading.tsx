import { ComponentPropsWithoutRef } from "react";

export type HeadingLevel = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";

export type HeadingProps = ComponentPropsWithoutRef<"h1"> & {
  level?: HeadingLevel;
};

/// A heading element with a level that can be specified as a prop.
/// NOTE: Use only if you need to change the level of the heading from the outside.
/// Otherwise, use the appropriate heading element directly.
/// Used by SchemaForm that needs to render headings of different levels depending on the context the form is used in.
export function Heading(props: HeadingProps) {
  const { level, ...passthruProps } = props;
  const HeadingElement = level || "h2";
  return <HeadingElement {...passthruProps} />;
}
