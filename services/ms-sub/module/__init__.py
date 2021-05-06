import os
from .sub import subtract
import pydicom
DATA = os.getenv("DATA")
dir_path = os.path.dirname(os.path.realpath(__file__))

def worker(jobName, headers, params, added_params, **kwargs):

  
  if (not DATA is None):
    dcmpath = os.path.join(DATA,headers.get("dcmpath"))
    print(dcmpath)
    files = []
    for r,d,f in os.walk(dcmpath):
        for fi in f:
          files.append(os.path.join(r,fi))
    ds = pydicom.dcmread(files[0])
    pps = ds.PerformedProcedureStepDescription

    if pps == 'mssub':

      niftipath = added_params.get("dcm2nii").get("output")
      niftipath = os.path.join(DATA,niftipath)
      
      subtract(dcmpath, niftipath)
    
    else:
      print('mssub tag not found', flush=True)
      print(pps, flush=True)
   
