import json
import re

import cv2
import numpy as np


def concatenate_images_vertically(images):
    if len(set(image.shape[1] for image in images)) != 1:
        raise ValueError("Images must have the same width")
    concatenated_image = np.vstack(images)
    return concatenated_image


def concatenate_images_horizontally(images):
    if len(set(image.shape[0] for image in images)) != 1:
        raise ValueError("Images must have the same height")
    concatenated_image = np.hstack(images)
    return concatenated_image


def show_image(my_image, size=(960, 540)):
    resized_image = cv2.resize(my_image, size)
    cv2.imshow("image", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def read_json(file_path):
    try:
        f = open(file_path)
        data = json.load(f)
        f.close()
    except Exception as e:
        print(e)
        data = []
    return data


def save_json(data, path):
    jsonString = json.dumps(data)
    jsonFile = open(path, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def chunkify(big_list, chunk_size):
    chunks = [big_list[x:x + chunk_size] for x in range(0, len(big_list), chunk_size)]
    return chunks


def read_image_for_annotation(image_path, img_size=(50, 100)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, img_size)
    return image



def extract_number(path):
    match = re.search(r'(\d+)(?=\D*$)', path)
    return int(match.group(0)) if match else float('inf')

