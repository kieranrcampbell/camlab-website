# Importing packages

import tifffile

import numpy as np
import random
import anndata as ad

from Functions import *
from Transformations import *

def generate_aug(imc_tiff, mask_tiff, prob, num_to_gen):

    imc_image = tifffile.imread(imc_tiff) # read IMC image
    mask = tifffile.imread(mask_tiff) # read mask

    # Initializations and import Data (Images)
    exp_matrix = np.zeros((1, imc_image.shape[0])) # Initialize the expression matrix
    aug_exp_matrix = np.zeros((1, imc_image.shape[0])) # Initialize the augmented expression matrix

    imc_array = np.array(imc_image)

    cell_to_neighbor = {}
    neighbor_num = []

    edge_cells = []
    non_edge_cells = []
    proportion_overlap = []
    cell_size = []

    cell_id_lst = []
    aug_type_lst = []
    error_cell = []

    # Look at all the cells to see which one is the biggest (horizontal, vertical) to set boundary box size
    max_x = 0
    max_y = 0
    max_x_lab = 0
    max_y_lab = 0

    for lab in np.unique(mask)[1:]:
        tmp_mask = np.zeros_like(mask)
        tmp_mask[mask == lab] = 1
        
        index = np.where(tmp_mask == 1)

        xs = np.unique(index[0])
        ys = np.unique(index[1])
        
        if len(xs) > max_x:
            max_x = len(xs)
            max_x_lab = lab
        if len(ys) > max_y:
            max_y = len(ys)
            max_y_lab = lab
        
        #print(xs)
        #print(ys)

    print("Max boundary of x is: " + str(max_x) + " of cell " + str(max_x_lab))
    print("Max boundary of y is: " + str(max_y) + " of cell " + str(max_y_lab))

    max_boundary = max(max_x, max_y)

    if max_boundary % 2 == 1:
        max_boundary = max_boundary + 1

    print("The boundary box will be: " + str(max_boundary) + "x" + str(max_boundary))

    select_cells = np.random.choice(np.unique(mask)[1:], num_to_gen)


    for lab in select_cells: # iterates over unique non-zero labels found in mask - exlcude 0 (background)
        tmp_mask = np.zeros_like(mask) # temporary mask with same shape as mask
        tmp_mask[mask == lab] = 1 # pixels in mask that has the current label are set to 1 in temp_msk, else 0
        tmp_merged_mask = tmp_mask.copy()
        
        # store cell size
        cellsize = np.count_nonzero(tmp_mask)
        cell_size.append(cellsize)
        
        # extracting indices of labelled region
        index, xs, ys = extract_indices(tmp_mask)
        
        # Compute original cell expression
        row_array = compute_cell_expression(imc_array, index)
        exp_matrix = np.concatenate((exp_matrix, row_array), axis=0)

        # Create Boundary Box
        bbox_min_row, bbox_max_row, bbox_min_col, bbox_max_col = make_boundary_box(tmp_mask, xs, ys, max_boundary)
        cropped_mask = tmp_mask[bbox_min_row:bbox_max_row, bbox_min_col:bbox_max_col].copy() # boundary box

        # Preparation for merging augmentations
        final_boundary = find_boundaries_including_gap(tmp_mask, index, xs, ys) # boundaries
        cell_to_neighbor, neighbor_lst = store_neighbor(mask, final_boundary, cell_to_neighbor, lab, neighbor_num)
        
        choose_trans = np.random.choice(5, 1, p=prob)

        try:
            if choose_trans == 0:
                    trans_mask = shift_transform(tmp_mask, index)
                    aug_index = np.where(trans_mask == 1)
                    aug_row_array = compute_cell_expression(imc_array, aug_index)
                    aug_exp_matrix = np.concatenate((aug_exp_matrix, aug_row_array), axis=0)
                    aug_type = "Shift"

            if choose_trans == 1:
                    trans_mask = rotation_transform(tmp_mask, cropped_mask, bbox_min_row, bbox_max_row, bbox_min_col, bbox_max_col, max_boundary)
                    aug_index = np.where(trans_mask == 1)
                    aug_row_array = compute_cell_expression(imc_array, aug_index)
                    aug_exp_matrix = np.concatenate((aug_exp_matrix, aug_row_array), axis=0)
                    aug_type = "Rotation"

            if choose_trans == 2:
                    trans_mask = merge_transform(neighbor_lst, mask, tmp_mask)
                    aug_index = np.where(trans_mask == 1)
                    aug_row_array = compute_cell_expression(imc_array, aug_index)
                    aug_exp_matrix = np.concatenate((aug_exp_matrix, aug_row_array), axis=0)
                    aug_type = "Merge"

            if choose_trans == 3:
                    trans_mask = expand_transform(tmp_mask)
                    aug_index = np.where(trans_mask == 1)
                    aug_row_array = compute_cell_expression(imc_array, aug_index)
                    aug_exp_matrix = np.concatenate((aug_exp_matrix, aug_row_array), axis=0)
                    aug_type = "Expand"

            if choose_trans == 4:
                    trans_mask = shrink_transform(tmp_mask)
                    aug_index = np.where(trans_mask == 1)
                    aug_row_array = compute_cell_expression(imc_array, aug_index)
                    aug_exp_matrix = np.concatenate((aug_exp_matrix, aug_row_array), axis=0)
                    aug_type = "Shrink"

            new_adata = ad.AnnData(aug_row_array)

            cell_id_lst.append(lab)
            aug_type_lst.append(aug_type)

        except Exception as e:
            error_cell.append(lab)
            print("An error occurred when applying Aug " + aug_type + " " + str(lab))
            continue


    exp_matrix = exp_matrix[1:]
    aug_exp_matrix = aug_exp_matrix[1:]

    # concatenate original expression matrix and augmented expression matrix
    combined_exp_matrix = np.vstack((exp_matrix, aug_exp_matrix))
    adata = ad.AnnData(combined_exp_matrix)
    select_cells = select_cells.tolist()
    cell_id_lst = select_cells + cell_id_lst

    adata.obs_names = [f"Cell_{i:d}" for i in cell_id_lst]
    adata.var_names = [f"Channel_{i:d}" for i in range(adata.n_vars)]

    original_labels = np.array(['original'] * exp_matrix.shape[0])
    aug_labels = np.array(aug_type_lst)

    adata.obs["Aug_type"] = np.concatenate((original_labels, aug_labels))

    print(adata.obs)
    print(adata.X.shape)
    print(error_cell)

    return adata


