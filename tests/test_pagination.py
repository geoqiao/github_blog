from typing import Any


def _paginate(issues: list[object], page_size: int) -> list[dict[str, Any]]:
    """Mirror of the pagination logic in cli.py._generate_index"""
    pages = [issues[i : i + page_size] for i in range(0, len(issues), page_size)]
    if not pages:
        pages = [[]]
    total_pages = max(1, len(pages))
    result = []
    for i, page_issues in enumerate(pages, start=1):
        result.append(
            {
                "page": i,
                "pages": total_pages,
                "has_prev": i > 1,
                "has_next": i < total_pages,
                "prev_num": i - 1,
                "next_num": i + 1,
                "issues": page_issues,
            }
        )
    return result


def test_empty_issues_gives_one_page():
    pages = _paginate([], page_size=10)
    assert len(pages) == 1
    assert pages[0]["issues"] == []


def test_exact_page_size_gives_one_page():
    pages = _paginate(list(range(10)), page_size=10)
    assert len(pages) == 1
    assert pages[0]["has_next"] is False
    assert pages[0]["has_prev"] is False


def test_overflow_creates_second_page():
    pages = _paginate(list(range(11)), page_size=10)
    assert len(pages) == 2
    assert pages[0]["has_next"] is True
    assert pages[1]["has_prev"] is True
    assert len(pages[1]["issues"]) == 1


def test_page_numbers_are_one_indexed():
    pages = _paginate(list(range(5)), page_size=2)
    assert [p["page"] for p in pages] == [1, 2, 3]
