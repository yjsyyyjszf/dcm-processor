TARGET = '/tmp/nifti'

function ToAscii(s)
   -- http://www.lua.org/manual/5.1/manual.html#pdf-string.gsub
   -- https://groups.google.com/d/msg/orthanc-users/qMLgkEmwwPI/6jRpCrlgBwAJ
   return s:gsub('[^a-zA-Z0-9-/-: ]', '_')
end

function OnStableSeries(seriesId, tags, metadata)
 
   local series = ParseJson(RestApiGet('/series/' .. seriesId))
   local instances = series['Instances']

   if #instances > 3 then

      local patientId = ParseJson(RestApiGet('/series/' .. seriesId .. '/patient')) ['ID']
      local studyId = ParseJson(RestApiGet('/series/' .. seriesId .. '/study')) ['ID']
      local data = ParseJson(RestApiGet('/instances/' .. instances[1] .. '/simplified-tags'))

      local ActionSource = data["ActionSource"]

      if ActionSource == "dcm-processor" then
         return
      end

      print("Stable Series Received, Storing series on disk :" .. seriesId)

      local dcmpath = ToAscii(TARGET .. '/dicom/' .. seriesId)
      os.execute('mkdir -p "' .. dcmpath .. '"')

      for i, instance in pairs(instances) do
         -- Retrieve the DICOM file from Orthanc
         local dicom = RestApiGet('/instances/' .. instance .. '/file')      
         -- Write to the file
         local target = assert(io.open(dcmpath .. '/' .. instance .. '.dcm', 'wb'))
         target:write(dicom)
         target:close()
      end

      -- dcm scheduler (RestApi - POST)
      local urlAddress = os.getenv("SCHEDULER_HOST") .. ':' .. os.getenv("SCHEDULER_PORT") .. '/stable-series'

      data["patientId"] = patientId
      data["studyId"] = studyId
      data["seriesId"] = seriesId
      data["dcmpath"] = 'dicom/' .. seriesId

      local headers = {}
      headers["Content-Type"] = "application/json"
      HttpPost(urlAddress, DumpJson(data,true), headers)
   else
      print('EXIT: No valied DICOM Series for NIFTI Conversion!')
   end

end