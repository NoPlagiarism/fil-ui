"""pip install httpx"""
import os
import shutil

import httpx

try:
    from .fil_utils import join_urls, recreate_directory, get_md_nested_list, get_nested_list_by_all_json
except ImportError:
    from fil_utils import join_urls, recreate_directory, get_md_nested_list, get_nested_list_by_all_json


BASE_INSTANCES = "https://raw.githubusercontent.com/NoPlagiarism/frontend-instances-list/master/instances/"
ALL_JSON_URL = join_urls(BASE_INSTANCES, "all.json")
ALL_MD_URL = join_urls(BASE_INSTANCES, "all.md")
INSTANCES_MD_URL = BASE_INSTANCES + "{path}/ReadMe.MD"
BASE_URL = "https://fil.noplagi.xyz/w/"

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
W_PATH = os.path.join(ROOT_PATH, "w")


def get_all_json():
    return httpx.get(ALL_JSON_URL).json()


def link_gen(x):
    return join_urls(BASE_URL, x)


data: dict = get_all_json()
md_nav = get_md_nested_list(get_nested_list_by_all_json(data), link_gen)


class HTMLTemplates:
    EXTERNAL_LINK = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{TITLE}</title>
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <style>
            body {
                background-color: #0d1117;
            }
            .sidebar {
                height: 100%;
                width: 150px;
                position: absolute;
                left: 0;
                top: 0;
                padding-top: 40px;
            }
            .body {
                margin-left: 150px;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <zero-md>
                <template>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/hyrious/github-markdown-css@main/dist/dark.css" />
                </template>
                <script type="text/markdown">{NAV_MD_CODE}</script>
            </zero-md>
        </div>
        <div class="body">
            <zero-md src="{MD_URL}">
                <template>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/hyrious/github-markdown-css@main/dist/dark.css" />
                </template>
            </zero-md>
        </div>
    </body>
</html>"""
    INLINE_MARKDOWN = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{TITLE}</title>
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <style>
            body {
                background-color: #0d1117;
            }
            .sidebar {
                height: 100%;
                width: 150px;
                position: absolute;
                left: 0;
                top: 0;
                padding-top: 40px;
            }
            .body {
                margin-left: 150px;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <zero-md>
                <template>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/hyrious/github-markdown-css@main/dist/dark.css" />
                </template>
                <script type="text/markdown">{NAV_MD_CODE}</script>
            </zero-md>
        </div>
        <div class="body">
            <zero-md>
                <template>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/hyrious/github-markdown-css@main/dist/dark.css" />
                </template>
                <script type="text/markdown">{MD_CODE}</script>
            </zero-md>
        </div>
    </body>
</html>"""

    @classmethod
    def get_external_html(cls, title, md_url):
        return cls.EXTERNAL_LINK.replace("{TITLE}", str(title)).replace("{MD_URL}", str(md_url)).replace("{NAV_MD_CODE}", str(md_nav))
    
    @classmethod
    def get_inline_html(cls, title, md_code):
        return cls.INLINE_MARKDOWN.replace("{TITLE}", str(title)).replace("{MD_CODE}", str(md_code)).replace("{NAV_MD_CODE}", str(md_nav))


class HTMLCreator:
    @staticmethod
    def write_html_file(path, content):
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        with open(path, mode="w+", encoding="utf-8") as f:
            f.write(content)
    
    @classmethod
    def create_instance_html(cls, instance_path):
        cls.write_html_file(os.path.join(W_PATH, instance_path + '.html'), HTMLTemplates.get_external_html(instance_path.split("/")[-1], INSTANCES_MD_URL.format(path=instance_path)))
    
    @staticmethod
    def create_md_list(instance_names):
        res = list()
        for x in instance_names:
            res.append(f"- [{x.split('.html')[0]}]({join_urls(BASE_URL, x)})")
        return "\n".join(res)


def main():
    recreate_directory(W_PATH)
    HTMLCreator.write_html_file(os.path.join(W_PATH, "index.html"), HTMLTemplates.get_external_html("ALL", ALL_MD_URL))
    for name, x in data.items():
        HTMLCreator.create_instance_html(x['path'])
        HTMLCreator.write_html_file(os.path.join(W_PATH, name + '.html'),  HTMLTemplates.get_external_html(x['path'].split("/")[-1], INSTANCES_MD_URL.format(path=x['path'])))
    
    for dirpath, _, files in os.walk(W_PATH):
        if dirpath.split("\\")[-1].startswith('.') or dirpath == W_PATH:
            continue
        if len(files) > 1:
            HTMLCreator.write_html_file(os.path.join(dirpath, "index.html"), HTMLTemplates.get_inline_html(os.path.basename(dirpath), HTMLCreator.create_md_list(files)))



if __name__ == "__main__":
    main()
