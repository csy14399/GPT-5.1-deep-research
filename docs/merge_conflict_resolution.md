# 合并冲突解决指南

当 GitHub 提示 “This branch has conflicts that must be resolved” 时，说明当前分支与目标分支存在代码差异，需要先消除冲突才能继续合并。下面提供一套在命令行解决冲突的通用步骤，假设目标分支为 `main`，当前开发分支为 `work`。

## 先决条件
- 已安装 Git。
- 已正确配置远程仓库（`origin` 指向托管服务）。

## 操作步骤
1. **同步远程的最新代码**
   ```bash
   git fetch origin
   ```

2. **切换到目标分支并更新**
   ```bash
   git checkout main
   git pull origin main
   ```

3. **回到自己的开发分支**
   ```bash
   git checkout work
   ```

4. **把目标分支的最新提交合并到当前分支**
   ```bash
   git merge main
   ```
   若出现冲突，Git 会提示哪些文件有冲突。

5. **逐个解决冲突**
   - 打开冲突文件，查找 `<<<<<<<`, `=======`, `>>>>>>>` 标记。
   - 根据需求保留或合并双方代码，删除冲突标记。
   - 修改完成后，保存文件。

6. **标记冲突已解决并提交合并结果**
   ```bash
   git add <冲突文件路径...>
   git commit -m "Resolve merge conflicts with main"
   ```

7. **推送当前分支**
   ```bash
   git push origin work
   ```
   此时再到平台上重新发起或继续合并操作，冲突应已消除。

## 常见问题排查
- **没有远程 `origin`**：使用 `git remote add origin <repo_url>` 先添加远程。
- **切换分支报错有未提交修改**：先 `git status` 查看，必要时 `git stash` 暂存，再切换分支。
- **想放弃本地合并重来**：在冲突未提交前，可使用 `git merge --abort` 恢复到合并前状态。
- **只想保持目标分支的改动**：在合并时使用 `git checkout --theirs <文件>`；若想保留当前分支的改动，用 `git checkout --ours <文件>`，然后再 `git add`。

## 额外提示
- 合并前先运行项目测试（如 `pytest`、`npm test`），确保解决冲突后功能正常。
- 如果希望在 GUI 中解决冲突，可安装 VS Code 等编辑器并使用其内置的冲突解决界面。
- 解决冲突后记得删除无用的临时文件，保持提交简洁。
