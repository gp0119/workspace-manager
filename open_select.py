import sys
import json
from refresh_apps import get_exist_app_name
from utils import get_folder_path, NOT_SELECTED_FOLDER_ITEM


def main():
    folder_path = get_folder_path().strip("'")
    if not folder_path:
        json.dump(
            {"items": [NOT_SELECTED_FOLDER_ITEM]},
            sys.stdout,
        )
        return
    app_items = get_exist_app_name(folder_path)
    json.dump({"items": app_items}, sys.stdout)


if __name__ == "__main__":
    main()
