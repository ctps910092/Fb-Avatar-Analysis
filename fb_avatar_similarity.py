import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from skimage.metrics import structural_similarity as ssim

def get_image_fill(orig_img):
    # Create an empty image
    img = np.zeros((124, 124), dtype=np.uint8)
    # Load the original image and paste it in the center of the new image
    h, w = orig_img.shape
    x = (124 - w) // 2
    y = (124 - h) // 2
    img[y:y+h, x:x+w] = orig_img
    return(img)

def compute_similarity(i, j):
    image_i = np.squeeze(gray_images_list[i])
    image_j = np.squeeze(gray_images_list[j])
    image_i = get_image_fill(image_i)
    image_j = get_image_fill(image_j)
    sim, diff = ssim(image_i, image_j, full=True)
    return sim

folder_path = 'fb_avatar_image'
# Get all the .jpg files in the folder
jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

gray_images_list = []

for jpg_file in tqdm(jpg_files):
    file_path = os.path.join(folder_path, jpg_file)
    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_images_list.append(np.array(gray_image))

image_sim_dict = defaultdict(lambda:defaultdict(int))
for i in tqdm(range(len(gray_images_list))):
    for j in range(i+1, len(gray_images_list)):
        image_sim_dict[jpg_files[i]][jpg_files[j]] = compute_similarity(i, j)

image_sim_df = pd.DataFrame(image_sim_dict).stack().reset_index()
image_sim_df.columns = ['user_i', 'user_j', 'sim']
print(image_sim_df.head())
image_sim_df.to_pickle('output/image_sim_df.pkl')