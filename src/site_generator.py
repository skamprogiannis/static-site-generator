from html import escape
from pathlib import Path
import shutil
import tempfile

from markdown_parser import markdown_to_html


TITLE_PLACEHOLDER = "{{ Title }}"
CONTENT_PLACEHOLDER = "{{ Content }}"
BASE_PATH_PLACEHOLDER = "{{ BasePath }}"


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    raise ValueError("Markdown page must contain a level-one heading")


def normalize_base_path(base_path):
    stripped = base_path.strip("/")
    return f"/{stripped}/" if stripped else "/"


def render_page(markdown, template, base_path="/"):
    missing = [
        placeholder
        for placeholder in (TITLE_PLACEHOLDER, CONTENT_PLACEHOLDER)
        if placeholder not in template
    ]
    if missing:
        raise ValueError(f"template missing placeholder: {', '.join(missing)}")

    return (
        template.replace(TITLE_PLACEHOLDER, escape(extract_title(markdown)))
        .replace(CONTENT_PLACEHOLDER, markdown_to_html(markdown))
        .replace(BASE_PATH_PLACEHOLDER, normalize_base_path(base_path))
    )


def generate_page(source_path, template, destination_path, base_path="/"):
    markdown = source_path.read_text(encoding="utf-8")
    html = render_page(markdown, template, base_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(html, encoding="utf-8")


def _validate_paths(content_dir, static_dir, output_dir):
    content = content_dir.resolve()
    static = static_dir.resolve()
    output = output_dir.resolve()

    if (
        output in (content, static)
        or output in content.parents
        or output in static.parents
    ):
        raise ValueError("output directory must not contain the source directories")
    if content in output.parents or static in output.parents:
        raise ValueError("output directory must not be inside a source directory")


def build_site(content_dir, template_path, static_dir, output_dir, base_path="/"):
    content_dir = Path(content_dir)
    template_path = Path(template_path)
    static_dir = Path(static_dir)
    output_dir = Path(output_dir)
    _validate_paths(content_dir, static_dir, output_dir)

    if not content_dir.is_dir():
        raise FileNotFoundError(f"content directory not found: {content_dir}")
    if not static_dir.is_dir():
        raise FileNotFoundError(f"static directory not found: {static_dir}")

    template = template_path.read_text(encoding="utf-8")
    markdown_files = sorted(content_dir.rglob("*.md"))
    if not markdown_files:
        raise ValueError("content directory contains no Markdown files")

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(
        tempfile.mkdtemp(prefix=f".{output_dir.name}-", dir=output_dir.parent)
    )
    generated_pages = []

    try:
        shutil.copytree(static_dir, temp_dir, dirs_exist_ok=True)
        for source_path in markdown_files:
            relative_path = source_path.relative_to(content_dir).with_suffix(".html")
            destination_path = temp_dir / relative_path
            generate_page(source_path, template, destination_path, base_path)
            generated_pages.append(output_dir / relative_path)

        if output_dir.exists():
            shutil.rmtree(output_dir)
        temp_dir.replace(output_dir)
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    return generated_pages
