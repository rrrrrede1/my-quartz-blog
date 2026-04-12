import os
import hashlib
import frontmatter # pip install python-frontmatter

# --- 配置 ---
CONTENT_DIR = "content"
# 排除不需要处理的文件
EXCLUDE_FILES = ["index.md", "changelog.md", "License.md", "friendlink.md", "aboutme.md"]

def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()[:6]

def safe_rename():
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            # 排除非 md 文件和排除列表中的文件
            if file.endswith(".md") and file not in EXCLUDE_FILES:
                old_path = os.path.join(root, file)
                original_title = os.path.splitext(file)[0]
                
                # 如果文件名已经是 6 位哈希，说明已经处理过，跳过
                if len(original_title) == 6 and all(c in '0123456789abcdef' for c in original_title):
                    continue
                
                try:
                    # 加载笔记内容和元数据
                    post = frontmatter.load(old_path)
                    
                    # 1. 确保原始中文名作为 title 保留，解决网页显示问题
                    if 'title' not in post.metadata:
                        post.metadata['title'] = original_title
                    
                    # 2. 核心：将原始中文名加入 aliases，修复 Quartz 双链 404
                    current_aliases = post.metadata.get('aliases', [])
                    
                    # 统一转为列表处理
                    if isinstance(current_aliases, str):
                        current_aliases = [current_aliases]
                    elif not isinstance(current_aliases, list):
                        current_aliases = []

                    if original_title not in current_aliases:
                        current_aliases.append(original_title)
                    
                    post.metadata['aliases'] = current_aliases
                    
                    # 3. 生成新文件名（保持在原目录）
                    new_filename = get_hash(original_title) + ".md"
                    new_path = os.path.join(root, new_filename)
                    
                    # 碰撞处理
                    if os.path.exists(new_path) and old_path != new_path:
                        new_filename = get_hash(original_title + "_alt") + ".md"
                        new_path = os.path.join(root, new_filename)

                    # 4. 写回更新后的 YAML
                    with open(old_path, 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(post))
                    
                    # 5. 执行原地重命名
                    os.rename(old_path, new_path)
                    print(f"✅ 处理成功: {original_title} -> {new_filename} (已注入别名)")
                    
                except Exception as e:
                    print(f"❌ 处理 {file} 失败: {e}")

if __name__ == "__main__":
    safe_rename()