PaperMod Jinja2 theme

How to use:
- Update `configs/config.yaml`:
  theme:
    path: "templates/PaperMod"

Templates provided:
- `base.html`, `index.html`, `post.html`, `about.html`
- `tag.html`: 标签列表页，展示某个标签下的文章列表
- `tags.html`: 标签索引页，展示所有标签及文章数量

Variables main.py provides to templates:
- index: `issues`, `tags`, `pagination`, `blog_title`, `github_name`, `meta_description`, `google_search_verification` (and `author_name` if present in config)
- post: `issue`, `html_body`, `blog_title`, `github_name`, `meta_description`
- tag: `issues`, `tag_name`, `tags`, `blog_title`, `github_name`, `meta_description`
- tags: `tag_items`, `tags`, `blog_title`, `github_name`, `meta_description`

Notes:
- The theme uses `/templates/default_theme/static/css/prism.css` for syntax highlighting. You can replace it by copying your preferred `prism.css` into `/templates/PaperMod/static/css/` and updating `base.html`.
- Utterances comments are configured to use `{{ github_name }}/{{ github_name }}.github.io`. If your comments repository differs, edit `post.html` accordingly.
