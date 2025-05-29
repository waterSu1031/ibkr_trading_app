import subprocess
import os


def main():
    os.chdir(os.path.dirname(__file__))  # 현재 편집 파일 목록으로 초기화

    # 특정 파일이 존재하면 삭제 (사전 web_sync_app 구성 목록)
    # for path in ["web_sync_app", "run.py", "launcher.py", "__pycache__"]:
    #     if os.path.exists(path):
    #         if os.path.isdir(path):
    #             import shutil
    #             shutil.rmtree(path)
    #         else:
    #             os.remove(path)

    # os.chdir(os.path.dirname(__file__))  # 경로 초기화
    subprocess.Popen(["python", "_web_app/launcher.py"])
    subprocess.Popen(["uvicorn", "_dashboard_app.app:app", "--host", "0.0.0.0", "--port", "8000"])
    print("✅ _web_app 과 _dashboard_app 시작 확인")


if __name__ == "__main__":
    main()
