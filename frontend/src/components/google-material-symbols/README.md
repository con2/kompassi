# Google Material Symbols

## Hand-picked SVG icons made into React components

Using Google Fonts hosted by Google is a GDPR hazard. There is no `next/font/material-symbols` as of 07/2025.

Current approach is as follows:

1. Find a symbol you want in the [icon search](https://fonts.google.com/icons)
2. Configure the following settings:

   - **Weight**: 400
   - **Grade**: 0
   - **Style**: Material Symbols (New), Outlined
   - **Optical size**: 24px

3. Download the SVG
4. Using eg. OpenInNewTab.tsx as a template, make the SVG into a React component

   - You may need to tweak the vertical translate to make the icon align with text.

The `.material-symbol` class lives in `globals.scss`.

## License

Material Symbols are available under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).
