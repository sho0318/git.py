import sys

from fileio import *

def check_index():
    array = fetch_indexfile()
    print(array)

def check_log():
    head_commit_hash = fetch_head_commit_hash()
    if head_commit_hash == "":
        print("your current branch does not has any commit")
        sys.exit()

    commit_hashs = fetch_branchs_head()
    if head_commit_hash in commit_hashs:
        commit_hashs[head_commit_hash].append("HEAD")
    else:
        commit_hashs[head_commit_hash] = ["HEAD"]

    print_commit_log(head_commit_hash, commit_hashs)


def print_commit_log(commit_hash, commit_hashs):
    commit_object = fetch_object(commit_hash)
    _, content = commit_object.split("\0")
    print_message = f"commit {commit_hash}"
    if commit_hash in commit_hashs:
        for branch in commit_hashs[commit_hash]:
            print_message += f" ({branch})"
    print_message += f"\n{content}"
    print(print_message)

    if "parent" in content:
        parent = content.split("\n")[1]
        parent_hash = parent.split()[-1]
        print_commit_log(parent_hash, commit_hashs)
    