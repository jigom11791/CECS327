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
}


def add_to_dict(file):
    value = hash_file1(file)
    dictionary_hash[file] = value


# CheckSame will return True if same , False if NOt same
def check_same(file):
    new_hash = hash_file1(file)
    if new_hash == dictionary_hash.get(file):
        return True
    else:
        return False


def hash_file1(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()
