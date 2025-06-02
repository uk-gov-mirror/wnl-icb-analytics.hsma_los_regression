SELECT los, 
	provider_code, par.[Organisation_Name] AS [provider_name], 
	site_code, org.[Organisation_Name] AS [site_name], 
	patient_age, patient_gender, admission_method
FROM [Data_Lab_NCL_Dev].[JakeK].[los_regression_slim] los

LEFT JOIN [Dictionary].[dbo].[Organisation] org
ON los.site_code = org.[Organisation_Code]

LEFT JOIN [Dictionary].[dbo].[Organisation] par
ON org.[SK_OrganisationID_ParentOrg] = par.[SK_OrganisationID]