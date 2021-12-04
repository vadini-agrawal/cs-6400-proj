import numpy as np
import json
import os
import pickle
from pprint import pprint as pp
import pdb
from PIL import Image
import random
from tqdm import tqdm
import argparse


my_parser = argparse.ArgumentParser(description='List the content of a folder')
my_parser.add_argument("-n", "--num-images", type=int, default=10000, help='Number of images to add to DB')
# my_parser.add_argument("-c", "--coco-categories", type=str, 
#                         default="../data/hico_20160224_det/coco_categories.pickle", help="Path to coco categories")


hico_verbs_list_path = "../data/hico_20160224_det/hico_list_vb.txt"
tr_anno_fl = "../data/hico_20160224_det/trainval_hico.json"
imgroot = "../data/hico_20160224_det/images/train2015"
coco_categories_path = "../data/hico_20160224_det/coco_categories.pickle"

args = my_parser.parse_args()


num_images = args.num_images


annots = json.load(open(tr_anno_fl, 'r'))
random.seed(0)
random.shuffle(annots)
annots_subset = annots[:num_images]
annots_subset.sort(key=lambda x: x["file_name"])

id_to_name = pickle.load(open(coco_categories_path,'rb'))[1]
lines = open(hico_verbs_list_path,'r').read().split('\n')[2:]
vid_to_verb = {int(l.split()[0]):l.split()[1] for l in lines}

dumproot = "csv_"+str(num_images)
if not os.path.exists(dumproot):
    os.makedirs(dumproot)
    
imgfile = open(os.path.join(dumproot, "IMAGE.csv"), "w")
objfile = open(os.path.join(dumproot,"OBJECT.csv"), "w")
imobfile = open(os.path.join(dumproot, "IMAGE_OBJECT_DETAILS.csv"), "w")

imgfile.write("{},{},{},{}\n".format("image_id","image_path", "img_width", "img_height"))
objfile.write("{},{},{},{},{},{}\n".format("bb_id","x1","y1","x2","y2","class_name" ))
imobfile.write("{},{},{},{}\n".format("human_bb","object_bb","action","img_id"))

bb_id_counter = 0

imgs_list = []
for anno in tqdm(annots_subset):
    imgs_list.append(anno["file_name"])
    img_path = os.path.join(imgroot, anno["file_name"])
    img_id = int(img_path.split('_')[-1].split('.')[0])
    im = Image.open(img_path)
    w, h = im.size
    img_path = img_path.replace("../hico_20160224_det/", "")
    bboxes = anno['annotations']
    bb_ids = list(range(bb_id_counter, bb_id_counter+len(bboxes)))
    bb_id_counter += len(bboxes)

    imgfile.write("{},{},{},{}\n".format(img_id, img_path, w, h))
    for i, bb in enumerate(bboxes):
        x1,y1,x2,y2 = bb["bbox"][0], bb["bbox"][1], bb["bbox"][2], bb["bbox"][3]
        class_name = id_to_name[bb["category_id"]]
        objfile.write("{},{},{},{},{},{}\n".format(bb_ids[i],x1,y1,x2,y2,class_name))

    for hoi in anno['hoi_annotation']:
        action = vid_to_verb[hoi['category_id']]
        human_bb = bb_ids[hoi['subject_id']]
        object_bb = bb_ids[hoi['object_id']]
        imobfile.write("{},{},{},{}\n".format(human_bb, object_bb, action, img_id))

with open("images_list.txt", 'w') as file:
    for flname in imgs_list:
        file.write("{}\n".format(flname))