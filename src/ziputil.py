import os
import zipfile

def zipfolder(path, relname, archive, excludelist):
    paths = os.listdir(path)
    for p in paths:
        if p not in excludelist:
            p1 = os.path.join(path, p) 
            p2 = os.path.join(relname, p)
            if os.path.isdir(p1): 
                zipfolder(p1, p2, archive, excludelist)
            else:
                archive.write(p1, p2) 

def create_zip(path, relname, archname, excludelist=None):
    archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        zipfolder(path, relname, archive, excludelist)
    else:
        archive.write(path, relname)
    archive.close()