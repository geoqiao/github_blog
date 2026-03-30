# AGENTS.md

This file provides essential guidance for AI coding agents working with this repository. The project is bilingual (Chinese/English), with Chinese being the primary language for code comments and documentation.

## Project Overview

`github-blog` 是一个基于 Python 的静态博客生成器，使用 GitHub Issues 作为 CMS（内容管理系统）。它从指定的 GitHub 仓库获取 Issues，将其转换为静态 HTML 文件，并通过 GitHub Pages 部署。

**核心特性：**
- 以 GitHub Issue 为博文，支持标签分类
- 全自动构建流程：Issue 更新自动触发 GitHub Actions 构建
- 内置 PaperMint 主题（Hugo PaperMod 风格），支持暗色模式和中西文排版优化
- SEO 友好：自动生成 sitemap.xml、robots.txt 和语义化 URL Slugs
- 中文标签自动转换为拼音生成友好的 URL

**在线示例：** https://geoqiao.github.io/

## Technology Stack

- **Python**: >=3.9
- **包管理**: uv (现代 Python 包管理器)
- **GitHub API**: PyGithub
- **Markdown 解析**: Marko (支持 GFM 和 pangu 扩展)
- **类型检查**: ty (快速 Python 类型检查器)
- **模板引擎**: Jinja2
- **配置管理**: pydantic-settings
- **RSS/Atom**: feedgen
- **重试机制**: tenacity
- **日志**: structlog

## Project Structure

```
├── src/github_blog/              # 主源代码
│   ├── __init__.py
│   ├── cli.py                   # CLI 入口，BlogGenerator 主类
│   ├── config.py                # Pydantic 配置模型
│   ├── models/                  # 数据模型（目前为空）
│   ├── services/                # 业务逻辑
│   │   ├── __init__.py
│   │   ├── github_service.py    # GitHub API 集成
│   │   └── render_service.py    # Markdown→HTML 渲染、RSS、站点地图
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       └── slug.py              # SEO 友好的 URL slug 生成（支持中文拼音）
├── templates/                   # Jinja2 模板
│   ├── PaperMint/              # 默认主题（Hugo PaperMod 风格）
│   │   ├── base.html           # 基础模板
│   │   ├── index.html          # 文章列表页
│   │   ├── home.html           # 主页/着陆页
│   │   ├── post.html           # 单篇文章页
│   │   ├── tag.html            # 单个标签页
│   │   ├── tags.html           # 标签列表页
│   │   ├── about.html          # 关于页面
│   │   └── static/             # 静态资源（CSS、JS、图片）
│   ├── default_theme/          # 旧版主题（保留）
│   └── seo/                    # SEO 模板
│       ├── sitemap.xml.j2
│       └── robots.txt.j2
├── tests/                      # 测试文件
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_github_service.py
│   ├── test_pagination.py
│   ├── test_renderer.py
│   └── test_slug.py
├── config.yaml                 # 博客配置
├── pyproject.toml             # 包元数据和工具配置
├── main.py                    # 开发入口（调用 cli.run_cli）
└── .github/workflows/         # GitHub Actions 工作流
    └── gen_site.yml           # 自动生成和部署站点
```

## Build and Test Commands

### 环境设置

```bash
# 安装依赖（生产环境）
uv sync

# 安装依赖（包含开发依赖）
uv sync --group dev
```

### 运行博客生成器

```bash
# 本地生成博客（需要 GitHub Token）
uv run blog-gen <GITHUB_TOKEN> <REPO_NAME>

# 示例
uv run blog-gen ghp_xxx geoqiao/geoqiao.github.io
```

### 本地预览

**重要：** 始终从项目根目录启动 HTTP 服务器，不要从 `contents/` 目录启动。

```bash
# 正确：从项目根目录启动
uv run python -m http.server 8000
# 然后访问 http://localhost:8000
```

**原因：** 项目使用绝对路径引用静态资源（如 `/templates/PaperMint/static/css/papermint.css`）。
- `templates/` 目录位于项目根目录
- `contents/` 只是生成的博客文件子目录
- 从 `contents/` 启动会导致静态资源 404 错误

