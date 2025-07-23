import React from "react";

import styles from "./Linebreaks.module.css";

/**
 * Accepts one prop, `text`, and displays it so that single line breaks get
 * turned into a `<br>` and double line breaks start a new `<p>`.
 *
 * This version does not accept HTML.
 */
const Linebreaks = ({ text }: { text: string }) => {
  const paragraphs = text.split(/(?:\r?\n){2,}/g);
  return (
    <div className={styles.Linebreaks}>
      {paragraphs.map((paragraph, index) => (
        <p key={index}>
          {paragraph.split(/\r?\n/g).map((line, ind, lines) => (
            <React.Fragment key={ind}>
              {line}
              {ind === lines.length - 1 ? null : <br />}
            </React.Fragment>
          ))}
        </p>
      ))}
    </div>
  );
};

export default Linebreaks;
