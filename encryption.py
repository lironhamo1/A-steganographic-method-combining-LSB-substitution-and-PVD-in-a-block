from PIL import Image
import numpy as np
import cv2
import os
import time


def abs(x):
    if x >= 0:
        return x
    return -1 * x


def get_range(value):
    if value in range(8):
        return 0
    elif value in range(8, 16):
        return 8
    elif value in range(16, 32):
        return 16
    elif value in range(32, 64):
        return 32
    elif value in range(64, 128):
        return 64
    elif value in range(128, 255):
        return 128
    else:
        return 0


def embedding(carrier_pixel_block, cover_pixel, k=3):
    gx = carrier_pixel_block[0][0]
    gur = carrier_pixel_block[0][1]
    gbl = carrier_pixel_block[1][0]
    gbr = carrier_pixel_block[1][1]
    cv = cover_pixel

    bin_gx = list(format(gx, '08b'))
    bin_gur = list(format(gur, '08b'))
    bin_gbl = list(format(gbl, '08b'))
    bin_gbr = list(format(gbr, '08b'))
    bin_cv = list(format(cv, '08b'))

    L = int(format(gx, '08b')[-k:])

    bin_gx[-1] = bin_cv[0]
    bin_gx[-2] = bin_cv[1]

    new_gx = ''.join(bin_gx)

    S = int(new_gx[-k:])

    new_gx = int(new_gx, 2)

    d = L - S

    if d > pow(2, k - 1) and 0 <= new_gx + pow(2, k) and new_gx + pow(2, k) <= 255:
        new_gx = new_gx + pow(2, k)
    elif d < -pow(2, k - 1) and 0 <= new_gx - pow(2, k) and new_gx - pow(2, k) <= 255:
        new_gx = new_gx - pow(2, k)
    else:
        new_gx = new_gx

    d1 = abs(new_gx - gur)
    d2 = abs(new_gx - gbr)
    d3 = abs(new_gx - gbl)

    l1 = get_range(d1)
    l2 = get_range(d2)
    l3 = get_range(d3)

    t1 = 3
    t2 = 3
    t3 = 2

    s1 = int(''.join(bin_cv[:t1]), 2)
    s2 = int(''.join(bin_cv[t1:t1 + t2]), 2)
    s3 = int(''.join(bin_cv[t1 + t2:t1 + t2 + t3]), 2)

    d1_new = l1 + s1
    d2_new = l2 + s2
    d3_new = l3 + s3

    new2gur = new_gx - d1_new
    new3gur = new_gx + d1_new
    new2gbr = new_gx - d2_new
    new3gbr = new_gx + d2_new
    new2gbl = new_gx - d3_new
    new3gbl = new_gx + d3_new

    # To obtain the optimized value for each block
    if abs(gur - new2gur) < abs(gur - new3gur) and 0 <= new2gur and new2gur <= 255:
        new_gur = new2gur
    else:
        new_gur = new3gur

    if abs(gbr - new2gbr) < abs(gbr - new3gbr) and 0 <= new2gbr and new2gbr <= 255:
        new_gbr = new2gbr
    else:
        new_gbr = new3gbr

    if abs(gbl - new2gbl) < abs(gbl - new3gbl) and 0 <= new2gbl and new2gbl <= 255:
        new_gbl = new2gbl
    else:
        new_gbl = new3gbl

    stego_pixel_block = [[new_gx, new_gur], [new_gbl, new_gbr]]
    return stego_pixel_block


def convert_to_binary(data):
    data_binary = ' '.join(format(ord(x), '08b') for x in data)
    return data_binary


def splitValues(num):
    return num // 100, num % 100


