import hashlib
import sys

from fileio import *

h = hashlib.new("sha1")

def make_tree_object(index):
    already_check_dir = []
    tree_content = ""
    for filename in index:
        if "/" in filename: #下の階層がある場合
            dirname = filename.split("/")[0]
            if dirname in already_check_dir:
                break
            child_path = filename[len(dirname)+1:]
            child_index = {child_path: index[filename]}

            for name in index:
                if name == filename: continue
                if name.startswith(dirname + "/"):
                    child_path = name[len(dirname)+1:]
                    hash_tmp = index[name]
                    child_index[child_path] = hash_tmp
            
            tree_hash = make_tree_object(child_index)
            tree_content += f"\0{tree_hash} {dirname}"
            
            already_check_dir.append(dirname)

        else:
            blob_hash = index[filename]
            tree_content += f"\0{blob_hash} {filename}"
    
    header = f"tree {len(tree_content)}"
    tree = header + tree_content
    tree_hash, tree_object = make_object(tree)

    save_object(tree_hash, tree_object)

    return tree_hash


def make_commit_object(tree_hash, commit_message):
    commit_content = f"tree {tree_hash}\n"
    parent_hash = fetch_head_commit_hash()
    if len(parent_hash) > 0:
        commit_content += f"parent {parent_hash}\n"
    commit_content += f"\n{commit_message}\n"

    header = f"commit {len(commit_content)}\0"
    commit_hash, commit_object = make_object(header + commit_content)
    save_object(commit_hash, commit_object)

    return commit_hash


def commit(commit_message):
    index = fetch_indexfile()
    if index == {}:
        print("there is no staging file")
        exit()

    tree_hash = make_tree_object(index)
    commit_hash = make_commit_object(tree_hash, commit_message)
    update_head(commit_hash)
