# Static Site Generator

A dependency-free Python tool that turns a directory of Markdown files into a
template-driven static website. It includes a small Markdown parser, safe HTML
rendering, recursive page generation, and a complete example site.

## Highlights

- Converts headings, paragraphs, quotes, ordered and unordered lists, fenced
  code, emphasis, links, and images.
- Escapes Markdown content and HTML attributes by default, and rejects active
  URL schemes such as `javascript:`.
- Builds nested content trees while copying static assets unchanged.
- Generates into a temporary directory first, so a rendering error does not
  leave a partially built site behind.
- Uses only the Python standard library at runtime.

## Quick start

Python 3.10 or newer is required.

```bash
./main.sh
python3 -m http.server 8000 --directory public
```

Then open `http://localhost:8000`. To build for a site hosted below a URL
prefix, pass it explicitly:

```bash
./main.sh --base-path /static-site-generator/
```

Run the test suite with:

```bash
./test.sh
```

## How it works

Each `.md` file below `content/` becomes an `.html` file at the matching path
below `public/`. Every page must contain one level-one heading, which becomes
the document title. The generator replaces three template tokens:

| Token | Value |
| --- | --- |
| `{{ Title }}` | Escaped level-one heading |
| `{{ Content }}` | Rendered Markdown document |
| `{{ BasePath }}` | Normalized asset URL prefix |

The build combines these inputs:

```text
content/        Markdown pages
static/         CSS, images, and other copied assets
template.html   Shared page shell
src/            Parser, HTML nodes, generator, and tests
public/         Generated example output
```

Use `--content`, `--static`, `--template`, and `--output` to replace any of the
default paths. Run `python3 src/main.py --help` for the complete CLI reference.

## Scope

This project intentionally implements a focused Markdown subset rather than
the full CommonMark specification. Templates and files in `static/` are trusted
inputs; Markdown content is treated as text and cannot inject raw HTML.

The project began as a guided static-site-generator exercise and was extended
with recursive builds, a command-line interface, defensive rendering, stronger
tests, and continuous integration.
