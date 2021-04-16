import os

def callback(jobName, headers, params, added_params, **kwargs):
  injected_params = {"custom-data": "Some new data"}
  
  # Check header information etc. to see if you have to execute job
  # If Yes return True with the additional injected params
  # If No return False with additional injected params

  return True, injected_params