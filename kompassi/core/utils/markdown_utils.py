import markdown as markdown_lib
import nh3

# Keep in sync with @con2/components' MarkdownEditor toolbar, which only offers the
# formatting allowed through here: headings (h1-h4, not h5/h6), bold, italics, lists,
# links. No images, tables, strikethrough, or horizontal rules.
ALLOWED_MARKDOWN_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "p",
    "strong",
    "em",
    "ul",
    "ol",
    "li",
    "a",
    "br",
    "blockquote",
    "code",
    "pre",
}
ALLOWED_MARKDOWN_ATTRIBUTES = {"a": {"href"}}


def render_markdown(source: str) -> str:
    """Render Markdown source into sanitized HTML."""
    html_fragment = markdown_lib.markdown(source)
    return nh3.clean(html_fragment, tags=ALLOWED_MARKDOWN_TAGS, attributes=ALLOWED_MARKDOWN_ATTRIBUTES)
