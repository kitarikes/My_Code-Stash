import shutil
import os

src = 'annotationv1/'
copy = 'copyv1/'

files = os.listdir(src)

li = ['blur', 'compre', 'clahe', 'rain', 'snow', 'sun', 'noise']

for file in files:
    for ctgr in li:
        cp_file = copy + ctgr + file 
        shutil.copyfile(src+file,cp_file)
