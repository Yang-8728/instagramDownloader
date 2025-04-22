import os
import subprocess
import random

# 测试视频源目录
VIDEO_DIR = "/Users/yanglan/video/funny/downloads"
OUTPUT_DIR = "/Users/yanglan/video/funny"
NUM_GROUPS = 2
GROUP_SIZE = 10

# 随机选择 20 个视频并分组
all_mp4s = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
if len(all_mp4s) < NUM_GROUPS * GROUP_SIZE:
    print("❌ 视频数量不足 20 个")
    exit(1)

random.shuffle(all_mp4s)
groups = [all_mp4s[i * GROUP_SIZE:(i + 1) * GROUP_SIZE] for i in range(NUM_GROUPS)]

for idx, group in enumerate(groups, 1):
    fixed_files = []
    for i, filename in enumerate(group):
        input_path = os.path.join(VIDEO_DIR, filename)
        fixed_path = os.path.join(VIDEO_DIR, f"fixed_{idx}_{i:02d}.mp4")
        fixed_files.append(fixed_path)

        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-i", input_path,
            "-vf", "scale=720:1280,fps=30,setpts=PTS-STARTPTS",
            "-af", "aresample=async=1",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-y", fixed_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    filelist_path = os.path.join(VIDEO_DIR, f"test_file_list_{idx}.txt")
    with open(filelist_path, "w") as f:
        for fixed_path in fixed_files:
            f.write(f"file '{fixed_path}'\n")

    output_path = os.path.join(OUTPUT_DIR, f"test_output_{idx}.mp4")
    if idx == 2:
        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-f", "concat", "-safe", "0",
            "-i", filelist_path,
            "-fflags", "+genpts",
            "-vsync", "vfr",
            "-vf", "scale=720:1280",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-avoid_negative_ts", "make_zero",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            "-y", output_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-f", "concat", "-safe", "0",
            "-i", filelist_path,
            "-fflags", "+genpts",
            "-vsync", "vfr",
            "-vf", "scale=720:1280",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            "-y", output_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"✅ 测试拼接完成：{output_path}")
