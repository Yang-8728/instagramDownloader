#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script loads Instagram session cookies from Firefox and saves them as a reusable session file.
该脚本从 Firefox 提取 Instagram 的登录 cookie，并保存为 session 文件。
"""

import glob
import platform
import sqlite3
from os.path import expanduser
from instaloader import Instaloader, ConnectionException

# 🔍 Auto-locate Firefox cookies.sqlite file
# 🔍 自动定位 Firefox cookies.sqlite 文件路径
def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
        "Linux": "~/.mozilla/firefox/*/cookies.sqlite",
    }.get(platform.system(), "~/.mozilla/firefox/*/cookies.sqlite")

    cookiefiles = glob.glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("❌ No Firefox cookies.sqlite file found.\n❌ 未找到 Firefox cookies 文件，请先登录 Instagram。")
    return cookiefiles[0]

# 🧠 Use cookies to simulate login and save session
# 🧠 使用 cookie 登录并保存 session
def import_session(cookiefile, username):
    print(f"📄 Using cookies from: {cookiefile}\n📄 使用的 cookie 文件路径为：{cookiefile}")
    conn = sqlite3.connect(f"file:{cookiefile}?immutable=1", uri=True)

    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except sqlite3.OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    loader = Instaloader(max_connection_attempts=1)
    loader.context._session.cookies.update(cookie_data)
    loader.context.username = username

    print(f"🔐 Verifying login for: {username}\n🔐 正在验证账号：{username}")
    if not loader.test_login():
        raise SystemExit("❌ Login failed. 请确认你已在 Firefox 中登录 Instagram。")

    session_path = expanduser(f"~/.config/instaloader/session-{username}")
    loader.save_session_to_file(session_path)
    print(f"✅ Session saved to: {session_path}\n✅ Session 文件已保存到：{session_path}")


if __name__ == "__main__":
    print("👤 Please login to your Instagram account in Firefox first.\n👤 请先在 Firefox 浏览器中登录你的 Instagram。")
    username = input("🔑 Enter your Instagram username (请输入 Instagram 用户名): ").strip()

    try:
        cookiefile = get_cookiefile()
        import_session(cookiefile, username)
    except (ConnectionException, sqlite3.OperationalError) as e:
        raise SystemExit(f"❌ Cookie import failed: {e}\n❌ Cookie 导入失败：{e}")
