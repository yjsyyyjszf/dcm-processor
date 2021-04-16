import os, json
from .anonymize import anonymize

DATA = os.getenv('DATA', '/data')
MODULES = os.getenv('MODULES', '/modules')


def worker(headers, params, added_params, **kwargs):
  if "seriesId" in headers:
    seriesId = str(headers.get("seriesId"))
    dcmpath = os.path.join(DATA, headers.get("dcmpath", seriesId))
    anonymize(dcmpath)
    
