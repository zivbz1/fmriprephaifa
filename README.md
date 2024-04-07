# fMRIprephaifa
Neuroimaging Preprocessing Pipeline for Haifa University
A repository for pipeline scripts - including organizing files and pre-processing using fMRIprep

# fMRIPrep Pipline
fmriPrep is a builtin pipeline that allow high quality preprocessing (https://fmriprep.org/en/latest/index.html#)

# Files Description
1. CreateBIDS.py -- A short script that will convert raw DICOM files into to NIFTI.GZ, and then create a BIDS compatible structure (https://bids.neuroimaging.io/)
2. fmriprep_onesub_onLocal.txt -- an example how to run fmriprep using docker (on a physical computer)
3. FmriPrep_singularity.sh -- A geenral script for running N subjects in the HPC (High Performance Cluster) at Yale (https://research.computing.yale.edu/services/high-performance-computing).

# FreeSurfer License File 
Need to create a "licenseFreeSurfer.txt" which gives us licence to use FreeSurfer as part of fMRIprep pipeline.
The license file should be transfered to the local folder. 
