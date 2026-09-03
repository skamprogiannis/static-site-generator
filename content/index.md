# Static sites, built from plain text

This page was generated from a Markdown file by a **dependency-free Python**
build pipeline. The source stays readable, the output stays portable, and the
browser receives straightforward HTML and CSS.

## A small, inspectable pipeline

The generator keeps its stages explicit:

1. Split Markdown into semantic blocks.
2. Convert inline syntax into typed nodes.
3. Escape content and render the node tree as HTML.
4. Insert the page into a shared template.
5. Copy static assets and publish the completed output tree.

## Supported authoring

- Headings, paragraphs, and block quotes
- Ordered and unordered lists
- **Bold**, _italic_, and `inline code`
- Fenced code blocks, links, and images

> Plain files are durable. A focused tool can stay understandable all the way
> from its parser to the HTML it emits.

## One command to build

```bash
./main.sh --base-path /
python3 -m http.server 8000 --directory public
```

Read the [source on GitHub](https://github.com/skamprogiannis/static-site-generator)
or edit this page in `content/index.md` and rebuild it locally.
