import os
from io import StringIO 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import pandas


def read_decrypt_file(path_file, private_key, is_dataframe=True, dtype=None,  sep=";"):
    """
    Read and decrypt file

    Parameters
    ----------
    path_file : str, file handle
        File path
    private_key : byte string, the encoded key, default None
        key to decrypt file
    is_dataframe : boolean,
        True if convert string decrypted to Pandas dataframe
    sep : str, default ';'
        String of length 1. Field delimiter if string decypted is pandas dataframe.
 
    Returns
    -------
    Sring or DataFrame

    Examples
    --------
    >>> private_key = RSA.importKey(open("private.pem").read(), passphrase=b'ungessaaaaaaable')
    >>> data = read_decrypt_file(path_file='data.ind')

    """
    # create the cipher config
 
    infile = open(path_file, "rb")

    # Decrypt RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    enc_password = infile.read(private_key.size_in_bytes())
    password = cipher_rsa.decrypt(enc_password)
    
    # Decrypt file with key
    block_size = AES.block_size
    iv = infile.read(block_size)
    cipher_aes = AES.new(password, AES.MODE_CBC, iv)
    
    data = ''
    next_ = b''
    finished = False
    string_len = 1024 * block_size

    while not finished:
        curr, next_ = next_, cipher_aes.decrypt(infile.read(string_len))
        if len(next_) == 0:
            padding_length = curr[-1]
            if padding_length < 1 or padding_length > block_size:
                raise ValueError("bad decrypt pad (%d)" % padding_length)
            curr = curr[:-padding_length]
            finished = True
        data += curr.decode("utf-8")
    
    if is_dataframe:
        data = pandas.read_csv(StringIO(data), dtype=dtype, sep=sep)

    return data
