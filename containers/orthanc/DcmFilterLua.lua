function ReceivedInstanceFilter(dicom, origin, info)
   -- Only allow incoming MR images
   if dicom.Modality == 'CT' then
   	return true
   elseif dicom.SeriesDescription == 'ANDUIN' then
   	PrintRecursive(dicom)
   	return true
   else
   	PrintRecursive(dicom)
   	return false
   end
end