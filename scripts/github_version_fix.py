import os

if __name__ == "__main__":
    github_ref_type = os.environ.get('GITHUB_REF_TYPE')
    github_sha = os.environ.get("GITHUB_SHA")
    github_ref_name = os.environ.get("GITHUB_REF_NAME")
    if github_ref_type == "tag":
        version = github_ref_name
    elif github_ref_type == "branch":
        version = f"{github_sha[:8]}_{github_ref_name}"
    else:
        version = github_sha

    with open('flask_app/__version__.py', 'w') as f:
        print(f'__version__ = "{version}"', file=f)

    with open('webapp/app/utils/ui_version.js', 'w') as f:
        print(f'export default "{version}";', file=f)
