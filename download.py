import os
from instaloader import Instaloader, Profile, Post
from login import get_session_file_path, ensure_logged_in_user
from utils import suppress_stdout_stderr

DOWNLOAD_DIR = "downloads"
LOG_FILE = "downloaded.log"

def is_video_post(post: Post) -> bool:
    return post.typename == "GraphVideo"

def download_saved_posts(username: str):
    # 加载 Session
    L = Instaloader()
    session_path = get_session_file_path(username)
    L.load_session_from_file(username, filename=session_path)

    # 加载已下载的 Shortcode 日志
    downloaded_shortcodes = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            downloaded_shortcodes = set(line.strip() for line in f)

    # 获取个人资料和收藏
    profile = Profile.from_username(L.context, username)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    count_downloaded = 0
    count_skipped = 0
    newly_downloaded = []

    for post in profile.get_saved_posts():
        if not is_video_post(post):
            continue

        shortcode = post.shortcode
        if shortcode in downloaded_shortcodes:
            count_skipped += 1
            continue

        print(f"⬇️ 正在下载视频：{shortcode}")
        with suppress_stdout_stderr():  # ⛔️ 屏蔽 Instaloader 的输出
            L.download_post(post, target=DOWNLOAD_DIR)
        newly_downloaded.append(shortcode)
        count_downloaded += 1

    # 记录新下载的 Shortcode
    if newly_downloaded:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for code in newly_downloaded:
                f.write(code + "\n")

    print(f"✅ 下载完成：{count_downloaded} 个")
    print(f"📦 已跳过：{count_skipped} 个")

if __name__ == "__main__":
    username = ensure_logged_in_user()
    download_saved_posts(username)
