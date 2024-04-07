# fmriprephaifa
Neuroimaging Preprocessing Pipeline for Haifa University
A repository for pipeline scripts - including organizing files and pre-processing using fMRIprep

# fmriPrep
fmriPrep is a builtin pipeline that allow high quality preprocessing (for more information please see here: https://fmriprep.org/en/latest/index.html#)

In the folder fmriPrep you'll find three files.
1. licenseFreeSurfer.txt -- this is the freesurfer license file (should be transfered to your local HPC folder).
2. FmriPrep_singularity.sh -- this file will be used to run N subjects in the HPC (please go through the comments and adjust the script accordingly)
3. fmriprep_onesub_onLocal.txt -- an example how to run fmriprep using docker (on the Linux computer in the lab)
