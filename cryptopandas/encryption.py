import os
from io import StringIO 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import pandas 


def encrypt_file(data, path_file, password, recipient_key, sep=";"):
    """
        Encrypt DataFrame and save it

        Parameters
        ----------
        data : Pandas Dataframe or string
            DataFrame or string to encrypt and store
        path_file : str, file handle
            File path
        password : byte string. Size 16, 24 or 32
            Password for encrypt data
        sep : str, default ';'
            String of length 1. Field delimiter for the output file.
        recipient_key : byte string, the encoded key, default None.
            RSA public key

        Returns
        -------
        None

        Examples
        --------
        >>> import pandas as pd
        >>> from Crypto.PublicKey import RSA
        >>> df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
        ...                    'mask': ['red', 'purple'],
        ...                    'weapon': ['sai', 'bo staff']})
        >>> recipient_key = RSA.importKey(open("receiver.pem").read())
        >>> encrypt_file(data=df, path_file='data.bin', password=b'ungessaaaaaaable', recipient_key=recipient_key)
        """     

    if not isinstance(data, (pandas.DataFrame, str)):
        raise Exception('Argument data must be string or Pandas Dataframe')

    if isinstance(data, pandas.DataFrame):
        data_bytes = data.to_csv(index=False, sep=sep).encode('utf-8')
    else:
        data_bytes = data.encode('utf-8')
    
    output_file = open(path_file, "wb")

    # Encrpyt password with RSA and save it
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    output_file.write(cipher_rsa.encrypt(password))
    
    # Save iv (initialization vector)
    cipher_aes = AES.new(password, AES.MODE_CBC)
    output_file.write(cipher_aes.iv)
    
    finished = False
    block_size = AES.block_size
    string_len = 1024 * block_size
    
    while not finished:
        string_b = data_bytes[:string_len]
        data_bytes = data_bytes[string_len:]
        if len(string_b) == 0 or len(string_b) % block_size != 0:
            padding_length = (block_size - len(string_b) % block_size) or block_size
            string_b += padding_length * str.encode(chr(padding_length))
            finished = True
        output_file.write(cipher_aes.encrypt(string_b)) 

    output_file.close()
