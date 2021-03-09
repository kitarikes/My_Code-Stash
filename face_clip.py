import cv2
import os

def face_cascade(img_path, save_cascade_image_dir, name):
    # 画像を読み込む
    img = cv2.imread(img_path)

    # カスケード分類器を生成 -&gt; 今回はアニメ画像の正面の顔を検出
    cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml') # DL for http://anime.udp.jp/data/lbpcascade_animeface.xml

    # 保存先ディレクトリ作成
    os.makedirs(save_cascade_image_dir, exist_ok=True)
    # 顔を検出する
    facerect = cascade.detectMultiScale(img)

    # 検出した顔を四角い枠線で囲む(検出した顔の数だけ繰り返す)
    for rect in facerect:
        cv2.rectangle(img, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)

    # 画像を保存する
    cv2.imwrite('{}/cascade_image_{}.jpg'.format(save_cascade_image_dir, name), img)

ORIGINAL_IMG_PATH = "cv-imgdata" # 参照元ディレクトリ
SAVE_CASCADE_FOLDER = 'hozonsaki2' # 保存先のディレクトリ

img_li = os.listdir(ORIGINAL_IMG_PATH)

for img in img_li:
  face_cascade("{}/{}".format(ORIGINAL_IMG_PATH, img), SAVE_CASCADE_FOLDER, str(img))
