# github-blog 🚀

[English](#english) | [简体中文](#简体中文)

---

## 简体中文

### 简介

`github-blog` 是一个极致简洁、自动化程度极高的个人博客框架。它将 GitHub Issues 作为后端编辑器，利用 GitHub Actions 自动触发构建，并最终通过 GitHub Pages 进行分发。

**核心特性**：

- 📝 **以 Issue 为博文**：直接在 GitHub Issues 中写作，支持标签分类。
- 🤖 **全自动化流**：无需本地部署，Issue 更新即刻触发自动构建。
- 🎨 **优雅 UI**：内置精美的 BearMinimal 主题，支持暗色模式。
- 🔍 **SEO 友好**：自动生成 `sitemap.xml`、`robots.txt` 以及语义化的 URL (Slugs)。
- ⚡ **性能卓越**：基于 Python 3.11 和 `uv` 构建，生成速度极快。

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│ github_blog (代码仓库 - 所有源码在这里维护)                   │
│                                                             │
│ ├── src/                  # Python 源代码                   │
│ ├── templates/            # 主题模板 (BearMinimal)           │
│ ├── .github/workflows/    # CI/CD 工作流                    │
│ └── config.yaml           # 博客配置                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ gen_site.yml
                              │ (生成网站并推送)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ geoqiao.github.io (内容仓库 - 仅存放 Issues)                  │
│                                                             │
│ ├── Issues              # 博客文章                          │
│ └── .github/workflows/  │                                   │
│     └── trigger.yml     │ 监听 Issues 事件                  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ trigger.yml
                              │ (Issue 更新时触发)
                              │
                     ┌────────┴────────┐
                     │   GitHub Issues  │
                     │  (你的编辑器)    │
                     └─────────────────┘
```

**完整流程**：

1. 在 `geoqiao.github.io` 创建或编辑 Issue（博客文章）
2. `trigger.yml` 检测到事件，发送 dispatch 到 `github_blog`
3. `github_blog` 的 `gen_site.yml` 运行：
   - 拉取 Issues
   - 生成静态 HTML
   - 推送到 `geoqiao.github.io` 的 main 分支
4. GitHub Pages 检测到更新，自动部署网站

### 如何使用

#### 方式一：直接使用（推荐）

1. **Fork 仓库**：Fork `github-blog` 到你的 GitHub 账号
2. **配置 GitHub Pages**：
   - 进入 `Settings -> Pages`
   - Source 选择 **Deploy from a branch**
   - Branch 选择 **main**，Folder 选择 **/ (root)**
3. **添加 Secret**：
   - 在 `Settings -> Secrets and variables -> Actions` 中添加 `G_T`
   - 值为你的 [GitHub Personal Access Token](https://github.com/settings/tokens)（需要 `repo` 和 `workflow` 权限）
4. **修改配置**：编辑 `config.yaml` 中的博客信息
5. **开始写作**：在仓库的 Issues 中创建文章，添加标签，稍等片刻博客就上线了

#### 方式二：作为上游维护者

如果你想贡献代码或自定义主题：

```bash
# Clone 仓库
git clone https://github.com/geoqiao/github_blog.git
cd github_blog

# 安装依赖
uv sync

# 本地预览
export G_T=ghp_你的token
uv run blog-gen
uv run python -m http.server 8000
```

### 配置说明

编辑 `config.yaml`：

```yaml
github:
  repo: username/username.github.io  # 你的 Issues 仓库

blog:
  title: 我的博客
  url: https://username.github.io/
  author: 你的名字

about:
  avatar: https://github.com/username.png
  bio: 个人简介
```

### 主题

内置主题：`BearMinimal`（简洁优雅，支持暗色模式）

### 示例

- **作者博客**: [geoqiao's Blog](https://geoqiao.github.io/)

### 致谢

本项目深受以下优秀项目的启发：

- [gitblog](https://github.com/yihong0618/gitblog) - 开启了 Issue 写作的先河。
- [Gmeek](https://github.com/Meekdai/Gmeek) - 提供了极简的构建思路。

---

## English

### Introduction

`github-blog` is a minimalist and highly automated personal blog framework. It turns GitHub Issues into a powerful CMS, leverages GitHub Actions for automated builds, and deploys via GitHub Pages.

**Key Features**:

- 📝 **Issue-based Writing**: Write directly in GitHub Issues with label support.
- 🤖 **Zero-Ops Workflow**: No local setup required; build triggers automatically on issue updates.
- 🎨 **Elegant UI**: Built-in BearMinimal theme with dark mode support.
- 🔍 **SEO Ready**: Automated generation of `sitemap.xml`, `robots.txt`, and human-friendly slugs.
- ⚡ **High Performance**: Powered by Python 3.11 and `uv` for lightning-fast site generation.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ github_blog (Code Repository - Source code lives here)      │
│                                                             │
│ ├── src/                  # Python source                   │
│ ├── templates/            # Theme templates (BearMinimal)    │
│ ├── .github/workflows/    # CI/CD workflows                 │
│ └── config.yaml           # Blog configuration              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ gen_site.yml
                              │ (generates & pushes site)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ geoqiao.github.io (Content Repository - Issues only)         │
│                                                             │
│ ├── Issues              # Blog posts                        │
│ └── .github/workflows/  │                                   │
│     └── trigger.yml     │ Listens for Issue events          │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ trigger.yml
                              │ (triggers on Issue update)
                              │
                     ┌────────┴────────┐
                     │   GitHub Issues  │
                     │  (Your Editor)   │
                     └─────────────────┘
```

**Complete Flow**:

1. Create or edit an Issue in `geoqiao.github.io` (your blog post)
2. `trigger.yml` detects the event, sends dispatch to `github_blog`
3. `github_blog`'s `gen_site.yml` runs:
   - Fetches Issues
   - Generates static HTML
   - Pushes to `geoqiao.github.io` main branch
4. GitHub Pages detects the update, auto-deploys

### How to Use

#### Method 1: Direct Use (Recommended)

1. **Fork the repo**: Fork `github-blog` to your GitHub account
2. **Configure GitHub Pages**:
   - Go to `Settings -> Pages`
   - Source: **Deploy from a branch**
   - Branch: **main**, Folder: **/ (root)**
3. **Add Secret**:
   - Go to `Settings -> Secrets and variables -> Actions`, add `G_T`
   - Value: your [GitHub Personal Access Token](https://github.com/settings/tokens) (needs `repo` and `workflow` scopes)
4. **Update config**: Edit `config.yaml` with your blog info
5. **Start writing**: Create Issues with labels, your blog goes live automatically

#### Method 2: For Upstream Maintainers

```bash
# Clone repository
git clone https://github.com/geoqiao/github_blog.git
cd github_blog

# Install dependencies
uv sync

# Local preview
export G_T=your_token
uv run blog-gen
uv run python -m http.server 8000
```

### Configuration

Edit `config.yaml`:

```yaml
github:
  repo: username/username.github.io  # Your Issues repository

blog:
  title: My Blog
  url: https://username.github.io/
  author: Your Name

about:
  avatar: https://github.com/username.png
  bio: Your bio here
```

### Themes

Built-in theme: `BearMinimal` (clean, minimal design with dark mode)

### Live Demo

- **Author's Blog**: [geoqiao's Blog](https://geoqiao.github.io/)

### Credits

This project is inspired by:

- [gitblog](https://github.com/yihong0618/gitblog) - The pioneer of Issue-based blogging.
- [Gmeek](https://github.com/Meekdai/Gmeek) - For the minimalist build philosophy.
