"""
This includes the categories added in version 1.5

TODO: What should image_data['id'] be?
TODO: Should number be forced to ints? If so, when?

http://cocodataset.org/#format-data

COCO consists of an overall datadict, which contains an info dict, images dicts,
annotation dicts, and a license dict

This file dumps a datadict, which contains everything
"""
import os
import pickle
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
    with open(filename, 'r') as f:
        source = ''
        gsd = ''
        #i = 0
        for _, line in enumerate(f):
            splitlines = line.strip().split(' ')
            if len(splitlines) == 1:
                if 'imagesource' in line:
                    _, source = splitlines[0].split(':')
                elif 'gsd' in line:
                    _, gsd = splitlines[0].split(':')
                else:
                    print("unknown metadata field")
                if source and gsd:
                    return source, gsd
                continue
            #elif len(splitlines) < 9:
            #    raise InputDataException("Not enough input data fields")
            #    continue
    return source, gsd


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


def DOTA2COCO(
        label_path: PathOrStr,
        image_paths: List[PathOrStr],
        dest_folder: PathOrStr):

    # Convert all to pathlib Paths
    label_path = Path(label_path)
    dest_folder = Path(dest_folder)

    os.makedirs(dest_folder, exist_ok=True)

    # go through images and get the label
    all_labels = get_files(label_path)
    #i = 0
    null_gsd_sources = []
    for label in all_labels:
        all_sources = []
        all_gsds = []
        for my_file in all_labels:

            sources, gsds = parse_label_file(my_file)
            all_sources.append(sources)
            if gsds == 'null':
                null_gsd_sources.append(sources)
            else:
                all_gsds.append(float(gsds))

    #print(all_sources)
    #c = Counter(all_sources)
    #print(c)

    #print(all_gsds)
    with open(dest_folder / 'sources.pkl', 'wb') as f:
        pickle.dump(all_sources, f)

    with open(dest_folder / 'gsd.pkl', 'wb') as f:
        pickle.dump(all_gsds, f)



if __name__ == "__main__":



    #plot_histo(mynewlist)

    train_label_path = 'E:\\Data\\Raw\\DOTA\\train\\labelTxt\\DOTA-v1.5_train'
    train_image_paths = [
        'E:\\Data\\Raw\\DOTA\\train\\images\\part1\\images',
        'E:\\Data\\Raw\\DOTA\\train\\images\\part2\\images',
        'E:\\Data\\Raw\\DOTA\\train\\images\\part3\\images']
    train_dest_folder = 'E:\\Data\\Processed\\DOTACOCO\\metadata\\train'
    # note i'm using horizontal labels now
    val_label_path = r'E:\Data\Raw\DOTA\val\labelTxt-v1.5\DOTA-v1.5_val_hbb'
    val_image_paths = [r'E:\Data\Raw\DOTA\val\part1\images']
    val_dest_folder = 'E:\\Data\\Processed\\DOTACOCO\\metadata\\val'

    #DOTA2COCO(
    #    train_label_path,
    #    train_image_paths,
    #    dest_folder,
    #    train_filename)
    DOTA2COCO(train_label_path, train_image_paths, train_dest_folder)
