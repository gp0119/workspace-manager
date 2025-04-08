import os
import threading
import sys
from typing import List, Mapping
from utils import get_folder_paths_from_string, load_cache, save_cache

ws = os.getenv("workspace")
sys.stderr.write("ws:   " + str(ws) + "\n")
exclude = os.getenv("exclude")
exclude = exclude.split(",") if exclude else []

CACHE_DURATION = 5  # 缓存时间（分钟）


def get_projects() -> List[Mapping[str, str]]:
    # 尝试从缓存加载
    cached_items, _ = load_cache("projects")

    # 如果缓存有效，直接返回缓存数据
    if cached_items:
        return cached_items
    else:
        return refresh_projects()


def refresh_projects():
    projects = []
    for path in get_folder_paths_from_string(ws):
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                if exclude and name in exclude:
                    continue
                projects.append({"name": name, "path": os.path.join(path, name)})

    # 保存到缓存
    save_cache(projects, "projects")
    return projects
