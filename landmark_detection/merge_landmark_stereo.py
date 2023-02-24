import os
from PIL import Image
from tqdm import tqdm

import warnings as warn
warn.filterwarnings("ignore")

from dataset.images.delete_stereo_images import delete_all_stereo

# dir_path = r'./dataset/images/stereoL/'

file_path_l = './dataset/images/stereoL/'
file_path_r = './dataset/images/stereoR/'
file_path_combined = './dataset/images/stereoCombined/'

# get number of images in stereoL folder
img_len = len([entry for entry in os.listdir(file_path_l) if os.path.isfile(os.path.join(file_path_l, entry))])

format = ".png"
all_deleted  = delete_all_stereo(file_path_combined,format)

#delete_all_stereo retuens true if all the images are deleted
# print(img_len, all_deleted)

if all_deleted:
    for i in tqdm(range(1,img_len)):
        image_l = Image.open(file_path_l +'imgL%d.png'%i)
        # image_l.show()
        image_r = Image.open(file_path_r +'imgR%d.png'%i)
        # image_r.show()
        imgL_size = image_l.size
        imgR_size = image_r.size
        # print(L_size,R_size)
        new_image = Image.new('RGB',(2*imgL_size[0], imgR_size[1]), (250,250,250))
        new_image.paste(image_l,(0,0))
        new_image.paste(image_r,(imgL_size[0],0))
        new_image.save(file_path_combined +'mergedStereo%d.png'%i,"PNG")

print(f"Merged and saved Stereo Images")
