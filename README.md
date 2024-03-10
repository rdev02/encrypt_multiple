# encrypt_multiple
Set password on multiple pdf files

## prerequisites
```shell
pip install pypdf2 pycryptodome 
```
usage
```shell
% python mcrypt.py -h                                              
usage: mcrypt.py [-h] [-p PWD] [-e | -d] path

positional arguments:
  path               path to scan for pdfs

optional arguments:
  -h, --help         show this help message and exit
  -p PWD, --pwd PWD
  -e, --encrypt
  -d, --decrypt
```

or simply
```
python mcrypt.py -p my_pwd /path/to/folder_or_file
```
to encrypt and 

```
python mcrypt.py -d -p my_pwd /path/to/folder_or_file
```
to decrypt
