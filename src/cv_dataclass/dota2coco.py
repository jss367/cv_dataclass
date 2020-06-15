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
from src.cv_dataclass.bounding_box import BoundingBox
import json
import os
from pathlib import Path
from typing import List, Union

import cv2

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
    objects = []
    with open(filename, 'r') as f:
        for _, line in enumerate(f):
            splitlines = line.strip().split(' ')
            if len(splitlines) == 1:
                print("we got a metadata")
                continue
            elif len(splitlines) < 9:
                raise InputDataException("Not enough input data fields")
                continue
            category = None
            if len(splitlines) >= 9:
                category = splitlines[8]
            bbox = BoundingBox.read_dota_data([
                (float(splitlines[0]), float(splitlines[1])),
                (float(splitlines[2]), float(splitlines[3])),
                (float(splitlines[4]), float(splitlines[5])),
                (float(splitlines[6]), float(splitlines[7])),
            ], category)
            bbox.difficult = '0' if len(splitlines) == 9 else splitlines[9]
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


def DOTA2COCO(label_path: PathOrStr, image_paths: List[PathOrStr], dest_folder: PathOrStr, dest_filename: PathOrStr):

    # Convert all to pathlib Paths
    label_path = Path(label_path)
    image_paths = [Path(p) for p in image_paths]
    dest_folder = Path(dest_folder)

    os.makedirs(dest_folder, exist_ok=True)

    # go through images and get the label
    all_labels = get_files(label_path)

    all_images = []
    for path in image_paths:
        all_images.extend(get_files(path))

    assert len(all_labels) == len(
        all_images), f"Should have equal labels and images, but have {len(all_labels)} labels and {len(all_images)} images"

    data_dict = {}
    data_dict['images'] = []
    data_dict['categories'] = []
    data_dict['annotations'] = []
    for idex, name in enumerate(dota_category_dict):
        single_cat = {'id': idex + 1, 'name': name, 'supercategory': name}
        data_dict['categories'].append(single_cat)

    inst_count = 1
    image_id = 1

    for my_file in all_images[:10]:

        data_dict['images'].append(create_image_item(my_file, image_id))
        label_file = label_path / (my_file.stem + '.txt')

        objects = parse_label_file(label_file)
        for obj in objects:
            single_obj = {}
            single_obj['area'] = obj.area
            single_obj['category_id'] = dota_category_dict[obj.category]
            single_obj['segmentation'] = obj.to_coords()
            single_obj['iscrowd'] = 0
            single_obj['bbox'] = obj.to_coco()
            single_obj['image_id'] = image_id
            data_dict['annotations'].append(single_obj)
            single_obj['id'] = inst_count
            inst_count = inst_count + 1
        image_id = image_id + 1

    output_json = dest_folder / dest_filename
    with open(output_json, 'w') as f_out:
        json.dump(data_dict, f_out)


if __name__ == "__main__":

    train_label_path = 'E:\\Data\\Raw\\DOTA\\train\\labelTxt\\DOTA-v1.5_train'
    train_image_paths = [
        'E:\\Data\\Raw\\DOTA\\train\\images\\part1\\images',
        'E:\\Data\\Raw\\DOTA\\train\\images\\part2\\images',
        'E:\\Data\\Raw\\DOTA\\train\\images\\part3\\images']
    # note i'm using horizontal labels now
    val_label_path = r'E:\Data\Raw\DOTA\val\labelTxt-v1.5\DOTA-v1.5_val_hbb'
    val_image_paths = [r'E:\Data\Raw\DOTA\val\part1\images']
    val_filename = 'dota2coco_val.json'
    dest_folder = 'E:\\Data\\Processed\\DOTACOCO'

    #DOTA2COCO(label_path, image_paths, dest_folder, dest_filename)
    DOTA2COCO(val_label_path, val_image_paths, dest_folder, val_filename)
