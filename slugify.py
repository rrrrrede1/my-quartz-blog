import os
import hashlib
import frontmatter # 需要 pip install python-frontmatter

# --- 配置 ---
CONTENT_DIR = "content"
# 排除不需要处理的文件
EXCLUDE_FILES = ["index.md", "changelog.md", "License.md", "friendlink.md", "aboutme.md"]

def get_short_hash(text):
    """生成 6 位短哈希"""
    return hashlib.md5(text.encode()).hexdigest()[:6]

def process_notes():
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md") and file not in EXCLUDE_FILES:
                file_path = os.path.join(root, file)
                
                try:
                    # 解析笔记（自动处理 YAML 和 正文）
                    post = frontmatter.load(file_path)
                    
                    # 检查是否已经存在 slug
                    if 'slug' not in post.metadata:
                        # 基于文件名生成唯一 ID
                        file_name_stem = os.path.splitext(file)[0]
                        short_id = get_short_hash(file_name_stem)
                        
                        # 插入新 slug，同时保留原有的 title 等 metadata
                        post.metadata['slug'] = short_id
                        
                        # 写回文件
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(frontmatter.dumps(post))
                        
                        print(f"Generated slug [{short_id}] for: {file}")
                    else:
                        print(f"Skipped (slug exists): {file}")
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    process_notes()
