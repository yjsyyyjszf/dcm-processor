import os, shutil

DATA = os.getenv('DATA', '/data')

def worker(headers, params, added_params, **kwargs):
  try:
    for j in list(added_params.values()):
      if "deleted" in j:
        tmp = j["deleted"]
        fns = []

        if isinstance(tmp, list) or isinstance(tmp, tuple):
          fns = tmp
        elif isinstance(tmp, str):
          fns = [tmp]

        for fn in fns:
          try:
            ffn = os.path.join(DATA, fn)
            if os.path.exists(ffn):
              if os.path.isfile(ffn):
                os.remove(os.path.join(DATA, fn))
              elif os.path.isdir(ffn):
                shutil.rmtree(ffn)
          except:
            pass
  except:
    pass