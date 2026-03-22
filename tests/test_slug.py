from github_blog.utils.slug import generate_slug


def test_no_tags_returns_issue_number():
    assert generate_slug(42, []) == "42"


def test_ascii_tag_slugified():
    assert generate_slug(1, ["Python"]) == "1-python"


def test_cjk_tag_transliterated():
    # 数据 → shuju
    assert generate_slug(2, ["数据"]) == "2-shuju"


def test_multiple_tags_joined():
    result = generate_slug(3, ["Python", "数据"])
    assert result == "3-python-shuju"


def test_special_chars_stripped():
    assert generate_slug(5, ["C++"]) == "5-c"
