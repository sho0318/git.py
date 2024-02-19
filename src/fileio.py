import os
import pickle
import hashlib
import zlib

import sys
sys.path.append("../")

h = hashlib.new("sha1")

#オブジェクトを保存する
def save_object(object_hash, object_content):
    dirpath = os.path.join(".", "git", "object", object_hash[:2])
    filename = object_hash[2:]
    try:
        os.makedirs(dirpath)
    except:
        pass

    path = os.path.join(dirpath, filename)
    with open(path, mode="wb") as f:
        f.write(object_content)

#indexに登録されている情報を取得する
def fetch_indexfile():
    with open(os.path.join("git", "index.pkl"), "rb") as f:
        try:
            array = pickle.load(f)
            return array
        except:
            return {}

#indexファイルに記述する
def write_indexfile(array):
    with open(os.path.join("git", "index.pkl"), "wb") as f:
        pickle.dump(array, f)

#SHA-1の生成と圧縮を行い、それぞれを返す
def make_object(object_content):
    encode_content = object_content.encode()
    comp_object = zlib.compress(encode_content, level=1)

    h.update(encode_content)
    object_hash = h.hexdigest()

    return object_hash, comp_object

#与えられたハッシュに対応するオブジェクトを解凍して返す
def fetch_object(object_hash):
    dirpath = os.path.join(".", "git", "object", object_hash[:2])
    filename = object_hash[2:]

    try:
        with open(os.path.join(dirpath, filename), "rb") as f:
            binary_object = f.read()
    except FileNotFoundError:
        sys.exit("there is no object having this hash")
    
    decom_binary_object = zlib.decompress(binary_object)
    return decom_binary_object.decode()

#HEADの参照しているcommitオブジェクトを返す
def fetch_head_commit_hash():
    with open(os.path.join("git", "HEAD"), "r") as f:
        head = f.read()
    
    if head.startswith("refs:"):
        dirpath = head.split()[1]
        with open(os.path.join("git", dirpath), "r") as f:
            commit_hash = f.read()
            return commit_hash
    else:
        return head

#HEADの参照するcommitオブジェクトを変更、branchを参照している場合はbrandhのファイルを変更
def update_head(commit_hash):
    with open(os.path.join("git", "HEAD"), "r") as f:
        head = f.read()
    
    if head.startswith("refs:"):
        dirpath = os.path.join("git", head.split()[1])
    else:
        dirpath = os.path.join("git", "HEAD")

    with open(dirpath, "w") as f:
        f.write(commit_hash)

#HEADの参照するbranchを変更
def change_head_ref(branch_name):
    with open(os.path.join("git", "HEAD"), "w") as f:
        f.write(f"refs: refs/heads/{branch_name}")

#HEADに記述されている内容をcommitハッシュに変更
def change_head_commit_hash(commit_hash):
    with open(os.path.join("git", "HEAD"), "w") as f:
        f.write(commit_hash)

#branch名と参照しているcommitハッシュを辞書型にして返す
def fetch_branchs_head():
    commit_hashs = {}
    refs_path = os.path.join("git", "refs", "heads")
    for name in os.listdir(refs_path):
        with open(os.path.join(refs_path, name), "r") as f:
            commit_hash = f.read()
            if commit_hash in commit_hashs:
                commit_hashs[commit_hash].append(name)
            else:
                commit_hashs[commit_hash] = [name]
    return commit_hashs

#refs/heads以下に存在するすべてのファイル名（branch名）を返す
def get_all_branch_name():
    refs_path = os.path.join("git", "refs", "heads")
    names = os.listdir(refs_path)
    return names

#存在するすべてのbranch名を表示する
def print_branch_name():
    with open(os.path.join("git", "HEAD"), "r") as f:
        head = f.read()
    
    if head.startswith("refs:"):
        tmp = head.split()[1]
        head_refs = tmp.split("/")[-1]
    else:
        head_refs = "HEAD"

    names = get_all_branch_name()
    for name in names:
        if name == head_refs:
            print("*", name)
        else:
            print(name)

#treeオブジェクトを展開し、blobオブジェクトのファイルパスとSHA-1ハッシュ、ファイルの中身を返す。
def deployment_tree(object_hash, filename, blob_objects_array):
    separete_content = fetch_object(object_hash).split("\0")

    if "blob" in separete_content[0]:
        content = fetch_object(object_hash).split("\0")[-1]
        blob_objects_array.append([filename, object_hash, content])
        return blob_objects_array
    else:
        for content in separete_content[1:]:
            try:
                tmp_hash = content.split()[0]
                tmp_name = os.path.join(filename, content.split()[1])
            except:
                return blob_objects_array
            blob_objects_array = deployment_tree(tmp_hash, tmp_name, blob_objects_array)
        return blob_objects_array
    
    
#blobオブジェクトの内容に合わせて、ファイルを変更する
def update_file_from_blob(filepath, blob_content):
    with open(filepath, "w") as f:
        f.write(blob_content)

#HEADの参照しているcommitオブジェクトの内容に合わせて、ファイルを変更する
def change_file_from_head():
    head_hash = fetch_head_commit_hash()
    root_tree_hash = fetch_commit_tree_hash(head_hash)

    blob_objects = deployment_tree(root_tree_hash, "", [])
    for blob_object in blob_objects:
        filepath = blob_object[0]
        blob_content = blob_object[2]
        update_file_from_blob(filepath, blob_content)

#commitオブジェクトの参照しているtreeオブジェクトのSHA-1ハッシュを取得
def fetch_commit_tree_hash(commit_hash):
    commit_object = fetch_object(commit_hash)
    commit_content = commit_object.split("\0")[1]
    root_tree_hash = commit_content.split()[1]
    return root_tree_hash

#オブジェクトのタイプを返す
def get_object_type(object_hash):
    object_content = fetch_object(object_hash)

    header = object_content.split("\0")[0]
    object_type = header.split()[0]
    return object_type

#ブランチの参照するcommitオブジェクトを変更する
def change_branch_hash(branch_name, commit_hash):
    path = os.path.join("git", "refs", "heads", branch_name)
    with open(path, "w") as f:
        f.write(commit_hash)
