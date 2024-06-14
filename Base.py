import numpy as np
import cv2

"""
画像の濃淡をはっきりさせて、ピアノの鍵盤の位置をわかりやすくするプログラム
(sampling_Imageを)
"""

EvaluationNumber = 100 #defoは90 数字が大きいほど黒い部分が増える

# 画像の読み込み
image = cv2.imread('saved_image0.jpg')

height, width, channels = image.shape
for w in range(0,width):
    for h in range(0,height):
        if image[h,w][0] > EvaluationNumber:
            image[h,w] = [255,255,255]
        else:
            image[h,w] = [0,0,0]

# 変更した画像を保存
cv2.imwrite('sampling_Image.jpg', image)
