function OnStoredInstance(instanceId, tags, metadata)
   -- Extract the value of the "PatientName" DICOM tag
   local seriesName = string.lower(tags['SeriesDescription'])
   local seriesNumber = tags['SeriesNumber']

   print('Instance: ' .. seriesName)
   print('Number: ' .. seriesNumber)


  if string.find(seriesName, 'anduin') ~= nil and 
  	seriesNumber == "261282" then
	
	print('Sending PDF to PACS: ' .. seriesName)
	-- Only route series whose SeriesDescription contains "anduin"
	-- and SeriesNumber contains 261282
	SendToModality(instanceId, 'pacs')

  else
      -- Delete the patients that are not called "David"
      --Delete(instanceId)
   end
end
