"""
This includes the categories added in version 1.5

TODO: What should image_data['id'] be?
TODO: Should number be forced to ints? If so, when?

http://cocodataset.org/#format-data

COCO consists of an overall datadict, which contains an info dict, images dicts,
annotation dicts, and a license dict


This file dumps a datadict, which contains everything

"""
#from cv_dataclass.bounding_box import BoundingBox
from cv_dataclass.bounding_box import BoundingBox
import json
import os
from pathlib import Path
from typing import List, Union
from collections import Counter
from matplotlib import pyplot as plt
import cv2
import pickle

PathOrStr = Union[Path, str]

# https://captain-whu.github.io/DOAI2019/dataset.html
dota_category_dict = {
    'plane': 1,
    'ship': 2,
    'storage-tank': 2,
    'baseball-diamond': 3,
    'tennis-court': 4,
    'basketball-court': 5,
    'ground-track-field': 6,
    'harbor': 7,
    'bridge': 8,
    'small-vehicle': 9,
    'large-vehicle': 10,
    'helicopter': 11,
    'roundabout': 12,
    'soccer-ball-field': 13,
    'swimming-pool': 14,
    'container-crane': 15}


class InputDataException(Exception):
    pass


def parse_label_file(filename: Path):
    """
    parse through the DOTA label files
    """
    with open(filename, 'r') as f:
        #source = ''
        #gsd = ''
        objects = []
        for _, line in enumerate(f):
            splitlines = line.strip().split(' ')
            category = None
            if len(splitlines) < 8:
                continue
            if len(splitlines) >= 9:
                category = splitlines[8]

            bbox = BoundingBox.read_dota_data([
                (float(splitlines[0]), float(splitlines[1])),
                (float(splitlines[2]), float(splitlines[3])),
                (float(splitlines[4]), float(splitlines[5])),
                (float(splitlines[6]), float(splitlines[7])),
            ], category)
            #bbox.difficult = '0' if len(splitlines) == 9 else splitlines[9]
            objects.append(bbox)
    return objects


def get_files(my_dir: Path):
    files_and_folders = my_dir.glob('**/*')
    files = [f for f in files_and_folders if f.is_file()]
    return files


def create_image_item(im_path: Path, image_id: int):
    im = cv2.imread(str(im_path))
    height, width, channels = im.shape
    image_data = {}
    image_data['file_name'] = im_path.name
    image_data['height'] = height
    image_data['width'] = width
    image_data['id'] = image_id
    return image_data


def DOTA2COCO(label_path: PathOrStr,):

    # Convert all to pathlib Paths
    label_path = Path(label_path)

    # go through images and get the label
    all_labels = get_files(label_path)
    #i = 0
    all_objects = []
    for label in all_labels:
        objects = parse_label_file(label)
        all_objects.append(objects)

    with open('objects.pkl', 'wb') as f:
        pickle.dump(all_objects, f)


if __name__ == "__main__":

    train_label_path = 'E:\\Data\\Raw\\DOTA\\train\\labelTxt\\DOTA-v1.5_train'
    train_filename = 'dota2coco_train.json'
    # note i'm using horizontal labels now
    val_label_path = r'E:\Data\Raw\DOTA\val\labelTxt-v1.5\DOTA-v1.5_val_hbb'
    val_filename = 'dota2coco_val.json'
    dest_folder = 'E:\\Data\\Processed\\DOTACOCO'

    #DOTA2COCO(
    #    train_label_path,
    #    train_image_paths,
    #    dest_folder,
    #    train_filename)
    DOTA2COCO(val_label_path)
