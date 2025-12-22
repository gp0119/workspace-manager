import os
import sys
from typing import List, Mapping, Optional, TypedDict
import json
import subprocess
from refresh_projects import get_projects
from refresh_apps import get_key_app
from utils import NOT_FOUND_PROJECT_ITEM, NOT_INSTALLED_ITEM

MAX_APP_COUNT = 6
keyword = os.getenv("alfred_workflow_keyword")
sys.stderr.write("keyword:   " + keyword + "\n")
query = sys.argv[1]
sys.stderr.write("query:   " + query + "\n")


class AlfredItem(TypedDict):
    uid: Optional[str]
    title: str
    subtitle: str
    variables: dict[str, str]
    arg: Optional[str]
    icon: dict[str, str]


def create_item(project: dict, key_app: dict, keyword: str) -> AlfredItem:
    app_item = key_app[keyword]
    return {
        "uid": project["path"],
        "title": project["name"],
        "subtitle": project["path"],
        "arg": project["path"],
        "variables": {
            "app_name": app_item["app_name"],
            "folder_path": project["path"],
        },
        "icon": {"path": app_item["icon_path"]},
    }


def async_refresh():
    """后台异步刷新缓存"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    refresh_script = os.path.join(script_dir, "refresh.py")
    # 继承当前环境变量（包含 Alfred workflow 的配置）
    subprocess.Popen(
        [sys.executable, refresh_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env=os.environ.copy(),
    )


def main() -> List[Mapping[str, str]]:
    key_app = get_key_app()
    if keyword not in key_app:
        json.dump({"items": [NOT_INSTALLED_ITEM]}, sys.stdout)
        return
    projects = get_projects()
    items = (
        [create_item(project, key_app, keyword) for project in projects]
        if projects
        else [NOT_FOUND_PROJECT_ITEM]
    )

    json.dump({"items": items}, sys.stdout)
    # 异步刷新缓存，不阻塞返回
    async_refresh()


if __name__ == "__main__":
    main()
