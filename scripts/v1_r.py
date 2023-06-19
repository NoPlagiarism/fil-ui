"""pip install httpx"""
import os
import shutil

import httpx

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        <script>
            location.href="{REDIRECT_PATH}";
        </script>
        <meta http-equiv="Refresh" content="3; url={REDIRECT_PATH}" />
        <noscript><link rel="canonical" href="{REDIRECT_PATH}" /></noscript>
        <style>a {font-size: large;}</style>
    </head>
    <body>
        <a href="{REDIRECT_PATH}">Click here</a>
    </body>
</html>"""

ALL_JSON_URL = "https://raw.githubusercontent.com/NoPlagiarism/frontend-instances-list/master/instances/all.json"
INSTANCES_TREE_URL = "https://github.com/NoPlagiarism/frontend-instances-list/tree/master/instances/"

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
R_PATH = os.path.join(ROOT_PATH, "r")


def join_urls(a, b):
    return httpx.URL(a).join(b)


def join_path_to_tree(path):
    return join_urls(INSTANCES_TREE_URL, path)


def get_all_json():
    return httpx.get(ALL_JSON_URL).json()


def recreate_directory(path):
    shutil.rmtree(path)
    os.makedirs(path)


class HTMLCreator:
    @staticmethod
    def get_html_for_url(url):
        return HTML_TEMPLATE.replace("{REDIRECT_PATH}", str(url))
    
    @classmethod
    def create_html(cls, path, url):
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        html = cls.get_html_for_url(url)
        with open(path, mode="w+", encoding="utf-8") as f:
            f.write(html)
    
    @classmethod
    def create_html_with_inst_path(cls, inst_path):
        cls.create_html(os.path.join(R_PATH, inst_path + ".html"), join_path_to_tree(inst_path))


def main():
    recreate_directory(R_PATH)
    HTMLCreator.create_html(os.path.join(R_PATH, "index.html"), join_path_to_tree("all.md"))
    data: dict = get_all_json()
    for name, x in data.items():
        HTMLCreator.create_html_with_inst_path(x['path'])
        HTMLCreator.create_html(os.path.join(R_PATH, name + '.html'), join_path_to_tree(x['path']))
    
    for dirpath, _, files in os.walk(R_PATH):
        if dirpath.split("\\")[-1].startswith('.') or dirpath == R_PATH:
            continue
        if len(files) > 1:
            url = join_path_to_tree(dirpath.split("\\")[-1])
        else:
            url = join_path_to_tree("/".join((dirpath.split("\\")[-1], files[0].split('.html')[0])))
        HTMLCreator.create_html(os.path.join(dirpath, "index.html"), url)


if __name__ == "__main__":
    main()
