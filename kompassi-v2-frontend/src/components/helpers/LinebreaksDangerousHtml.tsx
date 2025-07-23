import React from "react";

/**
 * Accepts one prop, `text`, and displays it so that single line breaks get
 * turned into a `<br>` and double line breaks start a new `<p>`.
 *
 * This version accepts HTML and uses dangerouslySetInnerHTML to render it.
 * Any elements should be on a single line or they will break.
 */
export default function LinebreaksDangerousHtml({ html }: { html: string }) {
  const paragraphs = html.split(/(?:\r?\n){2,}/g);
  return (
    <>
      {paragraphs.map((paragraph, index) => (
        <p key={index}>
          {paragraph.split(/\r?\n/g).map((line, ind, lines) => (
            <React.Fragment key={ind}>
              <span dangerouslySetInnerHTML={{ __html: line }} />
              {ind === lines.length - 1 ? null : <br />}
            </React.Fragment>
          ))}
        </p>
      ))}
    </>
  );
}
