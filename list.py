import os
import sys
from typing import List, Mapping, Optional, TypedDict
import json
from utils import get_icon
from refresh_projects import get_projects

MAX_APP_COUNT = 6
keyword = os.getenv("alfred_workflow_keyword")
sys.stderr.write("keyword:   " + keyword + "\n")
query = sys.argv[1]
sys.stderr.write("query:   " + query + "\n")


def handle_app_name() -> Mapping[str, Mapping[str, str]]:
    key_app = {}
    for i in range(1, MAX_APP_COUNT + 1):
        key = os.getenv(f"key{i}")
        app_name = os.getenv(f"app{i}")
        if app_name and key:
            app_name = app_name.split("/")[-1]
            if app_name.endswith(".app"):
                app_name = app_name[:-4]
            key_app[key] = {
                "app_name": app_name,
                "app_path": os.path.expanduser(os.path.expandvars(app_name)),
                "icon_path": get_icon(app_name),
            }
    sys.stderr.write("key_app:   " + str(key_app) + "\n")
    return key_app


class AlfredItem(TypedDict):
    uid: Optional[str]
    title: str
    subtitle: str
    variables: dict[str, str]
    arg: Optional[str]
    icon: dict[str, str]


DEFAULT_ITEM = {
    "title": "No result found",
    "subtitle": "Try another keyword",
    "arg": "refresh_projects",
    "icon": {"path": "./icon.png"},
}


def create_item(project: dict, key_app: dict, keyword: str) -> AlfredItem:
    return {
        "uid": project["path"],
        "title": project["name"],
        "subtitle": project["path"],
        "arg": project["path"],
        "variables": {
            "app_name": key_app[keyword]["app_name"],
            "folder_path": project["path"],
        },
        "icon": {"path": key_app[keyword]["icon_path"]},
    }


def main() -> List[Mapping[str, str]]:
    try:
        key_app = handle_app_name()
        if not key_app or keyword not in key_app:
            raise ValueError("Invalid application configuration")
        projects = get_projects()
        items = (
            [create_item(project, key_app, keyword) for project in projects]
            if projects
            else [DEFAULT_ITEM]
        )

        json.dump({"items": items}, sys.stdout)
        return items
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        return [DEFAULT_ITEM]


if __name__ == "__main__":
    main()
