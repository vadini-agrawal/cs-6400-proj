import os
from glob import glob
import pickle
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
import pdb

import torch
from torchvision.models.feature_extraction import create_feature_extractor
from torchvision import models, transforms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dataroot = "static/data/hico_20160224_det/images/train2015"
dump_path = "dump"

def load_features(feature_path="features_10k.pickle"):
    features_dict = pickle.load(open(os.path.join(feature_path), 'rb'))
    imlist = []
    feat_size = 1280
    featnp = np.zeros((len(features_dict), feat_size))
    for i, img in enumerate(features_dict):
        imlist.append(os.path.join(dataroot, img.split('/')[-1]))
        featnp[i,:] = features_dict[img]
    feat_normed = featnp/np.linalg.norm(featnp, axis=1)[:,None]
    imlist = np.array(imlist)
    return feat_normed, imlist


def read_image(imgpath):
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(imgpath).convert('RGB')
    img = transform(img)
    img = img[None,...]
    return img.to(device)


def extract_feature(img):
    model = models.efficientnet_b1(pretrained=True)
    model.eval()
    model_extract = create_feature_extractor(model, return_nodes={'flatten':'flatten'})

    with torch.no_grad():
        features = model_extract(read_image(img))
        feat = features['flatten'].squeeze().detach().cpu().numpy()
    
    return feat

def compute_closest(feat_normed, imlist, feat, topk=5):
    feat = feat/np.linalg.norm(feat)
    cosine = feat[None,:] @ feat_normed.T
    cosine_dist = 100*(1-cosine.squeeze())
    args = np.argsort(cosine_dist)[1:1+topk]
    return imlist[args]


def get_similar_images(filename):
    feat_normed, imlist = load_features()
    feat = extract_feature(filename)
    close_images = compute_closest(feat_normed, imlist, feat, topk=10)
    return close_images
        

