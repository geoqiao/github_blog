from github_blog.utils.slug import generate_slug_from_title


def test_title_slug_basic() -> None:
    """Test basic title slug generation."""
    assert (
        generate_slug_from_title(1, "Python 数据分析入门")
        == "1-python-shu-ju-fen-xi-ru-men"
    )


def test_title_slug_ascii_only() -> None:
    """Test with ASCII-only title."""
    assert generate_slug_from_title(2, "Hello World") == "2-hello-world"


def test_title_slug_empty_title() -> None:
    """Test with empty title returns issue number only."""
    assert generate_slug_from_title(3, "") == "3"
    assert generate_slug_from_title(4, "   ") == "4"
    assert generate_slug_from_title(5, None) == "5"  # type: ignore


def test_title_slug_no_cjk() -> None:
    """Test with title containing no CJK characters."""
    assert (
        generate_slug_from_title(6, "Getting Started with FastAPI")
        == "6-getting-started-with-fastapi"
    )


def test_title_slug_special_chars() -> None:
    """Test that special characters are properly handled."""
    # Note: slugify removes & rather than converting to 'and'
    assert (
        generate_slug_from_title(7, "C++ Programming: Tips & Tricks!")
        == "7-c-programming-tips-tricks"
    )


def test_title_slug_max_length() -> None:
    """Test that long titles are truncated to max_length."""
    long_title = "Python " * 20  # Very long title
    result = generate_slug_from_title(8, long_title, max_length=60)
    # Should be truncated and start with issue number
    assert result.startswith("8-")
    assert len(result) <= 60


def test_title_slug_truncation_at_word_boundary() -> None:
    """Test that truncation happens at word boundary when possible."""
    # A title that will be truncated
    title = "Python数据分析入门教程完整指南详细说明"
    result = generate_slug_from_title(9, title, max_length=40)
    # Should not end with a partial word (no hyphen at end)
    assert not result.endswith("-")
    # Should start with issue number
    assert result.startswith("9-")


def test_title_slug_issue_number_only_when_too_long() -> None:
    """Test that only issue number is returned when it's too long for max_length."""
    # An extremely long issue number that leaves no room for title
    result = generate_slug_from_title(9999999999, "Some Title", max_length=5)
    assert result == "9999999999"


def test_title_slug_stability() -> None:
    """Test that the same inputs always produce the same output."""
    title = "机器学习入门教程"
    result1 = generate_slug_from_title(10, title)
    result2 = generate_slug_from_title(10, title)
    assert result1 == result2


def test_title_slug_different_issues_same_title() -> None:
    """Test that different issue numbers produce different slugs even with same title."""
    title = "相同标题"
    result1 = generate_slug_from_title(11, title)
    result2 = generate_slug_from_title(12, title)
    assert result1 != result2
    assert result1.startswith("11-")
    assert result2.startswith("12-")
