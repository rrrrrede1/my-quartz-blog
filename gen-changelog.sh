#!/bin/bash

# 创建 content 目录（如果不存在）
mkdir -p content

# 写入 Markdown 头部
cat <<EOF >content/changelog.md
---
title: "更新记录"
comments: false
---

这里记录了笔记库的最近动态。内容根据 Git Commit 自动生成。

EOF

# 如果是浅克隆，则拉取完整历史
if [ "$(git rev-parse --is-shallow-repository)" = "true" ]; then
  echo "Shallow repository detected. Fetching full history..."
  git fetch --unshallow
fi

# 提取 commit
#git log --author="rrrrrede1" --no-merges -n 20 --pretty=format:"- [%ad] %s" --date=format:'%Y-%m-%d' >>content/changelog.md
# 包含 小时:分钟
git log --author="rrrrrede1" --no-merges -n 20 --pretty=format:"- [%ad] %s" --date=format:'%Y-%m-%d %H:%M' >>content/changelog.md

echo "Changelog generated successfully."