### 运行测试

```bash
# 运行所有测试（含覆盖率报告）
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_config.py

# 详细输出
uv run pytest -v
```

### 代码检查和格式化

```bash
# 运行 ruff 代码检查
uv run ruff check .

# 自动修复代码检查问题
uv run ruff check --fix .

# 格式化代码
uv run ruff format .
```

### 类型检查

```bash
# 运行 ty 类型检查
uv run ty

# 检查特定文件
uv run ty src/github_blog/cli.py
```

## Configuration

所有配置位于 `config.yaml`：

```yaml
blog:
  title: "博客标题"
  description: "博客描述"
  url: "https://username.github.io/"
  content_dir: "./contents/"      # 生成文件的输出目录
  blog_dir: "blog/"               # 文章子目录
  rss_atom_path: "atom.xml"
  author:
    name: "作者名"
    email: "email@example.com"
  page_size: 10                   # 每页文章数

github:
  name: "username"                # GitHub 用户名
  repo: "username/repo"           # Issues 源仓库

GoogleSearchConsole:
  content: "verification_code"    # GSC 验证代码
  verify: true                    # 是否启用验证

theme:
  path: "templates/PaperMint"     # 主题目录
```

配置也可以通过环境变量设置，使用 `APP_` 前缀和 `__` 分隔符，例如：
`APP_BLOG__TITLE="My Blog"`

## Code Style Guidelines

本项目使用 **Ruff** 进行代码检查和格式化，配置在 `pyproject.toml` 中。

### 启用的规则
- **E/W**: pycodestyle 错误和警告
- **F**: Pyflakes
- **I**: isort（导入排序）
- **N**: PEP8 命名规范
- **UP**: pyupgrade（Python 升级检查）
- **B**: flake8-bugbear
- **A**: flake8-builtins
- **C4**: flake8-comprehensions
- **SIM**: flake8-simplify
- **S**: flake8-bandit（安全检查）
- **RUF**: Ruff 特定规则

### 特殊配置
- **E501**: 忽略行长度限制（已通过代码审查）
- **S101**: 在测试文件中允许使用 `assert`

### 格式化风格
- 引号样式：双引号
- 缩进：空格（4个空格）

### 代码注释
代码注释主要使用中文，保持与现有代码风格一致。

## Testing Strategy

### 测试框架
- **pytest**: 测试框架
- **pytest-cov**: 覆盖率报告
- 使用 `unittest.mock` 进行模拟

### 测试结构
- `test_config.py`: 配置加载测试
- `test_slug.py`: URL slug 生成测试（包含中文拼音转换）
- `test_cli.py`: CLI 集成测试（使用 mock）
- `test_github_service.py`: GitHub API 服务测试
- `test_renderer.py`: 渲染服务测试
- `test_pagination.py`: 分页逻辑测试

### 运行测试的注意事项
- 集成测试会切换当前工作目录到临时目录，避免污染项目根目录
- 使用真实的模板文件进行渲染测试
- Mock GitHub API 调用以避免网络依赖

