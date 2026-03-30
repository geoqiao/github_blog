#!/bin/bash
# 提交前检查脚本
# 使用方法: ./scripts/pre-commit-check.sh

set -e

echo "🔍 运行提交前检查..."

# 检查是否修改了模板/CSS
if git diff --cached --name-only | grep -E "templates/.*\.(html|css)$"; then
    echo ""
    echo "⚠️  检测到模板/CSS 改动，请确认以下检查项："
    echo ""
    echo "  [ ] 已查看 git 历史: git log --oneline -- 文件"
    echo "  [ ] 已对比原始版本: git diff HEAD~n -- 文件"
    echo "  [ ] 已检查现有 CSS 类: grep 'class=' 模板.html"
    echo "  [ ] 已在本地验证效果"
    echo ""
    read -p "是否继续? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 提交取消"
        exit 1
    fi
fi

# 运行测试
echo "🧪 运行测试..."
uv run pytest -v --tb=short

# 代码检查
echo "🔧 运行代码检查..."
uv run ruff check .

echo ""
echo "✅ 所有检查通过！"
