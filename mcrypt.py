import argparse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

# Defining main function
def main(args):
    p = Path(args.path)
    if not p.exists() :
        print(f"path {args.path} does not exist or can't be accessed: ")
        raise SystemExit
    
    walkInfo(p, args.yestoall)
    if(not args.yestoall):
        userInput = input(("en" if args.encrypt else "de") + "crypt above files? [y/n]: ")
        if userInput != 'y': 
            print('okay then... bye!')
            raise SystemExit
    else:
        print(("en" if args.encrypt else "de") + "crypt above files? [y/n]: y\n")
    
    pwd = args.pwd
    while len(pwd) <= 3:
        pwd = input("use pwd(>=3 chars): ")
        if len(pwd) <= 3:
            print('read less than 3, again:')

    print('and so it was ' + getStarredInput(pwd))
    if(not args.yestoall):
        userInput = input("proceed? [y/n]: ")
        if userInput != 'y': 
            print('okay then... bye!')
            raise SystemExit
    
    walkCrypt(p, pwd, args.encrypt)
    print("====")
    print("All done!")

def walkInfo(path: Path, yestoall: bool):
    print("looking in " + path.absolute().__str__())
    if(path.is_file()):
        print("single file: " + path.name)
        return
    
    found = list(path.rglob('**/*.[pP][dD][fF]'))
    print(f"found {len(found)} files. examples: ")
    i = 0
    while i < len(found) and i < 3: 
        print(found[i].__str__().replace(path.absolute().__str__(), ""))
        i += 1
    if len(found) > 3:
        seeMore = 'y'
        if(not yestoall):
            seeMore = input("wanna see more? [y/n]:")

        if(seeMore == 'y'):
            print("\n".join(item.__str__().replace(path.absolute().__str__(), "") for item in found[3:]))
    
def walkCrypt(path: Path, pwd: str, isEncrypt: bool):
    if(path.is_file()):
        cryptFile(path, pwd, isEncrypt)
        return
    
    for file in path.rglob('**/*.[pP][dD][fF]'):
        cryptFile(file, pwd, isEncrypt)

def cryptFile(fPath: Path, pwd: str, isEncrypt: bool):
    scryptStr = ("en" if isEncrypt else "de") + "crypt"
    print(scryptStr + "ing: " + fPath.name)
    reader = PdfReader(fPath)
    
    if (isEncrypt and reader.is_encrypted) or (not isEncrypt and not reader.is_encrypted):
        print(f"{fPath.name} already {scryptStr}ed, skipping.")
        return
    
    writer = PdfWriter()

    if not isEncrypt:
        reader.decrypt(pwd)
    
    for page in reader.pages:
        writer.add_page(page)

    if isEncrypt:
        writer.encrypt(pwd)

    # Save the new PDF to a file
    encFile = Path(fPath)
    print(f"writing out file: {encFile.name}")
    with open(encFile.absolute().__str__(), "wb") as f:
        writer.write(f)
    
def getStarredInput(pwd: str):
    res = pwd[0]
    i = 2
    while i < len(pwd): 
        res += '*'
        i += 1
    res += pwd[len(pwd) -1]

    return res
# Using the special variable 
# __name__
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="path to scan for pdfs")
    parser.add_argument("-p", "--pwd", action="store", default='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--encrypt", action="store_true", default=True)
    group.add_argument("-d", "--decrypt", action="store_true")
    parser.add_argument("-y", "--yestoall", action="store_true", default=False)
    args = parser.parse_args()
    #print(args._get_kwargs())
    if args.decrypt:
        args.encrypt = False
    main(args)