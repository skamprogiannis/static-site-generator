import argparse
from pathlib import Path

from site_generator import build_site


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a static HTML site from a directory of Markdown files."
    )
    parser.add_argument(
        "--content",
        type=Path,
        default=PROJECT_ROOT / "content",
        help="Markdown source directory (default: content)",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=PROJECT_ROOT / "template.html",
        help="HTML template path (default: template.html)",
    )
    parser.add_argument(
        "--static",
        type=Path,
        default=PROJECT_ROOT / "static",
        help="Static asset directory (default: static)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "public",
        help="Generated site directory (default: public)",
    )
    parser.add_argument(
        "--base-path",
        default="/",
        help="URL prefix for assets, such as /project-name/",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    generated_pages = build_site(
        content_dir=args.content,
        template_path=args.template,
        static_dir=args.static,
        output_dir=args.output,
        base_path=args.base_path,
    )
    suffix = "page" if len(generated_pages) == 1 else "pages"
    print(f"Generated {len(generated_pages)} {suffix} in {args.output}")


if __name__ == "__main__":
    main()
