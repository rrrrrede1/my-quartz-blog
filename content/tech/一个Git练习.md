---
tags:
  - tutorial
---

 >一个我在学习Git的时候的产物
 
 **Git 全场景全流程实操题**（通关挑战）。覆盖了从基础工作流、分支管理、冲突解决，到撤销回滚以及模拟远程协作的绝大部分日常使用场景。

为了方便在==本地==完全独立完成，**第五阶段将使用本地目录来模拟远程仓库（GitHub/GitLab）**，无需配置网络或真实远程权限。

[runoob Git教程](https://www.runoob.com/git/git-tutorial.html)
[Git简明指南](https://www.runoob.com/manual/git-guide/)
### 🗺️ 挑战终局愿景（预期提交图）

完成所有步骤后，你的 Git 提交历史拓扑图最终应该呈现出类似以下结构：

```Plaintext
* (HEAD -> main, origin/main) 解决冲突并合并 feature-profile
|\  
| * (feature-profile) 提交个人资料功能
* | 提交了主页更新（造成冲突的根源）
|/  
* 实现了登录功能 (feature-login)
* 第一个完美的提交 (README)
```

### 🛠️ 实操通关任务单

#### 第一阶段：初始化与基础基础工作流

**任务目标**：初始化仓库，理解暂存区（Stage）与提交历史。

1. 在终端创建一个名为 `git-challenge` 的目录并进入。
    `mkdir git-challenge && cd git-challenge`
2. 初始化该目录为 Git 仓库。
    `git init`
3. 创建一个 `README.md` 文件，写入内容：`# Git 实操挑战项目`。
    
4. 将该文件添加进暂存区，并提交，提交信息为 `"feat: 第一个完美的提交 (README)"`。
    `git add . && git commit -m 'feat: 第一个完美的提交 (README)'`

- **如何查看预期结果**：运行 `git status` 应当显示 `nothing to commit, working tree clean`。
    
- **如何验证答案正确**：运行 `git log --oneline`，应当能看到一条哈希值开头的提交记录。
    

#### 第二阶段：分支开发与快速合并（Fast-Forward）

**任务目标**：体验标准的功能分支开发流程。

1. 创建并切换到一个名为 `feature-login` 的新分支。
    `git checkout -b feature-login`
2. 修改 `README.md`，在文件末尾追加一行：`- [x] 登录功能已完成`。
    
3. 提交这次修改，提交信息为 `"feat: 实现了登录功能 (feature-login)"`。
    
4. 切换回 `main` 分支。
    `git checkout main`
5. 将 `feature-login` 分支的修改合并到 `main` 分支。
    `git merge feature-login`

- **如何查看预期结果**：合并时终端输出中应当出现 `Fast-forward` 字样。
    
- **如何验证答案正确**：在 `main` 分支下运行 `cat README.md`，检查登录功能那一行是否已经存在。
    



#### 第三阶段：制造冲突与人工解决（Three-Way Merge & Conflict）

### 1. 核心原理

Git 触发冲突的必要条件：**两个分支必须从同一个祖先节点（分叉点）出发，在彼此不知情的情况下，修改了同一个文件的相同行。** 如果分支是前后串行的关系，Git 会直接执行 `Fast-forward`（快进合并），而不会产生冲突。

### 2. 实操步骤

#### 步骤一：确保当前分支状态干净

在开始前，确保当前处于 `master`（或 `main`）分支，且没有未提交的修改。



```Bash
git checkout master
git status
```

_预期输出：`nothing to commit, working tree clean`。此时的状态即为两个并行分支的共同起点。_

#### 步骤二：在 master 分支制造第一次修改

1. 打开 `README.md`，在文件末尾追加一行内容：
    
    
    
    ```Plaintext
    - [ ] 主页功能（由管理员在 master 修改）
    ```
    


2. 在本地提交这次修改：
	```bash
	   git add README.md
	   git commit -m "docs: 提交了主页更新（造成冲突的根源）"
	```
	

_此时，`master` 分支已经独自往前走了一个节点。_

#### 步骤三：强行回到过去的起点，创建并行分支

为了让新分支假装“不知道” `master` 刚刚偷跑了一步，我们需要让它基于 `master` **上一次的提交**（即退回一步的祖先节点）来创建。

1. 运行以下命令创建并切换分支（`HEAD~1` 表示当前提交的前一个节点）：
    
    ```Bash
    git checkout -b feature-profile HEAD~1
    ```
    


2. 打开 `README.md`，验证刚才管理员加的“主页功能”在当前分支不存在（确认已成功回到过去的起点）。
3. 在**完全相同的最后一行**，写入属于该分支的内容：
	```text
	   - [x] 个人资料功能（由开发者A修改）
	```

4. 在本地提交这次修改：
    
    
    ```Bash
    git add README.md
    git commit -m "feat: 提交个人资料功能"
    ```
    



#### 步骤四：触发合并冲突
现在，两个分支从同一个起点出发，各自独立前进一步，且修改了同一行。
1. 切换回主分支：
```bash
git checkout master
```

2. 尝试合并 `feature-profile` 分支：
    

`git merge feature-profile`


---

### 3. 预期结果与验证

#### 终端冲突提示
运行合并命令后，终端必然会拒绝自动合并，并弹出以下冲突报错：
```text
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
````

#### 查看分支网络拓扑图

运行以下命令查看提交历史：

```Bash
git log --graph --oneline --all
```

_验证要点：应当能看到清晰的线条分叉，`master` 和 `feature-profile` 各自占据一个独立的并行节点。_

### 4. 解决冲突与完成合并

1. 打开 `README.md`，会看到 Git 自动生成的冲突标记：
    
    
    ```Plaintext
    <<<<<<< HEAD
    - [ ] 主页功能（由管理员在 master 修改）
    =======
    - [x] 个人资料功能（由开发者A修改）
    >>>>>>> feature-profile
    ```
    
1. **人工编辑**：删掉 `<<<<<<< HEAD`、`=======`、`>>>>>>> feature-profile` 这些标记行，根据实际业务需求保留或合并核心代码。
2. **提交解决后的代码**：
```bash
git add README.md
git commit
```

_(注意：此时运行 `git commit` 不需要带 `-m` 参数，Git 会自动生成标准的合并信息，直接保存退出编辑器即可。)_

```bash
Fedora@DESKTOP-OPD1P32:~/projects/git-challenge$ git log --graph --oneline --all
*   7259489 (HEAD -> master) Merge branch 'feature-profile'
|\
| * 1b37005 (feature-profile) feat: 提交个人资料功能
* | b570b3b docs: 提交了主页更新（造成冲突的根源）
|/
* eebf3a8 (feature-login) feat: 实现了登录功能 (feature-login)
* 2759416 feat: 第一个完美的提交 (README)
```


#### 第四阶段：时光机操作（撤销与回滚）

**任务目标**：掌握线上出错时的安全挽救方法。

1. 假设你刚刚合并后，发现代码有严重 Bug，需要安全地撤销这次合并，但**要保留历史痕迹**。
    
2. 使用 `git revert -m 1 HEAD` 来撤销刚刚的合并提交（`-m 1` 表示保留主干分支 `main` 的变更，撤销传入分支的变更）。
    

- **如何查看预期结果**：查看 `README.md`，会发现 `feature-profile` 带来的变更不见了，但 `main` 自己原本的修改还在。
    
- **如何验证答案正确**：运行 `git log --oneline`，会发现多出一条开头的提交：`Revert "Merge branch 'feature-profile'..."`。
    
```bash
Fedora@DESKTOP-OPD1P32:~/projects/git-challenge$ git log --oneline
399579b (HEAD -> master) Revert "Merge branch 'feature-profile'"
7259489 Merge branch 'feature-profile'
1b37005 (feature-profile) feat: 提交个人资料功能
b570b3b docs: 提交了主页更新（造成冲突的根源）
eebf3a8 (feature-login) feat: 实现了登录功能 (feature-login)
2759416 feat: 第一个完美的提交 (README)
```
#### 第五阶段：本地模拟远程协作（Push/Pull/Clone）

**任务目标**：在没有真实网络的情况下，深度模拟团队远程协作。

1. **建立“中央远程仓库”**：
    
    - 退回到上一级目录：`cd ..`
        
    - 创建一个裸仓库（模拟 GitHub 服务器）：`git init --bare remote-repo.git`
        
2. **关联并推送**：
    
    - 回到你的工作目录：`cd git-challenge`
        
    - 关联远程端：`git remote add origin ../remote-repo.git`
        
    - 将 `main` 分支推送到模拟的远程端：`git push -u origin main`
        
3. **模拟同事克隆与提交**：
    
    - 退回上一级目录：`cd ..`
        
    - 模拟同事克隆该项目到新目录：`git clone remote-repo.git git-colleague`
        
    - 进入同事的目录：`cd git-colleague`
        
    - 让同事修改一下 `README.md`（比如在第一行加上 `## 团队协作版`），并提交推送：`git add . && git commit -m "chore: 同事加入了标题" && git push origin main`
        
4. **自己同步远程变更**：
    
    - 回到你自己的工作目录：`cd ../git-challenge`
        
    - 拉取并合并远程新代码：`git pull origin main`
        

- **如何查看预期结果**：在你的 `git-challenge` 目录下查看 `README.md`，应当能看到同事加上的 `## 团队协作版`。
    
- **如何验证答案正确**：运行 `git remote -v` 应当能看到指向 `../remote-repo.git` 的 fetch 和 push 地址。
    

### 🏁 终极答案验证脚本（核对清单）

当你看完以上步骤并实操结束后，在你的主工作目录（`git-challenge`）下依次运行以下三条命令，如果反馈符合预期，说明你已经完全掌握了 Git 的核心场景：

1. **验证提交拓扑结构**：
    
    
    
    ```Bash
    git log --graph --oneline --all
    ```
    
    _预期输出：能看到清晰的线条分叉与合拢，并且有 `origin/main` 和 `HEAD -> main` 标签指向最新或次新的节点。_
```bash
Fedora@DESKTOP-OPD1P32:~/projects/git-learn/git-challenge$ git log --graph --oneline --all
* fd3084f (HEAD -> master, origin/master) chore: 同事加入了标题
* 399579b Revert "Merge branch 'feature-profile'"
*   7259489 Merge branch 'feature-profile'
|\
| * 1b37005 (feature-profile) feat: 提交个人资料功能
* | b570b3b docs: 提交了主页更新（造成冲突的根源）
|/
* eebf3a8 (feature-login) feat: 实现了登录功能 (feature-login)
* 2759416 feat: 第一个完美的提交 (README)
```
    
2. **验证远程关联**：
    
    
    
    ```Bash
    git branch -vv
    ```
    
    _预期输出：`* main [origin/main] ...`，这证明你的本地 main 分支已经正确追踪了远程分支。_

```bash
Fedora@DESKTOP-OPD1P32:~/projects/git-learn/git-challenge$ git branch -vv
  feature-login   eebf3a8 feat: 实现了登录功能 (feature-login)
  feature-profile 1b37005 feat: 提交个人资料功能
* master          fd3084f [origin/master] chore: 同事加入了标题
```
2. **验证操作安全网（万能药）**：
    
    
    
    ```Bash
    git reflog
    ```
    
    _预期输出：能看到你今天在这张白纸上做过的每一步移动（包括 checkout、commit、merge、revert）。只要 reflog 在，你的代码在本地就永远不会丢。_
    

```bash
Fedora@DESKTOP-OPD1P32:~/projects/git-learn/git-challenge$ git reflog
fd3084f (HEAD -> master, origin/master) HEAD@{0}: pull origin master: Fast-forward
399579b HEAD@{1}: revert: Revert "Merge branch 'feature-profile'"
7259489 HEAD@{2}: commit (merge): Merge branch 'feature-profile'
b570b3b HEAD@{3}: checkout: moving from feature-profile to master
1b37005 (feature-profile) HEAD@{4}: commit: feat: 提交个人资料功能
eebf3a8 (feature-login) HEAD@{5}: checkout: moving from master to feature-profile
b570b3b HEAD@{6}: reset: moving to b570b3b
5ccb5e7 HEAD@{7}: checkout: moving from master to master
5ccb5e7 HEAD@{8}: merge feature-profile: Fast-forward
b570b3b HEAD@{9}: checkout: moving from feature-profile to master
5ccb5e7 HEAD@{10}: commit: feat: 提交个人资料功能
b570b3b HEAD@{11}: checkout: moving from master to feature-profile
b570b3b HEAD@{12}: commit: docs: 提交了主页更新（造成冲突的根源）
eebf3a8 (feature-login) HEAD@{13}: merge feature-login: Fast-forward
2759416 HEAD@{14}: checkout: moving from feature-login to master
eebf3a8 (feature-login) HEAD@{15}: commit: feat: 实现了登录功能 (feature-login)
2759416 HEAD@{16}: checkout: moving from master to feature-login
2759416 HEAD@{17}: commit (initial): feat: 第一个完美的提交 (README)
```
