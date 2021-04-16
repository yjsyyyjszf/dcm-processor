import os

DATA = os.getenv("DATA")

def worker(jobName, headers, params, added_params, **kwargs):
  a_params = added_params.get(jobName)
  
  if (not DATA is None) and (not a_params is None):
    base = a_params.get("base")
    filename = a_params.get("filename")
    dcmpath = headers.get("dcmpath")

    if (not base is None) and (not filename is None) and (not dcmpath is None):
      command = f"./dcm2niix -z y -b n -f {filename} -o {base} {dcmpath}"
      os.system(command)