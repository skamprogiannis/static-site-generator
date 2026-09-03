from pathlib import Path
import tempfile
import unittest

from site_generator import build_site, extract_title, normalize_base_path, render_page


TEMPLATE = """<!doctype html>
<html><head><title>{{ Title }}</title></head>
<body data-base="{{ BasePath }}">{{ Content }}</body></html>
"""


class TestSiteGenerator(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("## Intro\n\n# Site title\n"), "Site title")

    def test_extract_title_requires_h1(self):
        with self.assertRaisesRegex(ValueError, "level-one heading"):
            extract_title("## Missing title")

    def test_normalize_base_path(self):
        self.assertEqual(normalize_base_path("/"), "/")
        self.assertEqual(normalize_base_path("portfolio"), "/portfolio/")
        self.assertEqual(normalize_base_path("/portfolio/"), "/portfolio/")

    def test_render_page_replaces_placeholders(self):
        html = render_page("# Docs & demos\n\nWelcome.", TEMPLATE, "/project/")

        self.assertIn("<title>Docs &amp; demos</title>", html)
        self.assertIn('<body data-base="/project/">', html)
        self.assertIn("<h1>Docs &amp; demos</h1>", html)

    def test_render_page_requires_template_placeholders(self):
        with self.assertRaisesRegex(ValueError, "template missing placeholder"):
            render_page("# Title", "<html>{{ Content }}</html>")

    def test_build_site_recursively_and_copy_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = root / "content"
            static = root / "static"
            output = root / "public"
            content.mkdir()
            (content / "guides").mkdir()
            static.mkdir()
            (content / "index.md").write_text("# Home\n\nWelcome.", encoding="utf-8")
            (content / "guides" / "start.md").write_text(
                "# Start\n\nBuild it.", encoding="utf-8"
            )
            (static / "styles.css").write_text("body {}\n", encoding="utf-8")
            template = root / "template.html"
            template.write_text(TEMPLATE, encoding="utf-8")

            generated = build_site(content, template, static, output, "/docs/")

            self.assertEqual(
                generated, [output / "guides" / "start.html", output / "index.html"]
            )
            self.assertTrue((output / "styles.css").is_file())
            self.assertIn(
                "<h1>Start</h1>",
                (output / "guides" / "start.html").read_text(encoding="utf-8"),
            )

    def test_build_site_keeps_old_output_on_render_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = root / "content"
            static = root / "static"
            output = root / "public"
            content.mkdir()
            static.mkdir()
            output.mkdir()
            (content / "index.md").write_text("No title", encoding="utf-8")
            (output / "keep.txt").write_text("stable", encoding="utf-8")
            template = root / "template.html"
            template.write_text(TEMPLATE, encoding="utf-8")

            with self.assertRaises(ValueError):
                build_site(content, template, static, output)

            self.assertEqual((output / "keep.txt").read_text(), "stable")
