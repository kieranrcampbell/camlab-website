import tifffile
from PIL import Image
import cv2


import numpy as np
import pandas as pd
import torch

import scanpy as sc
from anndata import AnnData

import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize
from skimage import segmentation, morphology

from skimage import data, util
from skimage.measure import label, regionprops
from skimage.morphology import erosion, dilation, flood, flood_fill

from skimage.segmentation import expand_labels, find_boundaries, mark_boundaries


import scipy.ndimage as ndimage
from scipy.ndimage import shift, rotate, zoom
import Augmentor
import albumentations as A

from scipy.stats import pearsonr
import random

from sklearn.cluster import KMeans
from umap import UMAP

from Functions import *

def shift_transform(binary_mask, index):
    
    direction = np.random.randint(0, 4)
    if direction == 0:  # Up
        shifted_index = (index[0] - 1, index[1])
    elif direction == 1:  # Down
        shifted_index = (index[0] + 1, index[1])
    elif direction == 2:  # Left
        shifted_index = (index[0], index[1] - 1)
    elif direction == 3:  # Right
        shifted_index = (index[0], index[1] + 1)

    shifted_mask = np.zeros_like(binary_mask)
    shifted_mask[shifted_index] = 1
    return shifted_mask

def expand_transform(binary_mask):
    # Expand transformation
    outer_boundary = find_boundaries(binary_mask, mode='outer', connectivity=1)
    expand_index = np.where(outer_boundary)
    trans_mask = binary_mask.copy()
    trans_mask[expand_index] = 1
    return trans_mask


def merge_transform(neighbor_lst, mask, tmp_mask):
    # initialize the merged mask (expand the original cell mask)
    tmp_merged_mask = tmp_mask.copy()
    tmp_merged_mask = expand_cell(tmp_merged_mask)

    # Randomly choose a neighbor
    if len(neighbor_lst) > 0:
        chosen_neighbor = np.random.choice(neighbor_lst)

    tmp_neighbor_mask = np.zeros_like(mask) # temporary mask with same shape as mask
    tmp_neighbor_mask[mask == chosen_neighbor] = 1 
    tmp_expanded_neighbor_mask = expand_cell(tmp_neighbor_mask) # expand the neighbor cell    

    tmp_merged_mask[tmp_expanded_neighbor_mask == 1] = 1 # merge the expanded neighbor cell with the original cell

    merged_index = np.where(tmp_merged_mask == 1)
    merged_xs = np.unique(merged_index[0])
    merged_ys = np.unique(merged_index[1])

    return tmp_merged_mask

def rotation_transform(binary_mask, cropped_mask, bbox_min_row, bbox_max_row, bbox_min_col, bbox_max_col, max_boundary):
    angle = random.randint(-15, 15)
    rotated = ndimage.rotate(cropped_mask, angle)
    rotated = extract_center_square(rotated, max_boundary)
    trans_mask = binary_mask.copy()
    trans_mask[bbox_min_row:bbox_max_row, bbox_min_col:bbox_max_col] = rotated    
    return trans_mask

def shrink_transform(binary_mask):
    inner_boundary = find_boundaries(binary_mask, mode='inner', connectivity=1)
    inner_boundary_index = np.where(inner_boundary)
    trans_mask = binary_mask.copy()
    trans_mask[inner_boundary_index] = 0
    return trans_mask
