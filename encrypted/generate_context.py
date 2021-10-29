import os
from Pyfhel import Pyfhel

"""Encryption parameters"""
m = 2 ** 15
p = 2 ** 10 + 1
b = 3
intDigits = 8
fracDigits = 32
relinKeySize = 3


def generate_to_folder(folder_name):
    HE = Pyfhel()
    HE.contextGen(p=p, m=m, base=b, intDigits=intDigits, fracDigits=fracDigits)
    HE.keyGen()
    print("Generating Relin Key")
    HE.relinKeyGen(bitCount=16, size=relinKeySize)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    HE.saverelinKey(f"{folder_name}/relin")
    HE.savepublicKey(f"{folder_name}/public")
    HE.savesecretKey(f"{folder_name}/secret")
    HE.saveContext(f"{folder_name}/context")
    HE.multDepth(max_depth=64, delta=0.5, x_y_z=(1, 10, 0.1), verbose=True)


def restore_HE_from(folder_name):
    print("Restoring Pyfhel")
    HE = Pyfhel()
    HE.restoreContext(f"{folder_name}/context")
    HE.restoresecretKey(f"{folder_name}/secret")
    HE.restorepublicKey(f"{folder_name}/public")
    HE.restorerelinKey(f"{folder_name}/relin")
    return HE


# generate_to_folder("default")
# restore_from("default")