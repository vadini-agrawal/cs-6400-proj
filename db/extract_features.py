import os
from glob import glob
import pickle
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm

import torch
from torchvision.models.feature_extraction import get_graph_node_names
from torchvision.models.feature_extraction import create_feature_extractor
from torchvision import datasets, models, transforms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dataroot = "../data/hico_20160224_det/images/train2015"
imglist = open("images_list.txt").read().split('\n')[:-1]

def read_image(imgpath):
    img = Image.open(imgpath).convert('RGB')
    img = transform(img)
    img = img[None,...]
    return img.to(device)


imglist = list(map(lambda x: os.path.join(dataroot, x), imglist))
# imglist = glob(dataroot+"/*")
dump_path = "../dump_gitignore"
if not os.path.exists(dump_path):
    os.makedirs(dump_path)

transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


model = models.efficientnet_b1(pretrained=True)
model.eval()
model_extract = create_feature_extractor(model, return_nodes={'flatten':'flatten'})

features_dict = {}
model_extract.eval()
for img in tqdm(imglist):
    with torch.no_grad():
        features = model_extract(read_image(img))
        feat = features['flatten'].squeeze().detach().cpu().numpy()
        features_dict[img] = feat

pickle.dump(features_dict, open(os.path.join(dump_path, "features.pickle"), 'wb'))