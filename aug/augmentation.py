import numpy as np
import random
import os
import cv2
from matplotlib import pyplot as plt

import albumentations as A

# tmp = os.getcwd()
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# img_dir = "../batawa_pic/batawa_300x400"
img_dir = 'datav1'

"""
命名めちゃくちゃでごめなさい；；
参考: 
- https://lp-tech.net/articles/nCvfb
- https://www.kaggle.com/parulpandey/overview-of-popular-image-augmentation-packages
- https://github.com/albumentations-team/albumentations_examples
"""

class Batawa_img ():
  def __init__(self, file):
    self.filename = file
    image = cv2.imread(self.filename)
    self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  def visualize(self):
    plt.figure(figsize=(20, 10))
    plt.axis('off')
    plt.imshow(self.image)


  def trans_rain(self, seed=7, brightness_coefficient=0.8, drop_width=1, blur_value=3, p=1):
    transform = A.Compose(
      [A.RandomRain(brightness_coefficient=brightness_coefficient, drop_width=drop_width, blur_value=blur_value, p=p)],
    )
    random.seed(seed)
    transformed = transform(image=self.image)
    # visualize(transformed['image'])
    return transformed['image']

  def trans_snow(self, seed=7, brightness_coeff=2, snow_point_lower=0.5, snow_point_upper=0.5, p=1):
    transform = A.Compose(
        [A.RandomSnow(brightness_coeff=brightness_coeff, snow_point_lower=snow_point_lower, snow_point_upper=snow_point_upper, p=p)],
    )
    random.seed(seed)
    transformed = transform(image=self.image)
    #visualize(transformed['image'])
    return transformed['image']
    

  def trans_sunflare(self, seed=7, flare_roi=(0, 0, 1, 0.1), angle_lower=0.3, p=1):
    transform = A.Compose(
    [A.RandomSunFlare(flare_roi=flare_roi, angle_lower=angle_lower, p=p)],
    )
    random.seed(seed)
    transformed = transform(image=self.image)
    #visualize(transformed['image'])
    return transformed['image']


  def cha_drop(self):
    transform = A.Compose(
    [A.ChannelDropout(channel_drop_range=(1, 1), fill_value=0, p=1)],
    )
    random.seed(7)

    transformed = transform(image=self.image)
        #visualize(transformed['image'])
    tmp = transformed['image']

    return tmp


  def cha_shufful(self):
    transform = A.Compose(
        [A.ChannelShuffle(p=1)],
        )
    random.seed(7)

    transformed = transform(image=self.image)
        #visualize(transformed['image'])
    tmp = transformed['image']

    return tmp

  def to_compression(self):
    transform = A.Compose(
        [A.JpegCompression(quality_lower=5, quality_upper=6, p=1)],
        )
    random.seed(7)
    transformed = transform(image=self.image)

        #visualize(transformed['image'])
    tmp = transformed['image']

    return tmp

  
  def invert_img(self):
    transform = A.Compose(
    [A.InvertImg(p=1)],
    )
    random.seed(7)

    transformed = transform(image=self.image)
        #visualize(transformed['image'])
    tmp = transformed['image']

    return tmp

  
  def add_blur(self):
    transform = A.Compose(
    [A.Blur(blur_limit=(8, 8), p=1)],
    )
    random.seed(7)

    transformed = transform(image=self.image)
        #visualize(transformed['image'])
    tmp = transformed['image']

    return tmp

  def to_grey(self):
    transform = A.Compose(
    [A.ToGray(p=1)],
    )
    random.seed(7)

    transformed = transform(image=self.image)
        #visualize(transformed['image'])
    tmp = transformed['image']

    return tmp
      

  def toCLAHE(self):
    hist,bins = np.histogram(self.image.flatten(),256,[0,256])

    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()

    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')

    img2 = cdf[self.image]

    return img2

  def add_noise(self):
    img = self.image
    row,col,ch = img.shape

    # 白
    pts_x = np.random.randint(0, col-1 , 1000) #0から(col-1)までの乱数を千個作る
    pts_y = np.random.randint(0, row-1 , 1000)
    img[(pts_y,pts_x)] = (255,255,255) #y,xの順番になることに注意

    # 黒
    pts_x = np.random.randint(0, col-1 , 1000)
    pts_y = np.random.randint(0, row-1 , 1000)
    img[(pts_y,pts_x)] = (0,0,0)

    return img


files = os.listdir(img_dir)
aug_dir = "aug_imgsv1"

def img_save(img, path, name, ctgr):
  tmp = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
  cv2.imwrite(f"{path}/{ctgr}{name}", tmp)

for i in range(len(files)):
  filename = f"{img_dir}/{files[i]}"
  org_image = Batawa_img(filename)

  #img_save(org_image.to_grey(), aug_dir, name=files[i], ctgr="grey")
  #img_save(org_image.cha_drop(), aug_dir, name=files[i], ctgr="chadrop")
  #img_save(org_image.cha_shufful(), aug_dir, name=files[i], ctgr="chashuffle")
  #img_save(org_image.invert_img(), aug_dir, name=files[i], ctgr="invert")
  img_save(org_image.to_compression(), aug_dir, name=files[i], ctgr="compre")
  img_save(org_image.toCLAHE(), aug_dir, name=files[i], ctgr="clahe")
  img_save(org_image.trans_rain(), aug_dir, name=files[i], ctgr="rain")
  img_save(org_image.trans_snow(), aug_dir, name=files[i], ctgr="snow")
  img_save(org_image.trans_sunflare(), aug_dir, name=files[i], ctgr="sun")
  img_save(org_image.add_blur(), aug_dir, name=files[i], ctgr="blur")
  img_save(org_image.add_noise(), aug_dir, name=files[i], ctgr="noise")

# files = os.listdir(aug_dir)

# len(files)

# # >> 660