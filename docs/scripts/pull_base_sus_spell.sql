SELECT
	--LoS (Target)
	[spell.discharge.length_of_hospital_stay] AS [los],
	--Date of admission
	[spell.admission.date] AS [admission_date],
	--Features
	[spell.patient.identity.age_on_admission] AS [patient_age],
	[spell.patient.identity.gender] AS [patient_gender],
	[spell.admission.method] AS [admission_method],
	--Hospital Details
	parent.[Organisation_Code] AS [provider_code],
	[spell.care_location.site_code_of_treatment] AS [site_code]

FROM [Data_Store_SUS_Unified].[APC].[spell] spl

-- Get SK Organisation Code for the site
INNER JOIN [Dictionary].[dbo].[Organisation] child
ON spl.[spell.care_location.site_code_of_treatment] = child.[Organisation_Code]

-- Map the SK Parent Code to get the provider code
INNER JOIN [Dictionary].[dbo].[Organisation] parent
ON child.SK_OrganisationID_ParentOrg = parent.SK_OrganisationID

--Intended management is planned to be overnight
WHERE [spell.admission.intended_management] IN (1, 8)

--Limit to the main NCL sites
AND [spell.care_location.site_code_of_treatment] IN (
	'RRV03', 'RRVNQ', 'RAN01', 'RAL01', 'RRV30', 
	'C4M4J', 'RKEQ4', 'RAPNM')

--Limit data to a single month initially for testing
AND [spell.admission.date] >= '2022-01-01'

--Limit the data to adults
AND [spell.patient.identity.age_on_admission] >= 18

--Remove records with erroneous age values
AND [spell.patient.identity.age_on_admission] <= 120

--Remove records with no LoS
AND [spell.discharge.length_of_hospital_stay] IS NOT NULL
AND [spell.discharge.length_of_hospital_stay] > -1

--Remove non-relevant activity
--Maternity and neonatal
AND LEFT([spell.commissioning.grouping.core_hrg], 2) != 'NZ'
AND LEFT([spell.commissioning.grouping.core_hrg], 1) != 'P'

--Mental Health
AND LEFT([spell.commissioning.grouping.core_hrg], 2) != 'WD'

--COVID
AND LEFT([spell.commissioning.grouping.core_hrg], 2) != 'DX'

--Acute Drug Inoxication
AND LEFT([spell.commissioning.grouping.core_hrg], 4) != 'WH22'

--Acute Alcohol Intoxication
AND LEFT([spell.commissioning.grouping.core_hrg], 4) != 'WH21'

--Other
AND [spell.commissioning.grouping.core_hrg] NOT IN (
	'LA97B', 'WH50A', 'WH50B', 'BZ35A', 'BZ35B', 'AA82Z', 'WH01C')