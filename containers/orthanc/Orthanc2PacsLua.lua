function OnStoredInstance(instanceId, tags, metadata)
   -- Extract the value of the "PatientName" DICOM tag
   local ActionSource = tags['ActionSource']
   local ActionType = tags['ActionType']
   local Action = tags['Action']
   local ActionDestination = tags['ActionDestination']

   if ActionSource == "dcm-processor" then
      -- Only route series whose Action contains "store-data"
      if Action == 'store-data' then
	      print('Storing Data From ' .. ActionSource .. ' To ' .. ActionDestination )
	      SendToModality(instanceId, ActionDestination)
      end
  else
      -- Delete the patients that are not called "David"
      -- Delete(instanceId)
   end
end
