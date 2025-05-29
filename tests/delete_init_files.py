import os

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

# 사용 예: 현재 디렉토리 기준이면 '.'
if __name__ == '__main__':
    delete_all_init_files("")
