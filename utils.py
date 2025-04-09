import os
import sys
import subprocess
import json
import time
from typing import List

MAX_APP_COUNT = 6


NOT_FOUND_PROJECT_ITEM = {
    "uid": "no_projects",
    "title": "No Result Found",
    "subtitle": "Please Check Config Path",
    "icon": {"path": "./icon.png"},
}

NOT_INSTALLED_ITEM = {
    "uid": "no_apps",
    "title": "Not Found Configured Apps",
    "subtitle": "Please Install the Configured Apps",
    "icon": {"path": "./icon.png"},
}

NOT_SELECTED_FOLDER_ITEM = {
    "uid": "no_selected_folder",
    "title": "Please Select a Folder",
    "subtitle": "Please Select a Folder",
    "icon": {"path": "./icon.png"},
}

NOT_ENTER_FOLDER_ITEM = {
    "uid": "no_enter_folder",
    "title": "Please Enter a Folder",
    "subtitle": "Please Enter a Folder",
    "icon": {"path": "./icon.png"},
}


# 检查应用是否已安装
def is_app_installed(app_name: str) -> bool:
    if not app_name:
        return False

    common_paths = [
        f"/Applications/{app_name}.app",
        f"{os.path.expanduser('~')}/Applications/{app_name}.app",
    ]

    for path in common_paths:
        if os.path.exists(path):
            sys.stderr.write(f"Found app at: {path}\n")
            return True

    script = f"""
    tell application "System Events"
        return exists application "{app_name}"
    end tell
    """
    try:
        result = subprocess.check_output(["osascript", "-e", script]).decode().strip()
        sys.stderr.write(f"AppleScript check result: {result}\n")
        return result == "true"
    except Exception as e:
        sys.stderr.write(f"Error checking app {app_name}: {str(e)}\n")
        return False


# 加载IDE配置
def load_ide_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error loading config: {str(e)}\n")
        return {}


# 获取应用图标
def get_icon(app_name: str) -> str:
    config = load_ide_config()
    ide_config = config.get(app_name, {})
    return f"./{ide_config.get('icon', 'icon')}.png"


# 获取选中的文件夹路径
def get_folder_path() -> str:
    script = """
    tell application "Finder"
        set theItems to selection
        set filePath to (POSIX path of (the selection as alias))
        if filePath contains " " then
            set filePath to quoted form of filePath
        end if
    end tell
    return filePath
    """
    try:
        # 使用 subprocess 运行 AppleScript
        result = subprocess.check_output(["osascript", "-e", script]).decode().strip()
        return result
    except Exception as e:
        sys.stderr.write(f"Error running AppleScript: {str(e)}\n")
        return ""


# 获取当前Finder窗口的路径
def get_current_finder_path() -> str:
    script = """
    tell application "Finder" 
        if (count of windows) > 0 then
            try
                set currentPath to (POSIX path of (target of front window as alias))
                if currentPath contains " " then
                    set currentPath to quoted form of currentPath
                end if
                return currentPath
            on error
                return ""
            end try
        end if
    end tell
    """
    try:
        result = subprocess.check_output(["osascript", "-e", script]).decode().strip()
        return result
    except Exception as e:
        sys.stderr.write(f"Error getting Finder path: {str(e)}\n")
        return ""


def get_cache_path(cache_type: str) -> str:
    cache_dir = os.getenv("alfred_workflow_cache")
    if not cache_dir:
        return None
    return os.path.join(cache_dir, f"{cache_type}.json")


def load_cache(cache_type: str) -> tuple[any, float]:
    cache_path = get_cache_path(cache_type)
    if not cache_path or not os.path.exists(cache_path):
        return None, 0

    try:
        with open(cache_path, "r") as f:
            data = json.load(f)
            return data.get("items"), data.get("timestamp", 0)
    except Exception as e:
        sys.stderr.write(f"Error loading {cache_type} cache: {str(e)}\n")
        return None, 0


def save_cache(items: list, cache_type: str):
    cache_path = get_cache_path(cache_type)
    if not cache_path:
        return

    try:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump({"items": items, "timestamp": time.time()}, f)
    except Exception as e:
        sys.stderr.write(f"Error saving {cache_type} cache: {str(e)}\n")


def get_folder_paths_from_string(path_str: str) -> List[str]:
    if not path_str:
        return []
    paths = []
    for p in path_str.split(","):
        p = p.strip()
        if p.startswith("~"):
            p = os.path.expanduser(p)
        paths.append(p)
    sys.stderr.write("paths:   " + str(paths) + "\n")
    return paths
