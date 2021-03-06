"""
Kod prezentuje implementacje funkcji szyfrujących, deszyfrujących, relinearyzujących i odświeżających szyfrogramy.
"""

from Pyfhel import Pyfhel, PyCtxt
import numpy as np
global refreshes
refreshes = 0


def encrypt_array(x: np.array, HE: Pyfhel):
    result = np.empty(x.size, dtype=PyCtxt)
    i = 0
    for e in x.flatten():
        result[i] = HE.encryptFrac(e)
        i += 1
    return result.reshape(x.shape)


def decrypt_array(x: np.array, HE: Pyfhel):
    result = np.empty(x.size, dtype=PyCtxt)
    i = 0
    for e in x.flatten():
        result[i] = HE.decryptFrac(e)
        i += 1
    return result.reshape(x.shape)


def relinearize_array(x: np.array, HE: Pyfhel):
    for e in x.flatten():
        HE.relinearize(e)


def refresh_array(x: np.array, HE: Pyfhel):
    global refreshes
    refreshes += x.size
    print(f"Refreshing array [{x.size}], total refreshes: {refreshes}")
    return encrypt_array(decrypt_array(x, HE), HE)




