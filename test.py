import pickle

objdump = None

with open('deleted.dat', 'rb') as f:
    # Stores the now deserialized information into objdump
    objdump = pickle.load(f)

print(objdump)