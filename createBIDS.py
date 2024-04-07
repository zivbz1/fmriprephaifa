#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A short script that will convert raw DICOM files into to NIFTI.GZ, and then create a BIDS compatible structure (https://bids.neuroimaging.io/)
Updated by: Ziv Ben-Zion, April 2024
"""

# convert to NIFTI
import os   
from nipype.interfaces.dcm2nii import Dcm2niix
import shutil

#%% Convert functions Converts DICOM to NIFTI.GZ
def convert (source_dir, output_dir, subName, session): # this is a function that takes input directory, output directory and subject name and then converts everything accordingly
    try:
        os.makedirs(os.path.join(output_dir, subName, session))
    except:
        print ("folder already there")
#    try:
#       os.makedirs(os.path.join(output_dir, subName, ))
#    except:
#       print("Folder Exist")    
    converter = Dcm2niix()
    converter.inputs.source_dir = source_dir
    converter.inputs.compression = 7
    converter.inputs.output_dir = os.path.join( output_dir, subName, session)
    converter.inputs.out_filename = subName + '_%d , %a, %c'
    converter.run()

#%% Check functions
def checkGz (extension):
     # check if nifti gz or something else
    if extension[1] =='.gz':
        return '.nii.gz'
    else:
        return extension[1]

def checkTask(filename):
    sep = 'bold'
    rest = filename.split(sep)[1] # takes the last part of filename
    taskName = rest.split('.',1)[0]
    if taskName.find('(MB4iPAT2)')!=-1: # if the filename contains these words - remove it
        taskName = taskName.split('(MB4iPAT2)') # this is the part that will be omitted from the file name. If you have an extra - you should add that too. 
        taskName = taskName[0] + taskName[1] # cmobine toghether
   

    return taskName.replace("_","")


#%%
def organizeFiles(output_dir, subName, session):
    
    fullPath = os.path.join(output_dir, subName, session)
    os.makedirs(fullPath + '/dwi')
    os.makedirs(fullPath + '/anat')    
    os.makedirs(fullPath + '/func')
    os.makedirs(fullPath + '/misc')    
    
    a = next(os.walk(fullPath)) # list the subfolders under subject name

    # run through the possibilities and match directory with scan number (day)
    for n in a[2]:
        print (n)
        b = os.path.splitext(n)
        # add method to find (MB**) in filename and scrape it
        if n.find('diff')!=-1:
            print ('This file is DWI')
            shutil.move((fullPath +'/' + n), fullPath + '/dwi/' + n)
            os.rename((os.path.join(fullPath, 'dwi' ,n)), (fullPath + '/' + 'dwi' +'/' + subName + '_' + session +'_dwi' + checkGz(b)))
   
        elif n.find('MPRAGE')!=-1:
            print (n + ' Is Anat')
            shutil.move((fullPath + '/' + n), (fullPath + '/anat/' + n))
            os.rename(os.path.join(fullPath,'anat' , n), (fullPath + '/anat/' + subName+ '_' + session + '_acq-mprage_T1w' + checkGz(b)))
        elif n.find('t1_flash')!=-1:
            print (n + ' Is Anat')
            shutil.move((fullPath + '/' + n), (fullPath + '/anat/' + n))
            os.rename(os.path.join(fullPath,'anat' , n), (fullPath + '/anat/' + subName+ '_' + session + '_acq-flash_T1w' + checkGz(b)))
        elif n.find('t1_fl2d')!=-1:
            print (n + ' Is Anat')
            shutil.move((fullPath + '/' + n), (fullPath + '/anat/' + n))
            os.rename(os.path.join(fullPath,'anat' , n), (fullPath + '/anat/' + subName+ '_' + session + '_acq-fl2d1_T1w' + checkGz(b))) 
        elif n.find('GRE_3D_Sag_Spoiled')!=-1:
            print (n + ' Is Anat')
            shutil.move((fullPath + '/' + n), (fullPath + '/anat/' + n))
            os.rename(os.path.join(fullPath,'anat' , n), (fullPath + '/anat/' + subName+ '_' + session + '_acq-gre_spoiled_T1w' + checkGz(b)))            
        elif n.find('bold')!=-1:
            print(n  + ' Is functional')
            taskName = checkTask(n)
            shutil.move((fullPath + '/' + n), (fullPath + '/func/' + n))
            os.rename(os.path.join(fullPath, 'func', n), (fullPath  + '/func/' +subName+'_' +session + '_task-' + taskName + '_bold' + checkGz(b)))
        else:
            print (n + 'Is MISC')
            shutil.move((fullPath + '/' + n), (fullPath + '/misc/' + n))
           # os.rename(os.path.join(fullPath, 'misc', n), (fullPath +'/misc/' +'sub-'+subName+'_ses-' +sessionNum + '_MISC' + checkGz(b)))
    
# need to run thorugh misc folder and extract t1's when there is no MPRAGE - Need to solve issue with t1 - as adding the names is not validated with BIDS

#%%
sessionDict = {

      'ses-1': '/media/Data/Aging/Raw_Data/AG_15/pb10255_levy',
#'ses-2': '/media/Drobo/Levy_Lab/Projects/PTSD_reconsolidation/TrioB/Scan_data/newer/RCF020/RCF020_D2_tb1515_harpaz-rotem',
#'ses-3': '/media/Drobo/Levy_Lab/Projects/PTSD_reconsolidation/TrioB/Scan_data/newer/RCF020/RCF020_D3_tb1521_harpaz-rotem',
#'ses-4': '/media/Data/PTSD_KPE/kpe1468/kpe1468_scan4_pb9179_harpaz-rotem'
        }
subNumber = '015'
def fullBids(subNumber, sessionDict):
    output_dir = '/media/Data/Aging/agingBIDS'
    subName = 'sub-' + subNumber
  #  folder_name = ['anat','func','dwi','other']
    
    for i in sessionDict:
        session = i
        source_dir = sessionDict[i]
        print (session, source_dir)
        fullPath = os.path.join(output_dir, subName, session)
        print(fullPath)
        convert(source_dir,  output_dir, subName, session)
        organizeFiles(output_dir, subName, session)        
        
    
    #print (v)
#%%
fullBids(subNumber, sessionDict)

#%%
import glob
import json
import os 

subNumber = '018'
ses = {}
root_dir='/home/rl829/scratch60/agingBIDS/'
file_structure = '/ses-1/func/sub-*_ses-1*.json'
#glober = root_dir+file_stracture

glober = root_dir+"sub-"+subNumber+file_structure
# get all subjects data in a dicionary
for sub in glob.glob(glober):
    name = sub.split(sep="/")
    if name[5] not in ses:
        ses[name[5]] = {}
    if "rest" not in sub:  
        with open(sub, "r") as read_file:
            data = json.load(read_file)
            name = sub.split(sep="/")
            ses[name[5]][name[8].split("_")[2]]=data['SeriesNumber']    

# rearange order and set it to start at 1
for key in ses:
    sub = ses[key]
    key_min = min(sub.keys(), key=(lambda k: sub[k]))
    value_min = sub[key_min]
    for k in sub:
        sub[k]=sub[k]-value_min+1
        
for key in ses:
    sub =ses[key]
    for task in sub:
        oldnifti = root_dir+key+'/ses-1/func/'+key+"_ses-1_"+task+"_bold.nii.gz"
        newnifti = root_dir+key+'/ses-1/func/'+key+"_ses-1_task-"+str(sub[task])+"_bold.nii.gz"
               
        oldjson = root_dir+key+'/ses-1/func/'+key+"_ses-1_"+task+"_bold.json"
        newjson = root_dir+key+'/ses-1/func/'+key+"_ses-1_task-"+str(sub[task])+"_bold.json"
        os.rename(oldnifti,newnifti)
        os.rename(oldjson,newjson)
