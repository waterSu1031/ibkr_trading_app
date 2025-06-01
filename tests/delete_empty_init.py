import os


def delete_empty_init_files(root="."):
    deleted_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename == "__init__.py":
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:  # 내용이 비어 있으면
                        os.remove(file_path)
                        deleted_files.append(file_path)
    return deleted_files

def delete_all_init_files(root_dir):
    print(f"🔍 루트 경로: {os.path.abspath(root_dir)}")
    deleted = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == '__init__.py':
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    deleted.append(file_path)
                except Exception as e:
                    print(f"❌ Error deleting {file_path}: {e}")
    print(f"✅ Deleted {len(deleted)} '__init__.py' files:")
    for path in deleted:
        print(f" - {path}")


if __name__ == "__main__":
    deleted = delete_empty_init_files(".")
    print(f"🧹 삭제된 빈 __init__.py 파일 수: {len(deleted)}")
    for file in deleted:
        print(" -", file)
