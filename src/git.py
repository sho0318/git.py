import sys

from add import add_file
from commit import commit
from log import check_index, check_log
from branch import make_branch, checkout_branch, checkout_hash
from fileio import print_branch_name
from init import git_init

if __name__ == "__main__":
    args = sys.argv
    try:
        command = args[1]
    except:
        print("you need type the any command")
        sys.exit()
    
    if len(args) > 3:
        print("there are too many arguments")
        sys.exit()
    
    if command == "init":
        git_init()
        
    elif command == "add":
        try:
            argument = args[2]
        except:
            print("add command require the filename")
            sys.exit()
        add_file(argument)
        print(f"add {argument}")

    elif command == "commit":
        try:
            argument = args[2]
        except:
            print("you need set the commit message")
            sys.exit()
        commit(argument)

    elif command == "branch":
        try:
            argument = args[2]
            make_branch(argument)
            print(f"create {argument}")
        except:
            print_branch_name()

    elif command == "checkout":
        try:
            argument = args[2]
        except:
            print("you need set the branch name")
            sys.exit()
        checkout_branch(argument)
        print(f"check out to {argument}")
    
    elif command == "checkout-hash":
        try:
            argument = args[2]
        except:
            print("you need set the commit hash")
            sys.exit()
        checkout_hash(argument)
        print(f"check out to {argument}")

    elif command == "log":
        check_log()

    elif command == "index":
        check_index()

    else:
        print("you type the wrong command")