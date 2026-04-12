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
            if file.endswith(".md") and file not in EXCLUDE_FILES:
                old_path = os.path.join(root, file)
                original_title = os.path.splitext(file)[0]
                
                # 检查是否已经是处于根目录且为6位哈希
                is_hashed = len(original_title) == 6 and all(c in '0123456789abcdef' for c in original_title)
                is_at_root = root == CONTENT_DIR
                
                if is_hashed and is_at_root:
                    continue
                
                try:
                    # 加载笔记
                    post = frontmatter.load(old_path)
                    
                    # 1. 确保中文标题保留在 YAML
                    if 'title' not in post.metadata:
                        post.metadata['title'] = original_title
                    
                    # 2. 将原中文名加入 aliases，修复 Quartz 双链 404
                    if 'aliases' not in post.metadata:
                        post.metadata['aliases'] = [original_title]
                    else:
                        # 确保 aliases 是列表且不重复添加
                        if not isinstance(post.metadata['aliases'], list):
                            post.metadata['aliases'] = [post.metadata['aliases']]
                        if original_title not in post.metadata['aliases']:
                            post.metadata['aliases'].append(original_title)
                    
                    # 3. 生成新文件名并强制移动到 CONTENT_DIR 根目录（实现扁平化）
                    new_filename = get_hash(original_title) + ".md"
                    new_path = os.path.join(CONTENT_DIR, new_filename)
                    
                    # 如果发生碰撞（极低概率），加后缀
                    if os.path.exists(new_path) and old_path != new_path:
                        new_filename = get_hash(original_title + "_alt") + ".md"
                        new_path = os.path.join(CONTENT_DIR, new_filename)

                    # 4. 先写回更新后的元数据
                    with open(old_path, 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(post))
                    
                    # 5. 执行移动和重命名
                    # 如果文件已经在根目录且名字没变，就不操作
                    if old_path != new_path:
                        os.rename(old_path, new_path)
                        print(f"✅ 处理成功: {file} -> {new_filename} (已移至根目录并添加别名)")
                    
                except Exception as e:
                    print(f"❌ 处理 {file} 失败: {e}")

if __name__ == "__main__":
    safe_rename()