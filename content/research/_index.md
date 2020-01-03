+++
title = "Research"
+++

For a full list of publications please see [Google Scholar](https://scholar.google.co.uk/citations?user=C-M77l8AAAAJ&hl=en). 


<div class="container-fluid mt-2 pb-0 card card-body border-dark">
    <h4>Current and past research:</h4>
    <p>
    <ul class="nav flex-column">
    <li class="nav-item">
        <a class="nav-link" href="#sc">Probabilistic modelling of single-cell genomics data</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#disease">Disease genomics & cancer</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#ml">Probabilistic machine learning</a>
    </li>
    </ul>
    </p>
</div>


<div class="container-fluid mt-4 pb-0" id="sc">
    <h5>Probabilistic modelling of single-cell genomics data</h5>
    <p>Current research interests in this area include creating statistical machine learning models and scalable inference paradigms to understand cell type composition, interactions, and signatures from single-cell and spatially-resolved 'omics data with a focus on the tumour microenvironment.</p>
    <strong>Research works:</strong>
    <div class="card mb-1">
        <div class="card-header">Automated assignment of the tumour microenvironment from single-cell RNA-seq</div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-5 col-sm-12">
                    <img src="/img/research/cellassign.gif" class="img-fluid" alt="CellAssign">
                </div>
                <div class="col-md-7 col-sm-12">
                    <p>We created CellAssign, a novel statistical model implemented in Google's Tensorflow to assign cells to known tumour microenvironment cell types from single-cell RNA-sequencing data, across large patient cohorts while controlling for sample and technical effects.</p>
                    <p><a href="https://www.nature.com/articles/s41592-019-0529-1" class="btn btn-outline-secondary" style="white-space: normal">Zhang et al. 2019 (Nature Methods)</a></p>
                </div>
            </div>
        </div>
    </div>
    <div class="card mb-1">
        <div class="card-header">Statistical integration of single-cell RNA and DNA sequencing data</div>
        <div class="card-body">
            <div class="row">
                    <div class="col-md-3 col-sm-12">
                        <img src="/img/research/clonealign.png" class="img-fluid" alt="CloneAlign">
                    </div>
                    <div class="col-md-9 col-sm-12">
                        <p>CloneAlign assigns cells as measured with single-cell RNA-seq to mutational cancer clones defined by copy number profiles by probabilistically mapping RNA-seq to clone-specific copy number profiles using reparametrization gradient variational inference.</p>
                        <p><a href="https://www.nature.com/articles/s41592-019-0529-1" class="btn btn-outline-secondary"  style="white-space: normal">Campbell et al. 2019 (Genome Biology)</a></p>
                    </div>
                </div>
        </div>
    </div>
    <div class="card mb-1">
        <div class="card-header">Pseudotime inference from single-cell RNA-seq</div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-5 col-sm-12">
                    <img src="/img/research/ouija.png" class="img-fluid" alt="CloneAlign">
                </div>
                <div class="col-md-7 col-sm-12">
                    <p>
                    We have created a number of  methods to understand single-cell trajectories from a probabilistic perspective, in particular (i) while controlling for heterogeneous genetic or phenotypic backgrounds, (ii) directly from marker genes allowing interpretable inference of pseudotimes, (iii) probabilistic inference of bifurcations.
                    </p>
                    <p><a href="https://www.nature.com/articles/s41467-018-04696-6" class="btn btn-outline-secondary"  style="white-space: normal">Campbell and Yau (Nature Communications)</a></p>
                    <p><a href="https://academic.oup.com/bioinformatics/article/35/1/28/5043298" class="btn btn-outline-secondary"  style="white-space: normal">Campbell and Yau (Bioinformatics)</a></p>
                    <p><a href="https://wellcomeopenresearch.org/articles/2-19/v1" class="btn btn-outline-secondary"  style="white-space: normal">Campbell and Yau (Wellcome Open Research)</a></p>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="container-fluid mt-4" id="disease">
    <h5>Disease genomics & cancer</h5>
    <p>Current research interests include how the tumour microenvironment modulates both tumour evolution and phenotypic state, as well as deriving novel progression scores and signatures from high dimensional clinical, imaging, and 'omics data.</p>
    <strong>Research works:</strong>
    <div class="card mb-1">
        <div class="card-header">Tissue dissociation effects on scRNA-seq of solid tumours</div>
        <div class="card-body">
            <p> We performed single-cell RNA-sequencing of a large number of solid tumour types (patient derived xenografts, cell lines, primary tumour samples) in breast and ovarian cancers to uncover the effect of tissue dissociation using collagenase at 37C to alternative enzymes at lower temperatures. We found a marked upregulation of stress pathway related genes.</p>
            <p><a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1830-0" class="btn btn-outline-secondary"  style="white-space: normal">O'Flanagan et al. (Genome Biology)</a></p>
        </div>
    </div> 
    <div class="card mb-1">
        <div class="card-header">Single-cell Parkinson's disease progression modelling of stem cells</div>
        <div class="card-body">
            <p> We performed single-cell RNA-sequencing of iPSC-derived dopaminergic neurons from Parkinson's patients and controls to reconstruct disease progression at single-cell level. Through differential expression analysis we uncovered mis-localization of the protein HDAC4 being implicated in Parkinson's progression.</p>
            <p><a href="https://www.sciencedirect.com/science/article/pii/S1934590918305046" class="btn btn-outline-secondary"  style="white-space: normal">Lang et al. (Cell Stem Cell)</a></p>
        </div>
    </div> 
</div>

<div class="container-fluid mt-4" id="ml">
    <h5>Probabilistic machine learning</h5>
    <p>Current research interests in this area include statistical machine learning methods for understanding structure and outcome prediction calibration from large heterogeneous datasets such as EHRs in the presence of high levels of missing data.
    </p>
    <strong>Research works:</strong>
        <div class="card mb-1">
            <div class="card-header">Covariate Gaussian Process Latent Variable Models</div>
            <div class="card-body">
                <div class="row">
                    <div class="col-sm-12 col-md-5">
                        <img src="/img/research/cgplvm.png" class="img-fluid" alt="CloneAlign">
                    </div>
                    <div class="col-md-7 col-sm-12">
                        <p>
                            Covariate Gaussian Process Latent Variable Models (C-GPLVMs) are a novel type of probabilistic latent variable model similar to a GPLVM except the functional form of the outputs wrt the latent space is modified by an additional set of covariates.
                            </p>
                            <p><a href="http://proceedings.mlr.press/v97/martens19a/martens19a.pdf" class="btn btn-outline-secondary"  style="white-space: normal">Martens et al. (ICML)</a>
                        </p>
                    </div>
                </div>
            </div>
    </div> 
</div>
