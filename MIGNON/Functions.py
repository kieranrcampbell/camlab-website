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

def calculate_euclidean_distance(expression1, expression2):
    squared_diff = np.square(expression1 - expression2)
    euclidean_distance = np.sqrt(np.sum(squared_diff))
    return euclidean_distance

def extract_indices(binary_mask):
    index = np.where(binary_mask == 1)
    xs = np.unique(index[0])
    ys = np.unique(index[1])
    return index, xs, ys

def compute_cell_expression(imc_array, index):
    lst_expression = []
    # For each channel
    for i in range(imc_array.shape[0]):
        # Interested pixel values based on the labelled cell
        values_of_interest = imc_array[i][index]

        # Compute Cell Expression for each marker by taking the average of the pixel values of the interested cell
        average = np.mean(values_of_interest)

        # Append to the expression list
        lst_expression.append(average)
    row_array = np.array(lst_expression).reshape(1, -1) # Reshape to a row array
    return row_array

def expand_cell(binary_mask):
    outer_boundary = find_boundaries(binary_mask, mode='outer', connectivity=1)
    expand_index = np.where(outer_boundary)
    trans_mask = binary_mask.copy()
    trans_mask[expand_index] = 1
    return trans_mask

def find_boundaries_including_gap(binary_mask, binary_mask_index,xs,ys):
    # Find outer boundary that touches the cell
    first_boundary = find_boundaries(binary_mask, mode='outer',connectivity=1).astype(int)
    
    # temporarily assign 1s of the original mask to find further boundary
    first_boundary[binary_mask_index] = 1

    # Find second outer boundary (1 pixel away from the original masked cell)
    second_boundary = find_boundaries(first_boundary, mode='outer',connectivity=1)

    # Change first_boundary back by removing masked cell 1s
    first_boundary[binary_mask_index] = 0

    # Combine the two boundaries
    first_boundary_index = np.where(first_boundary)
    final_boundary = second_boundary.copy()
    final_boundary[first_boundary_index] = 1

    return final_boundary

def store_neighbor(mask, boundary, cell_neighbor_dict, label, neighbor_num_lst):
    has_neighbor = sum(mask[boundary] > 0) > 0
    neighbor_number = sum(np.unique(mask[boundary]) > 0)
    neighbor_num_lst.append(neighbor_number)

    # remove zero (background) as neighbor:
    neighbor_lst = np.unique(mask[boundary]).copy()
    
    if 0 in neighbor_lst:
        neighbor_lst = np.delete(neighbor_lst, np.where(neighbor_lst == 0))
    
    cell_neighbor_dict[label] = neighbor_lst
    return cell_neighbor_dict, neighbor_lst


def make_boundary_box(tmp_mask, xs, ys, max_boundary):
    # Find the coordinates of the bounding box that encloses all the ones
    min_row, min_col = xs[0], ys[0]
    max_row, max_col = xs[-1], ys[-1]

    # Calculate the center of the bounding box
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    # Calculate the coordinates for the boundary box
    half_size = max_boundary //2  # Half of the boundary box size (max_boundary // 2)
    bbox_min_row = center_row - half_size
    bbox_max_row = center_row + half_size
    bbox_min_col = center_col - half_size
    bbox_max_col = center_col + half_size

    # Ensure the boundary box does not exceed the matrix dimensions
    bbox_min_row = max(0, bbox_min_row)
    bbox_max_row = min(tmp_mask.shape[0] - 1, bbox_max_row)
    bbox_min_col = max(0, bbox_min_col)
    bbox_max_col = min(tmp_mask.shape[1] - 1, bbox_max_col)

    return bbox_min_row, bbox_max_row, bbox_min_col, bbox_max_col


def find_overlap_area(binary_mask, trans_binary_mask):
    # find overlap area
    # Find non-zero positions in original mask
    num_ones_mask = np.count_nonzero(binary_mask)
    # Find non-zero positions in augmented mask
    num_ones_trans = np.count_nonzero(trans_binary_mask)

    intersection = np.logical_and(binary_mask, trans_binary_mask)
    num_ones_intersection = np.count_nonzero(intersection)

    overlap_proportion = num_ones_intersection / num_ones_mask

    return overlap_proportion


def extract_center_square(image, max_boundary):
    # Get the dimensions of the original image
    height, width = image.shape

    # Calculate the coordinates to extract the center square
    left = (width - max_boundary) // 2
    top = (height - max_boundary) // 2
    right = left + max_boundary
    bottom = top + max_boundary

    # Crop the center square
    center_square = image[top:bottom, left:right]
    return center_square

