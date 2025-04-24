#!/usr/bin/env python3
from login import ensure_logged_in_user, import_session, get_cookiefile
from download import download_saved_posts
from merge import merge_all_downloaded_videos # 新增导入合并函数

# ✅ 确保已经有合法的 IG_USERNAME（自动读取或提示用户输入）
username = ensure_logged_in_user()

# 📄 获取 Firefox 的 cookie 路径
cookiefile = get_cookiefile()

# 🧠 使用 cookie 登录并保存 session
import_session(cookiefile, username)

# ⬇️ 下载已收藏的视频（自动跳过已存在的视频）
download_saved_posts(username)

# 🔀 合并下载好的视频（自动跳过已合并的）
merge_all_downloaded_videos()
