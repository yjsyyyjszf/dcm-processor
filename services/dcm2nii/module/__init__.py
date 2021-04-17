import os

DATA = os.getenv("DATA")
dir_path = os.path.dirname(os.path.realpath(__file__))

def worker(jobName, headers, params, added_params, **kwargs):
  a_params = added_params.get(jobName)
  
  if (not DATA is None) and (not a_params is None):
    base = a_params.get("base")
    filename = a_params.get("filename")
    dcmpath = headers.get("dcmpath")

    if (not base is None) and (not filename is None) and (not dcmpath is None):
      dcm2niix = os.path.join(dir_path, "dcm2niix")
      fullbase = os.path.join(DATA, base)
      fulldcmpath = os.path.join(DATA, dcmpath)
      command = f"{dcm2niix} -z y -b n -f {filename} -o {fullbase} {fulldcmpath}"
      os.system(f"mkdir -p {fullbase}")
      os.system(command)