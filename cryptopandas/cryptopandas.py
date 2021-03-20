import os
from io import StringIO 
import pandas
from .encryption import encrypt_file
from .decryption import read_decrypt_file


def read_decrypt(path_file, private_key, dtype=None, sep=";"):
    """
    Read and decrypt file

    Parameters
    ----------
    path_file : str, file handle
        File path
    private_key : byte string, the encoded key, default None
        key to decrypt file
    sep : str, default ';'
        String of length 1. Field delimiter
 
    Returns
    -------
    DataFrame

    Examples
    --------
    >>> private_key = RSA.importKey(open("private.pem").read(), passphrase=b'ungessaaaaaaable')
    >>> data = read_decrypt_file(path_file='data.ind')
    """
    return read_decrypt_file(path_file=path_file,
                             private_key=private_key, 
                             is_dataframe=True,
                             dtype=dtype,
                             sep=sep)
        

pandas.read_decrypt = read_decrypt


@pandas.api.extensions.register_dataframe_accessor("crypto")
class CryptoAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def to_encrypt_file(self, path_file, password, sep=";", recipient_key=None):
        """
        Encrypt DataFrame and save it

        Parameters
        ----------
        path_file : str, file handle
            File path
        password : byte string. Size 16, 24 or 32
            Password for encrypt data
        sep : str, default ';'
            String of length 1. Field delimiter for the output file.
        recipient_key : byte string, the encoded key
            RSA public key
        Returns
        -------
        None

        Examples
        --------
        >>> from crypto import pandas as pd
        >>> df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
        ...                    'mask': ['red', 'purple'],
        ...                    'weapon': ['sai', 'bo staff']})
        >>> df.crypto.to_encrypted_file('data.ini', recipient_key=b'ungessaaaaaaable')
        """ 
 
        return encrypt_file(data=self._obj,
                            path_file=path_file,
                            password=password,
                            sep=sep,
                            recipient_key=recipient_key)

