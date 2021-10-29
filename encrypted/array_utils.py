from Pyfhel import Pyfhel, PyCtxt
import numpy as np


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
    return encrypt_array(decrypt_array(x, HE), HE)


def copy_array(x: np.array):
    result = np.empty(x.size, dtype=PyCtxt)
    i = 0
    for e in x.flatten():
        result[i] = PyCtxt(e)
        i += 1
    return result.reshape(x.shape)


def print_array(x, HE):
    dec = decrypt_array(x, HE)
    print(dec)
