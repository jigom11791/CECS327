import hashlib

# maybe put file name into dictionary or something
# 1. Hashing function to find what files in the sync(master) folder
#
# 2. Check if the file changed by redoing the hash / check if same
# or check if the modified file name is same

#   3. send hash to server or client and then if same, do nothing

#       if not the same, send file over
#   4. well true loop:
# time interval to automatically check for files and check options
#
# acccount for if more than one file changed.

dictionary_hash = {
    "file_name": "hash"
}


def add_to_dict(file):
    dictionary_hash["file_name"] = file
    value = hash_file(file)
    dictionary_hash["hash"] = value
    print("ASODHSAD", dictionary_hash)


# hashes the file
def hash_file(file):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


# CheckSame will return True if same , False if NOt same
def check_same(file):
    new_hash = hash_file(file)
    print("NEW HASH", new_hash)
    print("Dictionary hash is ", str(dictionary_hash["hash"]).strip("[]'"))
    if new_hash == dictionary_hash.get("hash"):
        return True
    else:
        return False
