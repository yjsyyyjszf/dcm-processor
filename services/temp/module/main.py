import os

DATA = os.getenv("DATA")
LOGS = os.getenv("LOGS")
MODULES = os.getenv("MODULE")

def worker(jobName, headers, params, added_params, **kwargs):
  print(f"{jobName} can be handled here")
  print(f"I can log info into the {LOGS} folde")
  print(f"I can write and read from the {DATA} folde")
  print(f"I can access other service modules from the {MODULES} folder")