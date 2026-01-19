import os
import shutil


def copy_contents(src, dest):
    if not os.path.exists(src):
        raise OSError(f"{src} not found")
    if os.path.exists(dest):
        shutil.rmtree(dest)    
    os.mkdir(dest)
    for item in os.listdir(src):
        fp = os.path.join(src, item)
        print(item, fp)
        if os.path.isfile(fp):
            print(f'{item} is file, copying') 
            shutil.copy(fp,os.path.join(dest, item))
        if os.path.isdir(fp):
            copy_contents(fp, os.path.join(dest, item))

if __name__ == "__main__":
    copy_contents("static", "public")