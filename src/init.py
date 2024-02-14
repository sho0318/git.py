import os
import shutil
import pathlib

from fileio import change_head_ref

def git_init():
    remove_gitfile()
    make_dir()
    init_branch()
    change_head_ref("master")
    init_index()

def init_branch():
    refs_path = os.path.join("git", "refs", "heads")

    touch_file = pathlib.Path(os.path.join(refs_path, "master"))
    touch_file.touch()

def init_index():
    index_path = os.path.join("git", "index.pkl")

    touch_file = pathlib.Path(index_path)
    touch_file.touch()

def make_dir():
    os.makedirs("git")
    os.makedirs(os.path.join("git", "refs", "heads"))
    os.makedirs(os.path.join("git", "object"))

def remove_gitfile():
    try:
        refs_path = os.path.join("git")
        shutil.rmtree(refs_path)
    except:
        pass