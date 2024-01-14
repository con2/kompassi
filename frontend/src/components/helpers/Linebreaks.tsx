import React from "react";

/**
 * Accepts one prop, `text`, and displays it so that single line breaks get
 * turned into a `<br>` and double line breaks start a new `<p>`.
 *
 * This version does not accept HTML.
 */
const Linebreaks = ({ text }: { text: string }) => {
  const paragraphs = text.split(/(?:\r?\n){2,}/g);
  return (
    <>
      {paragraphs.map((paragraph, index) => (
        <p key={index}>
          {paragraph.split(/\r?\n/g).map((line, ind, lines) => (
            <span key={ind}>
              {line}
              {ind === lines.length - 1 ? null : <br />}
            </span>
          ))}
        </p>
      ))}
    </>
  );
};

export default Linebreaks;
