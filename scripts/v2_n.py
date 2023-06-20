"""pip install httpx"""
import os
import shutil

import httpx

try:
    from .fil_utils import join_urls, recreate_directory
except ImportError:
    from fil_utils import join_urls, recreate_directory


class HTMLTemplates:
    EXTERNAL_LINK = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>FIL-UI /n/ {TITLE}</title>
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <style>
            body {
                background-color: #0d1117;
            }
        </style>
    </head>
    <body>
        <noscript><h2>JS must be enabled for this mode. Try using /r/</h2></noscript>
        <zero-md src="{MD_URL}">
            <template>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/hyrious/github-markdown-css@main/dist/dark.css" />
            </template>
        </zero-md>
    </body>
</html>"""
    INLINE_MARKDOWN = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>FIL-UI /n/ {TITLE}</title>
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <style>
            body {
                background-color: #0d1117;
            }
        </style>
    </head>
    <body>
        <noscript><h2>JS must be enabled for this mode. Try using /r/</h2></noscript>
        <zero-md>
            <template>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/hyrious/github-markdown-css@main/dist/dark.css" />
            </template>
            <script type="text/markdown">{MD_CODE}</script>
        </zero-md>
    </body>
</html>"""

    @classmethod
    def get_external_html(cls, title, md_url):
        return cls.EXTERNAL_LINK.replace("{TITLE}", str(title)).replace("{MD_URL}", str(md_url))
    
    @classmethod
    def get_inline_html(cls, title, md_code):
        return cls.INLINE_MARKDOWN.replace("{TITLE}", str(title)).replace("{MD_CODE}", str(md_code))


BASE_INSTANCES = "https://raw.githubusercontent.com/NoPlagiarism/frontend-instances-list/master/instances/"
ALL_JSON_URL = join_urls(BASE_INSTANCES, "all.json")
ALL_MD_URL = join_urls(BASE_INSTANCES, "all.md")
INSTANCES_MD_URL = BASE_INSTANCES + "{path}/ReadMe.MD"
BASE_URL = "https://fil.noplagi,xyz/n/"

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
N_PATH = os.path.join(ROOT_PATH, "n")


def get_all_json():
    return httpx.get(ALL_JSON_URL).json()


class HTMLCreator:
    @staticmethod
    def write_html_file(path, content):
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        with open(path, mode="w+", encoding="utf-8") as f:
            f.write(content)
    
    @classmethod
    def create_instance_html(cls, instance_path):
        cls.write_html_file(os.path.join(N_PATH, instance_path + '.html'), HTMLTemplates.get_external_html(instance_path.split("/")[-1], INSTANCES_MD_URL.format(path=instance_path)))
    
    @staticmethod
    def create_md_list(instance_names):
        res = list()
        for x in instance_names:
            res.append(f"- [{x.split('.html')[0]}]({join_urls(BASE_URL, x)})")
        return "\n".join(res)


def main():
    recreate_directory(N_PATH)
    HTMLCreator.write_html_file(os.path.join(N_PATH, "index.html"), HTMLTemplates.get_external_html("ALL", ALL_MD_URL))
    data: dict = get_all_json()
    for name, x in data.items():
        HTMLCreator.create_instance_html(x['path'])
        HTMLCreator.write_html_file(os.path.join(N_PATH, name + '.html'),  HTMLTemplates.get_external_html(x['path'].split("/")[-1], INSTANCES_MD_URL.format(path=x['path'])))
    
    for dirpath, _, files in os.walk(N_PATH):
        if dirpath.split("\\")[-1].startswith('.') or dirpath == N_PATH:
            continue
        if len(files) > 1:
            HTMLCreator.write_html_file(os.path.join(dirpath, "index.html"), HTMLTemplates.get_inline_html(os.path.basename(dirpath), HTMLCreator.create_md_list(files)))



if __name__ == "__main__":
    main()
