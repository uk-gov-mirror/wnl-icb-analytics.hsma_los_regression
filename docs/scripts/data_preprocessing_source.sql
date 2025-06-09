SELECT los.los, 
	--par.[Organisation_Name] AS [provider_name], 
	--org.[Organisation_Name] AS [site_name],
	par.[Organisation_Code] AS [provider_code],
	los.site_code AS [site_code], 
	patient_age, patient_gender, admission_method
FROM [Data_Lab_NCL_Dev].[JakeK].[los_regression_slim] los

LEFT JOIN [Dictionary].[dbo].[Organisation] org
ON los.site_code = org.[Organisation_Code]

LEFT JOIN [Dictionary].[dbo].[Organisation] par
ON org.[SK_OrganisationID_ParentOrg] = par.[SK_OrganisationID]