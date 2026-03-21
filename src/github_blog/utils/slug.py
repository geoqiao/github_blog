from pypinyin import Style, pinyin
from slugify import slugify


def generate_slug(issue_number: int, tags: list[str]) -> str:
    """
    Generate a SEO friendly slug from an issue number and tags.
    Format: {issue_number}-{tag1}-{tag2}...
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
