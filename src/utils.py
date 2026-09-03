import re


def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^\s)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\]]+)\]\(([^\s)]+)\)"
    matches = re.findall(pattern, text)
    return matches
