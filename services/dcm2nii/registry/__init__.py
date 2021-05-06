import os

def callback(jobName, headers, params, added_params, **kwargs):
  injected_params = {}
  
  if "seriesId" in headers:
    seriesId = headers.get("seriesId")
    injected_params["output"] = os.path.join("nifti", f"{seriesId}.nii.gz")
    injected_params["base"] = "nifti"
    injected_params["filename"] = f"{seriesId}"
    injected_params["ext"] = ".nii.gz"

    # Add files to be deleted
    injected_params["storage"] = {
      "path": os.path.join("nifti", f"{seriesId}.nii.gz"),
      "type": "nifti"
    }

    #injected_params["deleted"] = ["nifti"]

  return True, injected_params