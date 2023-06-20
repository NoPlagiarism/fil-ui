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
