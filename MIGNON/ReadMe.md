
# MIGNON

MIGNON (Multiplexed Imaging auGmeNtatiONs) is a tool to generate data augmentations of multiplexed images. Given an IMC tiff file and a mask tiff file, augmentations can be generated. Possible augmentations that can be selected are Shift, Rotate, Merge, Expand, and Shrink. Users can select the probability to apply each augmentation and the desired number of augmentations to generate. The output includes original cell expressions and augmented cell expressions.

## Type of Augmentations

### Shift
* Randomly select a direction to shift the mask for one unit.

### Rotate
* Randomly rotate the mask at (-15, 15) degrees.

### Merge
* Randomly select a neighbour cell (a cell that touches the interested cell or has a one-pixel gap is considered a neighbour cell) and merge it with the original cell.
* Note: In order to fill the gaps, the original cell and neighbour cell are expanded before merging.

### Expand
* Expand the mask for one pixel

### Shrink
* Shrink the mask for one pixel

### Output
* The output is an anndata object: https://anndata.readthedocs.io/en/latest/index.html
* Original cell expression and augmented cell expressions are stored in a matrix. The matrix is N x C, where N is cell ID and C is the number of channels.

## Data Preparation
The Input Data should have the following structure:
* The IMC image in TIFF in the format: horizontal dimension of the image (width) x vertical dimension of the image (height) x number of channels imaged.
* The Mask image in TIFF in the format: horizontal dimension of the image (width) x vertical dimension of the image (height)
* Probability to apply each augmentation in a list: [0.2, 0.2, 0.2, 0.2, 0.2] (shift, rotate, merge, expand, shrink) would give an equal probability to apply each augmentation.
* Number of augmentations wish to generate in int: 500 - would give 500 augmentations, so the output will have 500 original expressions and 500 augmented expressions.
* Note: The final output may have fewer augmentations than number of augmentations wish to generate since some errors may arise during the process. E.g. No neighbour cell can be selected to merge when try to apply merge transformation; cells are too small to apply shrink transformation; edge cells may result errors when transformations are applied. All error cells will be reported.
