import re


def markdown_to_text_blocks(markdown):
    blocks_regex = re.compile(r"(?:[^\n\s]+?.+\n?)+")
    matched_blocks = blocks_regex.findall(markdown)
    blocks = [block.strip() for block in matched_blocks]
    return blocks


def block_to_block_type(text):
    if is_block_type_heading(text):
        return "heading"
    if is_block_type_code(text):
        return "code"
    if is_block_type_quote(text):
        return "quote"
    if is_block_type_unordered_list(text):
        return "unordered_list"
    if is_block_type_ordered_list(text):
        return "ordered_list"
    return "paragraph"


def is_block_type_heading(text):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    heading_regex = re.compile(r"(^#+ )[^\n]+$")
    hashes = heading_regex.findall(text)
    if len(hashes) != 1:
        return False
    hash_count = hashes[0].count("#")
    if hash_count <= 0 or hash_count > 6:
        return False
    return True


def is_block_type_code(text):
    # Code blocks must start with 3 backticks and end with 3 backticks.
    code_regex = re.compile(r"^```[^`]+```$")
    match = code_regex.fullmatch(text)
    return match != None


def is_block_type_quote(text):
    # Every line in a quote block must start with a > character.
    quote_regex = re.compile(r"^(?:>.*\n*)+$")
    match = quote_regex.fullmatch(text)
    return match != None


def is_block_type_unordered_list(text):
    # Every line in an unordered list block must start with a * or - character, followed by a space.
    unordered_regex = re.compile(r"^(?:[\*-] .*\n*)+$")
    match = unordered_regex.fullmatch(text)
    return match != None


def is_block_type_ordered_list(text):
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    unordered_regex = re.compile(r"^(?:\d+\. .*\n*)+$")
    match = unordered_regex.fullmatch(text)
    if match == None:
        return False
    unordered_regex = re.compile(r"(\d+?)\. .*\n*")
    matches = unordered_regex.findall(text)
    ordered_number = 1
    for number in matches:
        if int(number) != ordered_number:
            return False
        ordered_number += 1
    return True