### 覆盖率配置
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "--cov=src --cov-report=term-missing"
```

## Deployment Process

### GitHub Actions 工作流 (`.github/workflows/gen_site.yml`)

**触发条件：**
- `workflow_dispatch`: 手动触发
- `issues`: Issue 被打开或编辑
- `issue_comment`: 新增或编辑评论
- `push`: 推送到 main 分支

**构建任务：**
1. 检出代码
2. 安装 uv 和 Python 3.11
3. 运行 `blog-gen` 生成静态文件（需要 `G_T` secret）
4. 准备站点目录（复制 contents、templates 和根目录文件）
5. 创建 `.nojekyll` 文件（禁用 Jekyll 处理）
6. 上传为 GitHub Pages 产物

**部署任务：**
- 使用 `actions/deploy-pages@v4` 部署到 GitHub Pages

### 必需的环境变量
- `G_T`: GitHub Personal Access Token，需要 `repo` 权限
  - 在仓库 `Settings -> Secrets and variables -> Actions` 中设置

### 构建筛选
工作流包含条件 `github.event_name != 'issues' || github.repository_owner_id == github.event.issue.user.id`，确保只有仓库所有者的 Issue 会触发构建。

## Key Dependencies

| 依赖 | 用途 |
|------|------|
| `pygithub` | GitHub API 客户端 |
| `marko` | Markdown 解析（支持 GFM、pangu） |
| `jinja2` | 模板引擎 |
| `feedgen` | RSS/Atom 订阅生成 |
| `pypinyin` | 中文转拼音（用于 URL slug） |
| `python-slugify` | URL slug 规范化 |
| `pydantic-settings` | 配置管理 |
| `tenacity` | API 调用重试逻辑 |
| `structlog` | 结构化日志 |
| `cachetools`, `lru-dict` | 缓存 |

## Architecture Details

### 数据流

1. `BlogGenerator.generate()` 从 GitHub 获取 Issues（按创建者筛选）
2. 为每个 Issue 生成 slug（中文标题转换为拼音，格式：`{issue_number}-{title-slug}`）
3. 使用 Marko 渲染 Markdown 为 HTML（图片添加 `loading="lazy"`）
4. 输出：
   - 独立文章页（`contents/blog/{slug}.html`）
   - 分页索引页（`contents/index.html`, `contents/page/{n}.html`）
   - 标签页（`contents/tag/{tag}.html`, `contents/tag/index.html`）
   - 主页（`index.html`）
   - RSS/Atom 订阅（`contents/atom.xml`）
   - 站点地图（`sitemap.xml`）
   - robots.txt
   - 关于页面（`contents/about.html`）

### URL Slug 生成规则

格式：`{issue_number}-{slugified-title}`

- Issue number 保证 URL 稳定性和唯一性
- Title 转换为拼音 slug，保证可读性和 SEO 友好
- 超长标题自动截断至 60 字符（在单词边界截断）

示例：
- `1-python-shu-ju-fen-xi-ru-men`（标题：Python 数据分析入门）
- `2-hello-world-guide`（标题：Hello World Guide）
- `10-ji-qi-xue-xi-ru-men`（标题：机器学习入门）

**变更历史**：早期版本使用 tags 生成 slug，因标签变化会导致 URL 变化，现已改为使用 title。

### 图片懒加载

`LazyImageRenderer` 类继承自 Marko 的 `HTMLRenderer`，通过正则注入 `loading="lazy"` 属性：

```python
return re.sub(r"<img\b", '<img loading="lazy"', result, count=1)
```

## Security Considerations

1. **Token 安全**: GitHub Token 通过 GitHub Secrets 注入，不要在代码中硬编码
2. **输入验证**: 使用 Pydantic 模型验证所有配置
3. **XSS 防护**: 
   - Jinja2 模板启用 `autoescape=True`
   - RSS 内容使用 CDATA 包装
4. **依赖安全**: 启用 Ruff 的 `S`（bandit）规则检查安全问题

## Common Tasks

### 添加新模板变量

1. 在 `RenderService._get_common_context()` 中添加变量
2. 更新 `templates/PaperMint/README.md` 中的变量文档

### 修改主题

1. 编辑 `templates/PaperMint/` 下的模板文件
2. 静态资源放在 `templates/PaperMint/static/`
3. 使用 `{{ theme_path }}` 变量引用主题路径

### 添加新页面类型

1. 在 `RenderService` 中添加渲染方法
2. 创建对应的模板文件
3. 在 `BlogGenerator.generate()` 中添加调用

### 调试本地构建

```bash
# 使用 structlog 查看详细日志
uv run blog-gen <TOKEN> <REPO> 2>&1 | jq .
```

## Notes

- 生成的文件（`contents/`、`index.html`、`sitemap.xml`、`robots.txt`）已添加到 `.gitignore`，它们在 CI 中重新生成
- 博客只获取认证用户创建的 Issues（通过 `creator=me` 筛选）
- 项目使用 `uv` 而非 pip 进行包管理
- 开发时注意保持注释和文档的中文一致性
