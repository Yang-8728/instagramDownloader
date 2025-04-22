import os
import subprocess
from datetime import datetime
import time
import glob
import requests

DOWNLOAD_PATH = "/Users/yanglan/video/funny"
OUTPUT_DIR = "/Users/yanglan/video/funny"
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

AVATAR_IMAGE_PATH = "avatar.png"
AVATAR_VIDEO_PATH = "avatar.mp4"

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def download_saved_posts():
    if not check_internet_connection():
        print("❌ 网络连接失败")
        return

    # Dummy implementation of login and downloading posts
    print("登录成功，正在下载保存的帖子...")

    # Simulate downloading posts
    time.sleep(2)
    print("下载完成！")

# Step 2: 拼接所有下载的视频
def concatenate_videos():
    history_path = os.path.join(OUTPUT_DIR, "merged.log")
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            merged_history = set(f.read().splitlines())
    else:
        merged_history = set()

    if merged_history:
        pass
    else:
        print("📄 当前无已合并记录")

    video_files = sorted([
        f for f in glob.glob(os.path.join(DOWNLOAD_PATH, "downloads", "*.mp4"))
        if os.path.splitext(os.path.basename(f))[0] not in merged_history
    ])

    if not video_files:
        print("❌ 没有找到视频文件")
        return

    with open("file_list.txt", "w") as f:
        for video in video_files:
            f.write(f"file '{video}'\n")

    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "file_list.txt",
        "-fflags", "+genpts",
        "-vsync", "vfr",
        "-vf", "scale=720:1280",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-avoid_negative_ts", "make_zero",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "output.mp4"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("🛠️ 正在拼接视频，请稍候...")

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    final_path = os.path.join(OUTPUT_DIR, f"{now}.mp4")
    os.rename("output.mp4", final_path)
    print("✅ 视频拼接完成")
    print(f"🎞️ 已拼接视频数量：{len(video_files)}")
    print(f"📂 合并视频已保存到：{final_path}")

    with open(history_path, "a") as log:
        for f in video_files:
            shortcode = os.path.splitext(os.path.basename(f))[0]
            log.write(shortcode + "\n")

    # 拼接完成后日志输出
    merge_log_path = os.path.join(LOG_DIR, f"merge_{now}.log")
    with open(merge_log_path, "w") as merge_log:
        merge_log.write(f"🕒 合并时间：{now}\n")
        merge_log.write(f"📁 合并视频数量：{len(video_files)}\n")
        merge_log.write("📄 合并文件列表：\n")
        for f in video_files:
            merge_log.write(f"  - {os.path.basename(f)}\n")
        merge_log.write(f"\n🎞️ 输出文件：{final_path}\n")

    # 清理视频文件
    deleted = 0
    for f in video_files:
        os.remove(f)
        deleted += 1
    print(f"🧹 已清理下载目录中已合并的视频，共 {deleted} 个")

if __name__ == "__main__":
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕒 开始时间：{start_time}")
    download_saved_posts()
    concatenate_videos()
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ 完成时间：{end_time}")
