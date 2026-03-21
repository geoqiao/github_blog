import os
import sys

# 将 src 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from github_blog.cli import run_cli

if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(1)
