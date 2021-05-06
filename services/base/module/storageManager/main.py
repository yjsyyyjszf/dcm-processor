import os, shutil, requests, base64, json, time
from lib import nifti_to_dicom, import_dicom_to_orthanc, load_and_update_meta
import SimpleITK as sitk

DATA = os.getenv('DATA', '/data')
ORTHANC_REST_USERNAME = os.getenv('ORTHANC_REST_USERNAME', "anduin")
ORTHANC_REST_PASSWORD = os.getenv('ORTHANC_REST_PASSWORD', "anduin")
ORTHANC_REST_URL = os.getenv('ORTHANC_REST_URL', "http://orthanc:8042")
DEFAULT_STORE = os.getenv('ORTHANC_DEFUALT_STORE', "pac")
FORMATS = {
  "pdf": "data:application/pdf;base64,"
}

COPY_TAGS = [ '0002-0002', '0008-0016', '0008-0022', '0008-0023', '0008-0032', '0008-0033',
              '0008-0060', '0020-000d', '0020-0012', '0010-0010', '0010-0020', '0010-0030',
              '0010-0032', '0010-0040', '0020-0010', '0018-5100', '0018-0060', '0008-0090',
              '0008-0050', '0008-0020', '0008-0030', '0018-0015', '0040-0254', '0018-1030']

def load_header_codes():
  data = {}
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'header_codes.json')) as f:
    data = json.load(f)
  return data


def post_file_to_orthanc(filedata, filefmt, added_tags, seriesId):
  header = {'content-type': 'application/json'}
  authOrthanc = (ORTHANC_REST_USERNAME, ORTHANC_REST_PASSWORD)
  url = ORTHANC_REST_URL
  
  GET_studyinfo = url + "/series/" + seriesId + "/study"
  studyinfoResponse = requests.get(GET_studyinfo, auth=authOrthanc, headers=header)

  data = studyinfoResponse.json()

  tags = {
    "0405,0010" : "DCM-PROCESSOR",
    "0405,1001" : "store-data",
    "0405,1003" : filefmt,
    "0405,1005" : "dcm-processor",
    "0405,1007" : "pac",
  }

  tags.update(added_tags)

  payload = {
    "PrivateCreator": "DCM-PROCESSOR",
    "Parent": data["ID"],
    "Tags" : tags,
    "Content" : FORMATS[filefmt] + filedata
  }

  POST_pdf = url + "/tools/create-dicom"
  uploadpdfResponse = requests.post(POST_pdf, json=payload, auth=authOrthanc, headers=header)

  if uploadpdfResponse.status_code == 200:
    print("file successfully sent to orthanc")
  else:
    print("unable to sent file to orthanc")


def post_nifti_to_orthanc(path, filefmt, destination, added_tags, seriesId, base_folder):
  header = {'content-type': 'application/json'}
  authOrthanc = (ORTHANC_REST_USERNAME, ORTHANC_REST_PASSWORD)
  url = ORTHANC_REST_URL
  
  GET_seriesinfo = url + "/series/" + seriesId
  seriesinfoResponse = requests.get(GET_seriesinfo, auth=authOrthanc, headers=header)
  data = seriesinfoResponse.json()

  outpath = os.path.join(base_folder, seriesId)

  os.system(f"mkdir -p {outpath}")
  
  if "Instances" in data:
    instances = data["Instances"]
    if len(instances) > 0:
      instanceId = str(instances[0])
      dicom_tags = requests.get(url + "/instances/" + instanceId + "/content", auth=authOrthanc, headers=header)
      tags = dicom_tags.json()
      dicom_meta = []
      
      for tag in tags:
        if tag not in COPY_TAGS:
          continue
        tag_url = f"{url}/instances/{instanceId}/content/{tag}"
        meta = requests.get(tag_url, auth=authOrthanc, headers=header)
        dicom_meta.append((str(tag).replace("-", "|"), meta.text))
        
      #Set Custom header
      dicom_meta += [("0405|0010", "DCM-PROCESSOR"), ("0405|1001", "store-data"), ("0405|1003", filefmt), ("0405|1005", "dcm-processor"), ("0405|1007", destination)]

      #Set Series Description
      dicom_meta.append(("0008|103e", "Processed Information"))

      h_codes = load_header_codes()
      for k in added_tags:
        if k in h_codes:
          dicom_meta.append((h_codes[k], added_tags[k]))

      nifti_to_dicom(path, outpath ,dicom_meta)

      series_id = import_dicom_to_orthanc(outpath, url, ORTHANC_REST_USERNAME, ORTHANC_REST_PASSWORD)
      if (not series_id is None) and (not destination is None):
        time.sleep(2)
        patch_series_private_meta(series_id, {"0405-0010": "DCM-PROCESSOR", "0405-1001": "store-data", "0405-1003": filefmt, "0405-1005": "dcm-processor", "0405-1007": destination})
        
  os.system(f"rm -rf {outpath}")


