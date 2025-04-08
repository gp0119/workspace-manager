import os
import sys
from utils import (
    load_cache,
    save_cache,
    get_icon,
    is_app_installed,
    MAX_APP_COUNT,
)


def get_exist_app_name(folder_path: str) -> list:
    cached_app_names, _ = load_cache("app_names")
    folder_name = folder_path.rstrip("/").split("/")[-1]
    if cached_app_names:
        return render_app_items(cached_app_names, folder_path, folder_name)
    else:
        app_names = refresh_apps()
        return render_app_items(app_names, folder_path, folder_name)


def render_app_items(app_names: list, folder_path: str, folder_name: str) -> list:
    app_items = []
    for app_name in app_names:
        app_items.append(
            {
                "uid": app_name,
                "title": app_name,
                "subtitle": f"Open {folder_name} with {app_name}",
                "variables": {"app_name": app_name, "folder_path": folder_path},
                "icon": {"path": get_icon(app_name)},
                "arg": folder_path,
            }
        )
    return (
        app_items
        if app_items
        else [
            {
                "uid": "no_apps",
                "title": "No installed apps found",
                "subtitle": "Please install the configured apps",
                "icon": {"path": "./icon.png"},
            }
        ]
    )


def refresh_apps() -> list:
    app_names = []
    for i in range(1, MAX_APP_COUNT + 1):
        key = os.getenv(f"key{i}")
        app_name = os.getenv(f"app{i}")
        if app_name and key:
            app_name = app_name.split("/")[-1]
            if app_name.endswith(".app"):
                app_name = app_name[:-4]

            if not is_app_installed(app_name):
                continue
            app_names.append(app_name)

    save_cache(app_names, "app_names")
    return app_names
