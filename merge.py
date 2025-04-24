import os
import subprocess
from datetime import datetime
from tqdm import tqdm

DOWNLOADS_DIR = "downloads"
MERGED_DIR = "merged"
LOG_FILE = "merged.log"
FFMPEG_PATH = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")

def is_ffmpeg_installed():
    return os.path.exists(FFMPEG_PATH)

def merge_all_downloaded_videos():
    if not is_ffmpeg_installed():
        print("❌ ffmpeg.exe not found. Please place it under tools/ffmpeg/bin/")
        return

    os.makedirs(MERGED_DIR, exist_ok=True)

    # 读取已合并的记录
    merged_videos = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            merged_videos = set(line.strip() for line in f)

    # 找到未合并的视频
    all_videos = sorted([
        f for f in os.listdir(DOWNLOADS_DIR)
        if f.lower().endswith(".mp4") and f not in merged_videos
    ])

    if not all_videos:
        print("📭 No new videos to merge.")
        return

    # 生成 input.txt 文件供 ffmpeg 使用
    input_txt = "input.txt"
    with open(input_txt, "w", encoding="utf-8") as f:
        for video in all_videos:
            video_path = os.path.join(DOWNLOADS_DIR, video).replace("\\", "/")
            f.write(f"file '{video_path}'\n")

    # 输出文件名为当前日期+时间
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(MERGED_DIR, f"{timestamp}.mp4")

    # 执行合并
    print(f"🛠️ Merging {len(all_videos)} videos into {output_path}")
    result = subprocess.run([
        FFMPEG_PATH, "-y", "-f", "concat", "-safe", "0", "-i",
        input_txt, "-c", "copy", output_path
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Merged video saved to {output_path}")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for video in all_videos:
                f.write(video + "\n")
    else:
        print(f"❌ Failed to merge videos: {result.stderr}")

    os.remove(input_txt)

if __name__ == "__main__":
    merge_all_downloaded_videos()