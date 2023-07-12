import os
import io
import zipfile

def extract(filename):
    z = zipfile.ZipFile(filename, 'r', metadata_encoding="gbk")
    for f in z.namelist():
        print("EXTRACTING:",f)#---
        # get directory name from file
        dirname = os.path.splitext(f)[0]
        # create new directory
        os.mkdir(dirname)
        # read inner zip file into bytes buffer
        content = io.BytesIO(z.read(f))
        if zipfile.is_zipfile(content):
            zip_file = zipfile.ZipFile(content)
            for i in zip_file.namelist():
                zip_file.extract(i, dirname)
        else:
            print("ERROR:",f,"is not a zip file")


extract("00000.zip")

