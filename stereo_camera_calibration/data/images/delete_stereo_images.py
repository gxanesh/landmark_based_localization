import os
import glob2 as glob
file_path_l = 'stereoL'
file_path_l = 'stereoR'

removing_files_l = glob.glob('stereoL/*.png')
removing_files_r = glob.glob('stereoR/*.png')

for i in removing_files_l:
    os.remove(i)
print("cleared stereoL folder")
for j in removing_files_r:
    os.remove(j)
print("cleared stereoR folder")
