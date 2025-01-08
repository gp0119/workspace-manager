import os
import sys
from typing import List, Mapping, Optional, TypedDict
import json

MAX_APP_COUNT = 6
keyword = os.getenv("alfred_workflow_keyword")

sys.stderr.write("keyword:   " + keyword + "\n")
ws = os.getenv('workspace')
exclude = os.getenv('exclude')
exclude = exclude.split(',') if exclude else []
sys.stderr.write('workspace:   ' + ws + "\n")

def load_ide_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error loading config: {str(e)}\n")
        return {}

def get_query() -> str:
    return sys.argv[1]

def get_folder_path(path_str: str) -> List[str]:
    if not path_str:
        return []
    paths = []
    for p in path_str.split(","):
        p = p.strip()
        if p.startswith('~'):
            p = os.path.expanduser(p)
        paths.append(p)
    sys.stderr.write('paths:   ' + str(paths) + "\n")
    return paths

def update_projects() -> List[Mapping[str,str]]:
    projects = []
    for path in get_folder_path(ws):
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                if exclude and name in exclude:
                    continue
                projects.append({
                    'name': name,
                    'path': os.path.join(path, name)
                })
    return projects

def get_icon(app_name: str) -> str:
    config = load_ide_config()
    ide_config = config.get(app_name, {})
    return f"./{ide_config.get('icon', 'default')}.png"

def get_bundle_id(app_name: str) -> str:
    config = load_ide_config()
    ide_config = config.get(app_name, {})
    return ide_config.get('bundleId', 'com.apple.finder')

def handle_app_name() -> Mapping[str, Mapping[str, str]]:
    key_app = {}
    for i in range(1, MAX_APP_COUNT + 1):
        key = os.getenv(f'key{i}')
        app_name = os.getenv(f'app{i}')
        if app_name and key:
            app_name = app_name.split('/')[-1]
            if app_name.endswith('.app'):
                app_name = app_name[:-4]
            key_app[key] = {
                'app_name': app_name,
                'app_path': os.path.expanduser(os.path.expandvars(app_name)),
                'icon_path': get_icon(app_name),
                'bundle_id': get_bundle_id(app_name)
            }
    sys.stderr.write('key_app:   ' + str(key_app) + "\n")
    return key_app

class AlfredItem(TypedDict):
    uid: Optional[str]
    title: str
    subtitle: str
    arg: Optional[str]
    icon: dict[str, str]

DEFAULT_ITEM = {
    'title': 'No result found',
    'subtitle': 'Try another keyword',
    'icon': {'path': './default.png'}
}

def create_item(project: dict, key_app: dict, keyword: str) -> AlfredItem:
    return {
        'uid': project['path'],
        'title': project['name'],
        'subtitle': project['path'],
        'arg': project['path'],
        'variables': {
            'bundle_id': key_app[keyword]['bundle_id']
        },
        'icon': {
            'path': key_app[keyword]['icon_path']
        }
    }

def filter_projects(projects: List[dict], query: Optional[str]) -> List[dict]:
    if not query:
        return projects
    return [
        project for project in projects
        if query.lower() in project['name'].lower()
    ]



def main() -> List[Mapping[str, str]]:
    try:
        query = get_query()
        sys.stderr.write("query:   " + query + "\n")
        key_app = handle_app_name()
        if not key_app or keyword not in key_app:
            raise ValueError("Invalid application configuration")
        projects = update_projects()
        filtered_projects = filter_projects(projects, query)
        items = [
                create_item(project, key_app, keyword)
                for project in filtered_projects
            ] if filtered_projects else [DEFAULT_ITEM]
            
        print(json.dumps({'items': items}))
        return items
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        return [DEFAULT_ITEM]

if __name__ == '__main__':
    main()

