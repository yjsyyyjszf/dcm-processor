def dicomAnonymizer(jobName, headers, params, added_params, **kwargs):
  injected_params["deleted"] = ["dicom"]
  return True, injected_params
  
def systemcleaner(jobName, headers, params, added_params, **kwargs):
  return True, {}
