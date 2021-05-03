import hashlib

dictionary_hash = {
} #dictionary to store hash is created

#add_to_dict Function takes in file
#hashs file using our own hashing method
#stores into dictionary
def add_to_dict(file):
    value = hash_file(file) #use hash function and stores it in value
    dictionary_hash[file] = value #adds to dictionary 


# CheckSame Function will return True if both files are the same
# False if files are not the same in the dictionary
def check_same(file):
    new_hash = hash_file(file) #creates a new hash for the file being tested
    if new_hash == dictionary_hash.get(file): #checks the dictionary for any files that match the hash
        return True #if found, returns true
    else:
        return False #else, false.

# Hash_file Function takes in a file and then returns the SHA-1 hash
def hash_file(filename):
    #we make a hash object
    h = hashlib.sha1()
    # open file to read contents
    with open(filename, 'rb') as file:
        chunk = 0 #read each chunk and then
        while chunk != b'': #reading each byte
            chunk = file.read(1024)
            h.update(chunk) #update chunk with hash and update
    # then hex the resulting hash object to get our SHA-1 Hash
    return h.hexdigest()
