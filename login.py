import os
from instaloader import Instaloader
from dotenv import load_dotenv

load_dotenv()

def get_logged_in_instaloader():
    username = os.getenv("INSTAGRAM_USERNAME")
    if not username:
        raise Exception("❌ 未从环境变量中获取 INSTAGRAM_USERNAME，请检查 .env 文件")
    session_path = os.path.expanduser(f"~/.config/instaloader/session-{username}")
    L = Instaloader()
    if os.path.exists(session_path):
        L.load_session_from_file(username, session_path)
        print("✅ 已使用本地 Session 登录")
    else:
        raise Exception(f"❌ 未找到 Session 文件：{session_path}")
    return L

if __name__ == "__main__":
    loader = get_logged_in_instaloader()
    print("✅ 登录模块测试成功")
