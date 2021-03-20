from setuptools import find_packages, setup

setup(
    name="crypto-pandas",
    version="0.1",
    description="Encryption and decryption of Pandas DataFrame",
    author="Ablaye FAYE",
    author_email='fayablaye@gmail.com',
    license="BSD 3 clause",
    packages=find_packages(),
    keywords=["Encryption", "Decryption", "DataFrame"],
    install_requires=["pandas>=0.23.0", "pycryptodome>=3.9.9"],
    python_requires='>=3.6',

)