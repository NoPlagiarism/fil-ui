"""pip install httpx"""
import os
import shutil

import httpx


def join_urls(a, b):
    return httpx.URL(a).join(b)


def recreate_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def get_nested_list_by_all_json(data: dict):
    # Work with only "a/b". No "a/b/c"
    res = dict()
    for name, instance in data.items():
        for i, x in enumerate(instance['path'].split("/")):
            v = res
            for i1 in range(i+1):
                if instance['path'].count("/") == i1:
                    v.append(x)
                    break
                if instance['path'].split("/")[i1] not in v:
                    v[instance['path'].split("/")[i1]] = list()
                v = v[instance['path'].split("/")[i1]]
    return res


class MarkDownFuncs:
    @staticmethod
    def get_link(text: str, link):
        if link is not None:
            return f"[{text}]({str(link)})"
        else:
            return text
    
    @staticmethod
    def get_list_item(item: str, level: int = 0):
        return f"{' ' * 2 * level}- {item}"


def get_md_nested_list(x, link_generator, _level=0):
    if isinstance(x, dict):
        res = list()
        for k, v in x.items():
            res.append(MarkDownFuncs.get_list_item(MarkDownFuncs.get_link(k, link_generator(k)), _level) + '\n' + get_md_nested_list(v, link_generator, _level+1))
        return "\n".join(res)
    else:  # list or set
        return "\n".join([MarkDownFuncs.get_list_item(MarkDownFuncs.get_link(v, link_generator(v)), _level+1) for v in x])
