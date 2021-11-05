import os
import subprocess

if __name__ == "__main__":
    github_event = os.environ.get('GITHUB_EVENT')
    if github_event == "tags":
        version = subprocess.check_output('git describe --tags', shell=True, encoding='utf-8').strip()
    else:
        version = os.environ.get("GITHUB_SHA")

    with open('flask_app/__version__.py', 'w') as f:
        print(f'__version__ = "{version}"', file=f)

    with open('webapp/app/utils/ui_version.js', 'w') as f:
        print(f'export default "{version}";', file=f)
