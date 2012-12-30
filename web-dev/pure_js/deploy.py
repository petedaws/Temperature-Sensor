import os
import shutil
src = os.path.dirname(__file__)
src_files = os.listdir(src)
dest = 'C:\Program Files\Apache Software Foundation\Apache2.2\htdocs'
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if (os.path.isfile(full_file_name)):
        shutil.copy(full_file_name, dest)