def post_dicom_to_orthanc(path, filefmt, destination ,added_tags, seriesId, base_folder):
  header = {'content-type': 'application/json'}
  authOrthanc = (ORTHANC_REST_USERNAME, ORTHANC_REST_PASSWORD)
  url = ORTHANC_REST_URL
  
  GET_seriesinfo = url + "/series/" + seriesId
  seriesinfoResponse = requests.get(GET_seriesinfo, auth=authOrthanc, headers=header)
  data = seriesinfoResponse.json()

  if "Instances" in data:
    instances = data["Instances"]
    if len(instances) > 0:
      instanceId = str(instances[0])
      dicom_tags = requests.get(url + "/instances/" + instanceId + "/content", auth=authOrthanc, headers=header)
      tags = dicom_tags.json()
      dicom_meta = {}
      for tag in tags:
        if tag not in COPY_TAGS:
          continue

        tag_url = f"{url}/instances/{instanceId}/content/{tag}"
        meta = requests.get(tag_url, auth=authOrthanc, headers=header)
        dicom_meta[str(tag)] = meta.text

      h_codes = load_header_codes()
      for k in added_tags:
        if k in h_codes:
          dicom_meta[h_codes[k]] = added_tags[k]


      dicom_meta.update({"0405-0010": "DCM-PROCESSOR", "0405-1001": "store-data", "0405-1003": filefmt, "0405-1005": "dcm-processor", "0405-1007": destination})

      output = os.path.join(base_folder, seriesId)
      os.system(f"mkdir -p {output}")

      load_and_update_meta(path, output, dicom_meta)
      series_id = import_dicom_to_orthanc(output, url, ORTHANC_REST_USERNAME, ORTHANC_REST_PASSWORD)

      os.system(f"rm -rf {output}")

      if (not series_id is None) and (not destination is None):
        time.sleep(2)
        patch_series_private_meta(series_id, {"0405-0010": "DCM-PROCESSOR", "0405-1001": "store-data", "0405-1003": filefmt, "0405-1005": "dcm-processor", "0405-1007": destination})


def patch_series_private_meta(seriesId, tags):
  header = {'content-type': 'application/json'}
  authOrthanc = (ORTHANC_REST_USERNAME, ORTHANC_REST_PASSWORD)
  url = "http://localhost:8042"#ORTHANC_REST_URL

  payloadModify = {"Replace" : tags, "PrivateCreator": "DCM-PROCESSOR"}
  POST_modify = url + "/series/" + seriesId + "/modify"

  resp = requests.post(POST_modify, json=payloadModify, auth=authOrthanc, headers=header)

  if resp.status_code == 200:
    print("Successfully updated series")
    DELETE_series = url + "/series/" + seriesId
    requests.delete(DELETE_series, auth=authOrthanc, headers=header)
  else:
    print(resp.status_code)


def process_storage(storages, headers, params, added_params, **kwargs):

  base_folder = os.path.join(DATA, "storage_tmp")
  os.system(f"mkdir -p {base_folder}")

  for store in storages:
    if not isinstance(store, dict):
      continue

    if ("type" in store) and ("path" in store):
      f_type = store.get("type")
      f_type = str(f_type).lower()
      fullpath = os.path.join(DATA, store.get("path"))
      tags = {}
      destination = store.get("destination", DEFAULT_STORE)

      if "tags" in store:
        t = store.get("tags")
        if isinstance(t, dict):
          tags = t

      if f_type in FORMATS:
        try:
          fileobject = open(fullpath, "rb")
          filedata = str(base64.b64encode(fileobject.read()), 'utf-8')
          post_file_to_orthanc(filedata, f_type, tags, headers.get("seriesId"))
        except Exception as err:
          print(f"Error: {err}")

      elif f_type == "nifti":
        post_nifti_to_orthanc(fullpath, f_type, destination, tags, headers.get("seriesId"), base_folder)

      elif f_type == "dicom":
        post_dicom_to_orthanc(fullpath, f_type, destination, tags, headers.get("seriesId"), base_folder)
  
  os.system(f"rm -rf {base_folder}")


def worker(jobName, headers, params, added_params, **kwargs):
  try:
    for j in list(added_params.values()):
      if "storage" in j:
        tmp = j["storage"]
        storages = []

        if isinstance(tmp, list) or isinstance(tmp, tuple):
          storages = tmp
        elif isinstance(tmp, dict):
          storages = [tmp]

        process_storage(storages, headers, params, added_params, **kwargs)
  except:
    pass

