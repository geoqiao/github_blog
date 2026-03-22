def test_settings_loads_from_yaml():
    """settings object should load without error from config.yaml"""
    from github_blog.config import settings
    assert settings.blog.title
    assert settings.blog.url
    assert settings.github.name


def test_settings_has_content_dir():
    from github_blog.config import settings
    assert settings.blog.content_dir is not None


def test_settings_page_size_positive():
    from github_blog.config import settings
    assert settings.blog.page_size > 0
