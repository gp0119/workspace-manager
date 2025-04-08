import os
import sys
import json
import time
from typing import List, Mapping
from utils import get_folder_path, load_cache, save_cache

ws = os.getenv("workspace")
exclude = os.getenv("exclude")
exclude = exclude.split(",") if exclude else []

CACHE_DURATION = 5  # 缓存时间（分钟）


def get_projects() -> List[Mapping[str, str]]:
    # 尝试从缓存加载
    cached_items, timestamp = load_cache("projects")
    current_time = time.time()

    # 如果缓存有效，直接返回缓存数据
    if cached_items and (current_time - timestamp) < (CACHE_DURATION * 60):
        return cached_items

    projects = []
    for path in get_folder_path(ws):
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                if exclude and name in exclude:
                    continue
                projects.append({"name": name, "path": os.path.join(path, name)})

    # 保存到缓存
    save_cache(projects, "projects")
    return projects
