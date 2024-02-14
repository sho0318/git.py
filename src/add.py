import sys
sys.path.append("../")

from fileio import *

def make_blob_object(file_content):
    blob_content = f"blob {len(file_content)}\0{file_content}"
    blob_hash, blob_object = make_object(blob_content)
    save_object(blob_hash, blob_object)

    return blob_hash
    
def update_index(blob_hash, filename):
    index_array = fetch_indexfile()
    index_array[filename] = blob_hash
    write_indexfile(index_array)


def add_file(filename):
    with open(filename, "r") as f:
        file_content = f.read()
    
    blob_hash = make_blob_object(file_content)
    update_index(blob_hash, filename)