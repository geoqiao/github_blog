## 改动前检查清单

### 基本信息
- [ ] 我已阅读 `/.claude/skills/my-coding-guidelines/SKILL.md`
- [ ] 我已查看本次改动的文件 git 历史 (`git log --oneline -- 文件`)

### 模板/CSS 改动
- [ ] 已检查 `templates/PaperMint/static/css/papermint.css` 现有样式
- [ ] 已对比原始设计 (`git diff HEAD~n -- 文件`)
- [ ] 已在本地验证效果 (`uv run python -m http.server`)

### 代码质量
- [ ] 所有测试通过 (`uv run pytest -v`)
- [ ] 代码检查通过 (`uv run ruff check .`)
- [ ] 类型检查通过 (`uv run ty`)

### Git 规范
- [ ] 提交信息清晰明确
- [ ] 避免 force push 到 main 分支
- [ ] 小步提交，方便回滚

## 改动描述

### 解决了什么问题？
<!-- 描述改动的背景和目的 -->

### 如何解决的？
<!-- 描述具体改动内容 -->

### 测试方法？
<!-- 如何验证改动有效 -->

## 截图（如适用）
<!-- UI 改动必须附截图 -->
