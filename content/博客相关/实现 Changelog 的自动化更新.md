---
tags:
  - tutorial
---
> 想法：将笔记 repo 里面的 commit 记录以某种方式放到博客的更新记录页面上，并且在每次 commit 自动更新

实现效果：[[changelog]]

目前的流程大概是：**Git Push** -> **CF Pages 监测到更新** -> **CF Pages 在其服务器上执行 `npx quartz build`** -> **部署上线**。

在这种模式下，不需要配置 GitHub Actions。只需要在 Quartz 项目中添加一个**预构建脚本**，并修改 Cloudflare 的**构建命令**即可。

---

### 1. 核心运行流程图解

1. **本地/Obsidian 推送**：你完成笔记并执行 `git push`。
    
2. **CF 环境初始化**：CF Pages 启动一个微型 Linux 容器，克隆你的仓库。
    
3. **执行预处理（关键修改点）**：执行我们自定义的脚本，从 Git 历史中提取你的 Commit，生成 `changelog.md`。
    
4. **Quartz 构建**：执行 `npx quartz build`，此时 Quartz 会把刚生成的 `changelog.md` 一并转换成 HTML。
    
5. **上线**：生成的静态文件发布到 CF 的 CDN。
    

---

### 2. 具体操作步骤

#### 第一步：在项目根目录创建脚本

在你的 Quartz 项目根目录下新建一个文件，命名为 `gen-changelog.sh`：


```bash
#!/bin/bash

# 创建 content 目录（如果不存在）
mkdir -p content

# 写入 Markdown 头部
cat <<EOF > content/changelog.md
---
title: "更新记录"
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
# 包含 小时:分钟 的记录
git log --author="rrrrrede1" --no-merges -n 20 --pretty=format:"- [%ad] %s" --date=format:'%Y-%m-%d %H:%M' >>content/changelog.md

echo "Changelog generated successfully."
```

**注意：** 创建后，请在本地终端运行 `chmod +x gen-changelog.sh` 赋予其执行权限，然后 commit 并 push 这个脚本到仓库。

#### 第二步：修改 Cloudflare Pages 的构建设置

1. 登录 **Cloudflare Dashboard**。
    
2. 进入 **Workers & Pages** -> 选中你的 Quartz 项目。
    
3. 点击 **Settings (设置)** -> **Build & deployments (构建与部署)**。
    
4. 找到 **Build configurations (构建配置)**，点击 **Edit (编辑)**。
    
5. 修改 **Build command (构建命令)**：
    
    - **原命令**：`npx quartz build`
        
    - **新命令**：`bash gen-changelog.sh && npx quartz build`
        
6. 点击 **Save (保存)**。
    
7. 推送一个“空提交”

如果你本地修改了代码或笔记，但不想手动点网页，可以直接通过 Git 触发。如果你没有任何代码想改，只想触发一次构建，可以发送一个“空提交”：

```bash
git commit --allow-empty -m "Trigger manual build"
git push origin main
```

CF Pages 监测到新的 Commit 就会立即开始执行 `bash gen-changelog.sh && npx quartz build`。


---

### 详细代码解释

Cloudflare Pages 在执行构建时，为了节省时间和资源，默认进行的是 **浅克隆 (Shallow Clone)**，也就是它只抓取了最近的一次提交（depth=1）。因此 `git log` 只能看到你刚推送到 GitHub 的那一条信息。

**解决方案：**

在脚本中强制要求 Git 拉取完整的提交历史（Unshallow）。

在执行 `git log` 之前需要加入这行代码：


```bash
# ... 脚本前面的部分 ...

# 关键修正：如果是浅克隆，则拉取完整历史
if [ "$(git rev-parse --is-shallow-repository)" = "true" ]; then
    echo "Shallow repository detected. Fetching full history..."
    git fetch --unshallow
fi

# 然后再执行 git log
git log --author="YourName" --no-merges -n 20 --pretty=format:"- [%ad] %s" --date=format:'%Y-%m-%d' >> content/changelog.md
```

---

1. **脚本执行逻辑**：脚本开头的 `> content/changelog.md`（单个大于号）操作是**覆盖写入**。每次构建开始时，它都会把文件清空，然后重新根据 Git 记录填入最新的 20 条。它不会像追加写入那样导致内容无限堆叠。
    
2. **Git 时间戳解析**：
    
    - 在你的命令中，`--date=format:'%Y-%m-%d'` 只是**显示格式**。
        
    - Git 内部依然是按照精确到秒的提交顺序排队的。
        
    - 如果你在同一天（比如 2026-04-11）提交了 3 次，输出结果会像这样：
        
        
        
        ```Markdown
        - [2026-04-11] 修改了关于我页面
        - [2026-04-11] 修正了 Quartz 换行问题
        - [2026-04-11] 增加了更新记录页面
        ```

        

---

如果你觉得同一天的记录太多，分辨不出先后顺序，建议在脚本中把时间显示得更精细一点：

```bash
# 将格式改为包含 小时:分钟
git log --author="YourName" --no-merges -n 20 --pretty=format:"- [%ad] %s" --date=format:'%Y-%m-%d %H:%M' >> content/changelog.md
```

### 验证步骤

1. 修改本地脚本并 `push`。
    
2. 由于你修改了文件，CF Pages 会自动触发部署。
    
3. 检查 CF 构建日志，看是否有 `Fetching full history...` 的输出。
    
4. 部署完成后，查看 `/changelog` 页面，此时应该能看到过去 20 条所有的历史记录了。

```
18:16:37.896 Executing user command: bash gen-changelog.sh && npx quartz build
18:16:37.906 Shallow repository detected. Fetching full history...
18:16:40.342 From https://github.com/rrrrrede1/my-quartz-blog
18:16:40.342  \* \[new branch\] dependabot/github\_actions/ci-dependencies-518f26b0b3 -> origin/dependabot/github\_actions/ci-dependencies-518f26b0b3
18:16:40.342  \* \[new branch\] dependabot/npm\_and\_yarn/production-dependencies-21fcd3ffb9 -> origin/dependabot/npm\_and\_yarn/production-dependencies-21fcd3ffb9
18:16:40.342  \* \[new branch\] main -> origin/main
18:16:40.360 Changelog generated successfully.
```