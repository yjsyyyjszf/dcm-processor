TARGET = '/tmp/nifti'

function ToAscii(s)
   -- http://www.lua.org/manual/5.1/manual.html#pdf-string.gsub
   -- https://groups.google.com/d/msg/orthanc-users/qMLgkEmwwPI/6jRpCrlgBwAJ
   return s:gsub('[^a-zA-Z0-9-/-: ]', '_')
end

function OnStableSeries(seriesId, tags, metadata)
   print('This series is now stable, writing its instances on the disk: ' .. seriesId)

 
   local instances = ParseJson(RestApiGet('/series/' .. seriesId)) ['Instances']
   local patientId = ParseJson(RestApiGet('/series/' .. seriesId .. '/patient')) ['ID']
   local studyId = ParseJson(RestApiGet('/series/' .. seriesId .. '/study')) ['ID']

   print('NumberOfInstances: ' .. #instances)

   if #instances > 3 then

      --print(patientId)
      --print(studyId)

      local dcmpath = ToAscii(TARGET .. '/' .. seriesId)
      os.execute('mkdir -p "' .. dcmpath .. '"')

      local data = ParseJson(RestApiGet('/instances/' .. instances[1] .. '/simplified-tags'))
      -- local target = assert(io.open(TARGET .. '/' .. seriesId .. '.json', 'wb'))
      -- target:write(DumpJson(data,true))
      -- target:close()

      for i, instance in pairs(instances) do

         --print(i,instance)

         -- Retrieve the DICOM file from Orthanc
         local dicom = RestApiGet('/instances/' .. instance .. '/file')      

         -- Write to the file
         local target = assert(io.open(dcmpath .. '/' .. instance .. '.dcm', 'wb'))
         target:write(dicom)
         target:close()
      end

      -- DCM2NIIX command line tool 
      -- local cmd = ToAscii('/run/secrets/dcm2niix -z y -b n -f ' .. seriesId .. ' -o ' .. TARGET .. ' ' .. dcmpath)
      -- print('Execute: ' .. cmd)
      -- os.execute(cmd)

      -- Anduin Connector (RestApi - POST)
      local urlAddress = os.getenv("SCHEDULER_HOST") .. ':' .. os.getenv("SCHEDULER_PORT") .. '/stable-series'
      -- local data = {}

      data["patientId"] = patientId
      data["studyId"] = studyId
      data["seriesId"] = seriesId
      data["dcmpath"] = seriesId

      local headers = {}
      headers["Content-Type"] = "application/json"
      --print(urlAddress)
      --print(data)
      HttpPost(urlAddress, DumpJson(data,true), headers)
   else
      print('EXIT: No valied DICOM Series for NIFTI Conversion!')

   end

end