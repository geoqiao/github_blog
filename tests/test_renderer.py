from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from github_blog.services.render_service import RenderService


@pytest.fixture
def render():
    return RenderService()


def _make_issue(number=1, title="Test Post", body="Hello **world**", labels=None):
    issue = MagicMock()
    issue.number = number
    issue.title = title
    issue.body = body
    issue.labels = labels or []
    issue.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    issue.updated_at = datetime(2024, 1, 2, tzinfo=timezone.utc)
    return issue


def test_markdown_to_html_renders_bold(render):
    html = render.markdown_to_html("Hello **world**")
    assert "<strong>world</strong>" in html


def test_render_post_contains_title(render):
    issue = _make_issue(title="My Great Post")
    html = render.render_post(issue, slug="1-test", html_body="<p>body</p>")
    assert "My Great Post" in html


def test_render_post_contains_toc_element(render):
    issue = _make_issue()
    html = render.render_post(issue, slug="1-test", html_body="<p>body</p>")
    assert 'id="toc"' in html


def test_render_index_contains_issues(render):
    issues = [_make_issue(number=1, title="Post One"), _make_issue(number=2, title="Post Two")]
    pagination = {"page": 1, "pages": 1, "has_prev": False, "has_next": False, "prev_num": 0, "next_num": 2}
    html = render.render_index(issues, tags=["python"], pagination=pagination, issue_slugs={1: "1-python", 2: "2-python"})
    assert "Post One" in html
    assert "Post Two" in html


def test_render_home_shows_latest_posts(render):
    issues = [_make_issue(number=i, title=f"Post {i}") for i in range(1, 4)]
    html = render.render_home(issues, issue_slugs={i: f"{i}-test" for i in range(1, 4)})
    assert "Post 1" in html


def test_render_tag_page_contains_tag_name(render):
    issues = [_make_issue(title="Tagged Post")]
    html = render.render_tag_page("python", issues, tags=["python"], issue_slugs={1: "1-python"})
    assert "python" in html.lower()


def test_image_has_lazy_loading(render):
    html = render.markdown_to_html("![alt text](https://example.com/img.png)")
    assert '<img loading="lazy"' in html
