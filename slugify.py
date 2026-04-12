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
            if file.endswith(".md") and file not in EXCLUDE:
                old_path = os.path.join(root, file)
                original_title = os.path.splitext(file)[0]
                
                # 如果已经是哈希（6位16进制），跳过
                if len(original_title) == 6 and all(c in '0123456789abcdef' for c in original_title):
                    continue
                
                try:
                    # 加载笔记
                    post = frontmatter.load(old_path)
                    
                    # 1. 把中文文件名存入 YAML 的 title，确保网页显示正常
                    if 'title' not in post.metadata:
                        post.metadata['title'] = original_title
                    
                    # 2. 生成新文件名
                    new_filename = get_hash(original_title) + ".md"
                    new_path = os.path.join(root, new_filename)
                    
                    # 3. 如果新文件名已存在（极低概率碰撞），加个后缀
                    if os.path.exists(new_path):
                        new_filename = get_hash(original_title + "_alt") + ".md"
                        new_path = os.path.join(root, new_filename)

                    # 4. 写回并更名
                    with open(old_path, 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(post))
                    
                    os.rename(old_path, new_path)
                    print(f"✅ 重命名成功: {original_title} -> {new_filename}")
                    
                except Exception as e:
                    print(f"❌ 处理 {file} 失败: {e}")

if __name__ == "__main__":
    safe_rename()