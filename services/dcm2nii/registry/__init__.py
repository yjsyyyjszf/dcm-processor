import os

def callback(headers, added_params, **kwargs):
  params = {}
  
  if "seriesId" in headers:
    seriesId = headers.get("seriesId")
    params["output"] = os.path.join("nifti", f"{seriesId}.nii.gz")
    params["base"] = "nifti"
    params["filename"] = f"{seriesId}"
    params["ext"] = ".nii.gz"

    # Add files to be deleted
    params["deleted"] = ["nifti"]

  return True, params