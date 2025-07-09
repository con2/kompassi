import React from "react";

/**
 * Accepts one prop, `text`, and displays it so that
 * double line breaks start a new `<p>`.
 *
 * This version accepts HTML and uses dangerouslySetInnerHTML to render it.
 * Any elements should be on a single line or they will break.
 */
export default function Paragraphs({ text }: { text: string }) {
  const paragraphs = text.split(/(?:\r?\n){2,}/g);
  return (
    <>
      {paragraphs.map((paragraph, index) => (
        <p key={index}>{paragraph}</p>
      ))}
    </>
  );
}
