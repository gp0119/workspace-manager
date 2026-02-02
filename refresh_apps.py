import os
import sys
from utils import (
    load_cache,
    save_cache,
    get_icon,
    is_app_installed,
    MAX_APP_COUNT,
    NOT_INSTALLED_ITEM,
)


def get_key_app() -> dict:
    cached_key_app, _ = load_cache("key_app")
    sys.stderr.write(f"cached_key_app: {cached_key_app}\n")
    if cached_key_app:
        return cached_key_app
    else:
        return refresh_apps()


def get_exist_app_name(folder_path: str) -> list:
    key_app = get_key_app()
    folder_name = folder_path.rstrip("/").split("/")[-1]
    return render_app_items(key_app, folder_path, folder_name)


def render_app_items(key_app: dict, folder_path: str, folder_name: str) -> list:
    app_items = []
    for key, app_info in key_app.items():
        app_items.append(
            {
                "uid": key,
                "title": f"{folder_name} 👉 {app_info['app_name']}",
                "subtitle": f"Open {folder_name} with {app_info['app_name']}",
                "variables": {
                    "app_name": app_info["app_name"],
                    "folder_path": folder_path,
                },
                "icon": {"path": app_info["icon_path"]},
                "arg": folder_path,
                "mods": {
                    "cmd": {
                        "subtitle": f"Copy {folder_path} to clipboard",
                        "valid": True,
                    },
                },
            }
        )
    return app_items if app_items else [NOT_INSTALLED_ITEM]


def refresh_apps() -> dict:
    key_app = {}
    for i in range(1, MAX_APP_COUNT + 1):
        key = os.getenv(f"key{i}")
        app_name = os.getenv(f"app{i}")
        if app_name and key:
            app_name = app_name.split("/")[-1]
            if app_name.endswith(".app"):
                app_name = app_name[:-4]
            if not is_app_installed(app_name):
                continue
            key_app[key] = {
                "app_name": app_name,
                "app_path": os.path.expanduser(os.path.expandvars(app_name)),
                "icon_path": get_icon(app_name),
            }

    save_cache(key_app, "key_app")
    return key_app
