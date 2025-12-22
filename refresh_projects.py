import os
import sys
from typing import List, Mapping
from utils import get_folder_paths_from_string, load_cache, save_cache, is_cache_fresh

ws = os.getenv("workspace")
sys.stderr.write("ws:   " + str(ws) + "\n")
exclude = os.getenv("exclude")
exclude = exclude.split(",") if exclude else []


def get_projects() -> List[Mapping[str, str]]:
    """优先返回缓存数据（即使过期），由调用方异步刷新"""
    cached_items, timestamp = load_cache("projects")

    if cached_items:
        return cached_items
    # 仅在完全没有缓存时才同步刷新
    return refresh_projects()


def refresh_projects():
    projects = []
    for path in get_folder_paths_from_string(ws):
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                if exclude and name in exclude:
                    continue
                projects.append({"name": name, "path": os.path.join(path, name)})

    save_cache(projects, "projects")
    return projects
