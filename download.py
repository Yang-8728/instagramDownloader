import os
from instaloader import Profile, Post
from login import get_logged_in_instaloader

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", os.path.expanduser("~/video/funny/downloads"))

def is_video_post(post: Post) -> bool:
    return post.typename == "GraphVideo"

def download_saved_posts():
    L = get_logged_in_instaloader()
    profile = Profile.from_username(L.context, L.context.username)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    count = 0
    for post in profile.get_saved_posts():
        if is_video_post(post):
            shortcode = post.shortcode
            target_path = os.path.join(DOWNLOAD_DIR, f"{shortcode}.mp4")
            if os.path.exists(target_path):
                continue
            print(f"⬇️ 正在下载视频：{shortcode}")
            L.download_post(post, target=DOWNLOAD_DIR)
            count += 1

    print(f"✅ 下载完成，共下载 {count} 个新视频。")

if __name__ == "__main__":
    download_saved_posts()
