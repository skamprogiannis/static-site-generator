import unittest

from markdown_parser import markdown_to_html


class TestMarkdownParser(unittest.TestCase):
    def test_renders_headings_and_paragraphs(self):
        html = markdown_to_html(
            "# Static sites\n\nA **small** page with _style_ and `code`."
        )

        self.assertEqual(
            html,
            '<div class="markdown-body"><h1>Static sites</h1>'
            "<p>A <b>small</b> page with <i>style</i> and <code>code</code>.</p></div>",
        )

    def test_renders_links_and_images(self):
        html = markdown_to_html(
            "[Zone01](https://zone01.gr)\n\n![Athens](images/athens.jpg)"
        )

        self.assertIn('<a href="https://zone01.gr">Zone01</a>', html)
        self.assertIn('<img src="images/athens.jpg" alt="Athens">', html)

    def test_renders_lists(self):
        html = markdown_to_html(
            "- Parse Markdown\n- Render HTML\n\n1. Write content\n2. Build the site"
        )

        self.assertIn("<ul><li>Parse Markdown</li><li>Render HTML</li></ul>", html)
        self.assertIn("<ol><li>Write content</li><li>Build the site</li></ol>", html)

    def test_renders_quote(self):
        html = markdown_to_html("> Plain files are portable.\n> Static sites are fast.")

        self.assertIn(
            "<blockquote>Plain files are portable.\nStatic sites are fast.</blockquote>",
            html,
        )

    def test_renders_and_escapes_fenced_code(self):
        html = markdown_to_html("```html\n<h1>Hello & goodbye</h1>\n```")

        self.assertIn(
            '<pre><code class="language-html">&lt;h1&gt;Hello &amp; goodbye&lt;/h1&gt;\n</code></pre>',
            html,
        )

    def test_escapes_raw_html(self):
        html = markdown_to_html("<script>alert('no')</script>")

        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
