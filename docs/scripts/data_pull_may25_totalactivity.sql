SELECT 
	COUNT(1) AS activity, AVG(los * 1.0) AS los, 
	provider_code, [site_code]
FROM (
SELECT
	--LoS (Target)
	[spell.discharge.length_of_hospital_stay] AS [los],
	--Features
	[spell.patient.identity.age_on_admission] AS [patient_age],
	[spell.patient.identity.gender] AS [patient_gender],
	[spell.admission.method] AS [admission_method],
	--Hospital Details
	parent.[Organisation_Code] AS [provider_code],
	[spell.care_location.site_code_of_treatment] AS [site_code]

FROM [Data_Store_SUS_Unified].[APC].[spell] spl

-- Derive Provider ------------------------------------------------------------
-- Get SK Organisation Code for the site
INNER JOIN [Dictionary].[dbo].[Organisation] child
ON spl.[spell.care_location.site_code_of_treatment] = child.[Organisation_Code]

-- Map the SK Parent Code to get the provider code
INNER JOIN [Dictionary].[dbo].[Organisation] parent
ON child.SK_OrganisationID_ParentOrg = parent.SK_OrganisationID
-------------------------------------------------------------------------------

--Intended management is planned to be overnight
WHERE [spell.admission.intended_management] = 1

--Limit to the main NCL sites
AND [spell.care_location.site_code_of_treatment] IN (
	'RRV03', 'RP401', 'RRVNQ', 'RAN01', 'RAL01', 'RRV30', 
	'C4M4J', 'RKEQ4', 'RAPNM')

--Limit data to a single month initially for testing
AND YEAR([spell.admission.date]) = 2024
) t
GROUP BY provider_code, site_code
ORDER BY COUNT(1) DESC