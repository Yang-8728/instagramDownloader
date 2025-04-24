#!/usr/bin/env python3
import os
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect
from instaloader import Instaloader, ConnectionException
from dotenv import load_dotenv

load_dotenv()

# 🔍 获取 Firefox cookies.sqlite 文件路径
def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
        "Linux": "~/.mozilla/firefox/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")

    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("❌ No Firefox cookies.sqlite file found.\n❌ 未找到 Firefox cookies 文件，请先登录 Instagram。")
    return cookiefiles[0]

# ✅ 返回 session 文件完整路径
def get_session_file_path(username: str) -> str:
    config_dir = expanduser("~/.config/instaloader")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, f"session-{username}")

# ✅ 检查浏览器登录的 IG 账号是否匹配
def validate_login(cookiefile, input_username):
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    loader = Instaloader(max_connection_attempts=1)
    loader.context._session.cookies.update(cookie_data)

    actual_username = loader.test_login()
    return actual_username == input_username

# 🔐 从 cookie 登录并保存 session 文件
def import_session(cookiefile, username):
    print(f"📄 Using cookies from: {cookiefile}")
    print(f"📄 使用的 cookie 文件路径为：{cookiefile}")

    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    loader = Instaloader(max_connection_attempts=1)
    loader.context._session.cookies.update(cookie_data)
    loader.context.username = username

    print(f"🔐 Verifying login for: {username}\n🔐 正在验证账号：{username}")
    if not loader.test_login():
        raise SystemExit("❌ Login failed. 请确认你已在 Firefox 中登录 Instagram。")

    session_path = get_session_file_path(username)
    loader.save_session_to_file(session_path)
    print(f"✅ Session saved to: {session_path}\n✅ Session 文件已保存到：{session_path}")

# 🚀 确保用户已登录（首次输入并保存到 .env）
def ensure_logged_in_user():
    username = os.getenv("IG_USERNAME")
    if username:
        return username

    print("🔑 IG_USERNAME not found in .env file.")
    while True:
        username = input("🔑 Enter your Instagram username (请输入 Instagram 用户名): ").strip()
        cookiefile = get_cookiefile()
        if validate_login(cookiefile, username):
            # 避免重复写入 .env
            with open(".env", "a+") as f:
                f.seek(0)
                content = f.read()
                if f"IG_USERNAME={username}" not in content:
                    f.write(f"IG_USERNAME={username}\n")
            print(f"✅ IG_USERNAME saved to .env: {username}")
            return username
        else:
            print("❌ Login failed or the account does not match the session.\n❌ 登录失败，或当前浏览器已登录账号与输入不一致，请重试。")
