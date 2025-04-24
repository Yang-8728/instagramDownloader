#!/usr/bin/env python3
import subprocess
import platform
import os
import zipfile
import urllib.request

def is_ffmpeg_installed():
    """Check if ffmpeg is available in system PATH"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def download_and_install_ffmpeg():
    """Download and extract ffmpeg locally into tools/ffmpeg/bin"""
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_dir = os.path.join("tools", "ffmpeg")
    bin_path = os.path.join(ffmpeg_dir, "bin")
    os.makedirs(bin_path, exist_ok=True)
    zip_path = os.path.join(ffmpeg_dir, "ffmpeg.zip")

    print("⬇️ Downloading ffmpeg...")
    urllib.request.urlretrieve(url, zip_path)

    print("📦 Extracting ffmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(ffmpeg_dir)

    # Move contents to bin
    extracted_folders = [f for f in os.listdir(ffmpeg_dir) if os.path.isdir(os.path.join(ffmpeg_dir, f)) and f != "bin"]
    for folder in extracted_folders:
        bin_src = os.path.join(ffmpeg_dir, folder, "bin")
        if os.path.exists(bin_src):
            for file in os.listdir(bin_src):
                src = os.path.join(bin_src, file)
                dst = os.path.join(bin_path, file)
                os.replace(src, dst)
            break

    os.remove(zip_path)
    print("✅ ffmpeg installed successfully to tools/ffmpeg/bin")

def ensure_ffmpeg():
    """Main logic to ensure ffmpeg exists or install it"""
    if is_ffmpeg_installed():
        return

    print("⚠️ ffmpeg not found on your system.")
    choice = input("Would you like to download and install it locally? (Y/n): ").strip().lower()
    if choice in ["y", "yes", ""]:
        download_and_install_ffmpeg()
        print("💡 You may need to update your PATH to include: tools/ffmpeg/bin")
    else:
        print("❌ ffmpeg is required. Please install it manually and re-run the script.")
        exit(1)

if __name__ == "__main__":
    ensure_ffmpeg()
