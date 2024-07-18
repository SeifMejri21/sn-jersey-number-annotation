import os
import re
from pprint import pprint

import cv2

from helpers import chunkify, read_image_for_annotation, concatenate_images_vertically, concatenate_images_horizontally, \
    show_image, extract_number, read_json, save_json

split = 'train'
split = 'test'
fps = 25

images_ct = 0
tracklets_ct = 0
my_base_path = f"D:/soccernet_jersey"
relative_dataset_path = f"/jersey-2023/{split}/images"

tracklets = os.listdir(f"{my_base_path}/{relative_dataset_path}")
tracklets_ct += len(tracklets)

gt_path = f"{my_base_path}/jersey-2023/{split}/{split}_gt.json"

ground_truth = read_json(gt_path)

show_size = (400, 800)
x_position = 1000
y_position = 0
# for key,gt in ground_truth.items():
#     print(key, gt)


annotation_file_path = f'{split}_annotations.json'
annotations = read_json(annotation_file_path)

annotated_info_file_path = f'{split}_annotated_info.json'
annotated_info = read_json(annotated_info_file_path)
if not annotated_info:
    annotated_info = {'annotated': []}

for key, gt in ground_truth.items():
    if key in annotated_info['annotated']:
        print(key, 'already annotated')
    else:
        tr_path = f"{my_base_path}{relative_dataset_path}/{key}"
        tr_images = [f"{tr_path}/{fn}" for fn in os.listdir(tr_path)]
        tr_images = sorted(tr_images, key=extract_number)
        if gt == -1:
            for el in tr_images:
                annotations.append({'relative_image_path': re.sub('D:/soccernet_jersey', '',el), 'class': -1})
            save_json(annotations, annotation_file_path)
            annotated_info['annotated'].append(key)
            save_json(annotated_info, annotated_info_file_path)
        else:
            chunked_tr_images = chunkify(tr_images, chunk_size=fps)
            for ch_dx, chunk in enumerate(chunked_tr_images):
                # print(chunk)
                images = [read_image_for_annotation(img_path) for img_path in chunk]
                chunked_images = chunkify(images, 5)
                chunked_images = [chhh for chhh in chunked_images if len(chhh) == 5]
                rez_image = concatenate_images_vertically([concatenate_images_horizontally(ch) for ch in chunked_images])
                resized_image = cv2.resize(rez_image, show_size)

                window_name = f'{ch_dx + 1}/{len(chunked_tr_images)} from {key} in {split}'
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Create a named window

                cv2.moveWindow(window_name, x_position, y_position)
                cv2.resizeWindow(window_name, 400, 800)
                cv2.imshow(window_name, resized_image)
                button = cv2.waitKeyEx(0)

                if button == 83 or button == 2555904:  # ASCII code for right arrow
                    group_class = gt
                    for el in chunk:
                        annotations.append({'relative_image_path': re.sub('D:/soccernet_jersey', '',el), 'class': group_class})
                    save_json(annotations, annotation_file_path)
                    print(f"{ch_dx + 1}/{len(chunked_tr_images)} from {key} in {split} marked as {group_class}.")
                    cv2.destroyAllWindows()
                elif button == 81 or button == 2424832:  # ASCII code for left arrow
                    group_class = -1
                    for el in chunk:
                        annotations.append({'relative_image_path': re.sub('D:/soccernet_jersey', '',el), 'class': group_class})
                    save_json(annotations, annotation_file_path)
                    print(f"{ch_dx + 1}/{len(chunked_tr_images)} from {key} in {split} marked as {group_class}.")
                    cv2.destroyAllWindows()
                # else:
                #     save_json(annotations, annotation_file_path)
                #     cv2.destroyAllWindows()
            annotated_info['annotated'].append(key)
            save_json(annotated_info, annotated_info_file_path)

            print(f'{key}/{len(ground_truth)}--------------------------------------------------------------------------------------------------------')
            # show_image(rez_image, (400, 800))
