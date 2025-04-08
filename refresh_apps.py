import os
import time
from utils import (
    load_cache,
    save_cache,
    get_folder_path,
    get_icon,
    is_app_installed,
    CACHE_DURATION,
    MAX_APP_COUNT,
)


def get_exist_app_name() -> list:
    # 尝试从缓存加载
    cached_items, timestamp = load_cache("app_items")
    current_time = time.time()

    # 如果缓存有效，直接返回缓存数据
    if cached_items and (current_time - timestamp) < (CACHE_DURATION * 60):  # 转换为秒
        return cached_items

    app_items = []
    folder_path = get_folder_path()

    # 获取路径最后的文件夹名称
    folder_name = folder_path.rstrip("/").split("/")[-1]

    if not folder_path:
        return [
            {
                "uid": "folder",
                "title": "Please select a folder",
                "subtitle": "Please select a folder",
                "icon": {"path": "./icon.png"},
            }
        ]

    for i in range(1, MAX_APP_COUNT + 1):
        key = os.getenv(f"key{i}")
        app_name = os.getenv(f"app{i}")
        if app_name and key:
            app_name = app_name.split("/")[-1]
            if app_name.endswith(".app"):
                app_name = app_name[:-4]

            if not is_app_installed(app_name):
                continue

            app_items.append(
                {
                    "uid": app_name,
                    "title": app_name,
                    "subtitle": f"Open {folder_name} with {app_name}",
                    "icon": {"path": get_icon(app_name)},
                    "variables": {"app_name": app_name, "folder_path": folder_path},
                    "arg": folder_path,
                }
            )

    if not app_items:
        app_items = [
            {
                "uid": "no_apps",
                "title": "No installed apps found",
                "subtitle": "Please install the configured apps",
                "arg": "refresh_apps",
                "icon": {"path": "./icon.png"},
            }
        ]

    # 保存到缓存
    save_cache(app_items, "app_items")
    return app_items
