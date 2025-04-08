import sys
import json
from refresh_apps import get_exist_app_name, refresh_apps
from utils import get_folder_path


def main():
    folder_path = get_folder_path().strip("'")
    if not folder_path:
        json.dump(
            {
                "items": [
                    {
                        "uid": "folder",
                        "title": "Please select a folder",
                        "subtitle": "Please select a folder",
                        "icon": {"path": "./icon.png"},
                    }
                ]
            },
            sys.stdout,
        )
        return
    app_items = get_exist_app_name(folder_path)
    json.dump({"items": app_items}, sys.stdout)
    refresh_apps()


if __name__ == "__main__":
    main()
