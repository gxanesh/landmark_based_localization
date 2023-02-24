import os
import glob2 as glob

# file_path_l = 'stereoL'
# file_path_l = 'stereoR'
#
# removing_files_l = glob.glob('./stereoL/*.png')
# removing_files_r = glob.glob('./stereoR/*.png')
#
# for i in removing_files_l:
#     os.remove(i)
# print("cleared stereoL folder")
# for j in removing_files_r:
#     os.remove(j)
# print("cleared stereoR folder")


def delete_all_stereo(filepath,format = '.png'):
    img_len = len([entry for entry in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, entry))])
    if img_len>0:
        all_images = glob.glob(filepath + '*' + format)  #eg "../landmark_detection/dataset/images/stereoL/*.png"
        # assert isinstance(all_images, object)
        for i in all_images:
            os.remove(i)
    return True
