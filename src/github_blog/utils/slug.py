from pypinyin import Style, pinyin
from slugify import slugify


def generate_slug(issue_number: int, tags: list[str]) -> str:
    """
    Generate a SEO friendly slug from an issue number and tags.
    Format: {issue_number}-{tag1}-{tag2}...

    Note: This function is kept for backward compatibility.
    New code should use generate_slug_from_title().
    """
    if not tags:
        return str(issue_number)

    processed_tags = []
    for tag in tags:
        pinyin_list = pinyin(tag, style=Style.NORMAL)
        pinyin_str = "".join([item[0] for item in pinyin_list])
        processed_tags.append(slugify(pinyin_str, lowercase=True))

    tags_slug = "-".join(processed_tags)
    return f"{issue_number}-{tags_slug}"


def generate_slug_from_title(issue_number: int, title: str, max_length: int = 60) -> str:
    """
    Generate a SEO friendly slug from an issue number and title.
    Format: {issue_number}-{slugified-title}

    The title is converted to pinyin (for CJK characters) and slugified.
    The result is truncated to max_length characters to keep URLs concise.

    Args:
        issue_number: The issue number (guarantees uniqueness and stability)
        title: The issue title
        max_length: Maximum length of the total slug

    Returns:
        A URL-friendly slug string

    Examples:
        >>> generate_slug_from_title(1, "Python 数据分析入门")
        "1-python-shu-ju-fen-xi-ru-men"

        >>> generate_slug_from_title(2, "A" * 100, max_length=30)
        "2-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a-a"
    """
    if not title or not title.strip():
        return str(issue_number)

    # Convert CJK characters to pinyin, joining with hyphens for readability
    pinyin_list = pinyin(title, style=Style.NORMAL)
    pinyin_str = "-".join([item[0] for item in pinyin_list])

    # Slugify the pinyin string (this handles special chars, spaces, etc.)
    title_slug = slugify(pinyin_str, lowercase=True)

    if not title_slug:
        return str(issue_number)

    # Build the full slug prefix (issue_number + hyphen)
    prefix = f"{issue_number}-"

    # Calculate remaining space for the title slug
    remaining_length = max_length - len(prefix)

    if remaining_length <= 0:
        # If issue number itself is too long, just return it
        return str(issue_number)

    # Truncate title_slug if necessary (avoid cutting in the middle of a word)
    if len(title_slug) > remaining_length:
        # Find the last hyphen within the limit
        truncated = title_slug[:remaining_length]
        last_hyphen = truncated.rfind("-")

        # Cut at the last complete word, or just truncate if no hyphen found
        title_slug = truncated[:last_hyphen] if last_hyphen > 0 else truncated

    return f"{prefix}{title_slug}"
