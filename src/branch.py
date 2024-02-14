from fileio import *

def make_branch(branch_name):
    head_hash = fetch_head_commit_hash()
    change_head_ref(branch_name)
    update_head(head_hash)


def checkout_branch(branch_name):
    branch_names = get_all_branch_name()
    if branch_name not in branch_names:
        print("this branch is not exist")
        return

    change_head_ref(branch_name)
    change_file_from_head()


def checkout_hash(commit_hash):
    object_type = get_object_type(commit_hash)

    if object_type != "commit":
        sys.exit("this hash does not represent commit object")

    change_head_commit_hash(commit_hash)
    change_file_from_head()