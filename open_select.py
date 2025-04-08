import os
import sys
import json
from utils import get_exist_app_name


def main():
    app_items = get_exist_app_name()
    json.dump({"items": app_items}, sys.stdout)


if __name__ == "__main__":
    main()
