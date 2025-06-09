def markdown_to_blocks(markdown):
    old_blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in old_blocks:
        trimmed_block = block.strip()
        if trimmed_block != "":
            filtered_blocks.append(trimmed_block)

    return filtered_blocks