import os

splits = ['train', 'test']

images_ct = 0
tracklets_ct = 0




for split in splits:
    base_path = f"D:/soccernet_jersey/jersey-2023/{split}/images"
    tracklets = os.listdir(base_path)
    tracklets_ct += len(tracklets)
    for tr in tracklets:
        tr_path = f"{base_path}/{tr}"
        tr_images = os.listdir(tr_path)
        images_ct += len(tr_images)








