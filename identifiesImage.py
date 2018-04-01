import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

def create_canny_img(img_name):
    """create 3 Mat from a image_file.
    argument:
        img_name (str): image file's name
    return:
        can_img (Mat):Edge detecion by canny
        gau_can_img (Mat): Edge detection by canny after GaussianBlur
        med_can_img (Mat): Edge detection by canny agter MedianBlur
    """
    ave_square = (5, 5)
    # x軸方向の標準偏差
    sigma_x = 1
    gray_img_src = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    can_img = cv2.Canny(gray_img_src, 100, 200)
    
    gau_img = cv2.GaussianBlur(gray_img_src, ave_square, sigma_x)
    gau_can_img = cv2.Canny(gau_img, 100, 200)
    
    med_img = cv2.medianBlur(gray_img_src, ksize=5)
    med_can_img = cv2.Canny(med_img, 100, 200)
    
    return can_img, gau_can_img, med_can_img

def get_color(img_name):
    """
    argument:
        img_name (str): file name
        
    return:
        result (float): maxium value of the most used color 
    """
    img_src = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
    
    same_colors = {}
    for row in img_src:
        for at in row:
            at = tuple(at)
            if at in same_colors:
                same_colors[at] += 1
            else:
                same_colors[at] = 0
    
    result = max(same_colors.values()) / len(img_src)
    print("color_result :",result)
    
    return result
    
def cal_diff(mat, c_mat):
    """
    argument:
        mat (Mat): 
        c_mat: 
        
    return:
        result (float): mat diff
    """
    sum_mat = 0
    for m in mat:
        for n in m:
            sum_mat += n
    sum_mat /= 255
    diff = mat - c_mat
    sum_diff = 0
    for d in diff:
        for n in d:
            sum_diff += n
    sum_diff /= 255
    result = sum_diff / sum_mat
    
    return result

def cal_score(gau_result, med_result, color_result):
    result1 = gau_result + med_result
    print("result1 :", result1)
    return (1 / result1) * 0.8 + (color_result / 100) * 0.2


def identifies_img(img_name):
    can_img, gau_can_img, med_can_img = create_canny_img(img_name)
    gau_result = cal_diff(can_img, gau_can_img)
    med_result = cal_diff(can_img, med_can_img)
    color_result = get_color(img_name)
    score = cal_score(gau_result, med_result, color_result) * 0.625
    print("score :", round(score, 3) ,end=" -->")
    if score > 0.5:
        return "illust"
    else:
        return "picture"

if __name__ == "__main__":
    dir_path = ".\\pictures\\"
    num = 0
    good = 0
    for pic_path in os.listdir(dir_path):
        print("----- ", dir_path, " -----")
        result = identifies_img(dir_path + pic_path)
        print(result)
        if result == "picture":
            good += 1
        num += 1
    print("score :", good / num)


    dir_path = ".\\illusts\\"
    num = 0
    good = 0
    for pic_path in os.listdir(dir_path):
        print("----- ", dir_path, " -----")
        result = identifies_img(dir_path + pic_path)
        print(result)
        if result == "illust":
            good += 1
        num += 1
    print("score :", good / num)
