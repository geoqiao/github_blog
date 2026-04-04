def test_settings_loads_from_yaml():
    """settings object should load without error from config.yaml"""
    from github_blog.config import get_settings

    settings = get_settings()
    assert settings.blog.title
    assert settings.blog.url
    assert settings.github.name


def test_settings_advanced_has_defaults():
    from github_blog.config import get_settings

    settings = get_settings()
    assert settings.advanced.page_size > 0
    assert settings.advanced.home_post_count > 0
    assert settings.advanced.language
