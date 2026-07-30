"use client";

import MDEditor from "@uiw/react-md-editor";
import * as commands from "@uiw/react-md-editor/commands";
import { useState } from "react";

// Required for the editor's layout (in particular, for the text area and preview pane
// to actually fill the visible bordered box instead of collapsing to their browser
// default size while the surrounding chrome renders at the full configured height).
import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";

interface MarkdownEditorProps {
  id?: string;
  name: string;
  defaultValue?: string;
  required?: boolean;
  readOnly?: boolean;
  rows?: number;
  insertHeadingLabel: string;
}

// Keep the toolbar limited to the formatting we actually allow through the backend
// sanitizer and document in the field's help text: headings, bold, italics, lists,
// links. In particular, only offer h1-h4 (not h5/h6, which nh3 would strip), and omit
// strikethrough, quote, code, tables, images, and horizontal rules entirely.
function buildToolbarCommands(insertHeadingLabel: string) {
  return [
    commands.group(
      [commands.title1, commands.title2, commands.title3, commands.title4],
      {
        name: "title",
        groupName: "title",
        buttonProps: { "aria-label": insertHeadingLabel },
        icon: commands.title.icon,
      },
    ),
    commands.bold,
    commands.italic,
    commands.divider,
    commands.unorderedListCommand,
    commands.orderedListCommand,
    commands.divider,
    commands.link,
  ];
}

/// A Markdown editor with a toolbar and preview restricted to the formatting the
/// backend renders/sanitizes, backed by a hidden input so it participates in normal
/// <form> submission.
export default function MarkdownEditor({
  id,
  name,
  defaultValue = "",
  required,
  readOnly,
  rows = 10,
  insertHeadingLabel,
}: MarkdownEditorProps) {
  const [value, setValue] = useState(defaultValue);
  // The toolbar (~40px) sits above the text area within `height`, so the text area's
  // own minHeight must leave room for it - otherwise its min-height (forced via an
  // inline style, see below) exceeds the space actually left for it after the
  // toolbar, and `.w-md-editor-area`'s `overflow: auto` permanently shows a scrollbar.
  const toolbarHeight = 40;
  const contentHeight = rows * 24;
  const editorHeight = contentHeight + toolbarHeight;

  return (
    <div data-color-mode="light">
      <input type="hidden" name={name} value={value} required={required} />
      <MDEditor
        id={id}
        value={value}
        onChange={(newValue) => setValue(newValue ?? "")}
        preview={readOnly ? "preview" : "live"}
        visibleDragbar={false}
        height={editorHeight}
        // MDEditor's `minHeight` defaults to 100px and, once set, is applied as an
        // inline style overriding the stylesheet's `min-height: 100%` rule on the
        // text area's wrapper - so without this, the editable area stays stuck at
        // 100px regardless of `height`, even though the surrounding chrome (and the
        // preview pane) do size to `height` correctly.
        minHeight={contentHeight}
        textareaProps={{ readOnly }}
        commands={buildToolbarCommands(insertHeadingLabel)}
      />
    </div>
  );
}
