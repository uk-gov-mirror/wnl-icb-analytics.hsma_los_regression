SELECT sus.*
FROM (
	SELECT
		--PRIMARY KEY ID
		spl.[PRIMARYKEY_ID] AS [pid],
		--LoS
		[spell.discharge.length_of_hospital_stay] AS [los],
		--ID of patient to join to other datasets
		[spell.patient.identity.nhs_number.value Pseudo] AS [nhs_pseudo],
		--Hospital Details
		CASE
			WHEN RIGHT([spell.patient.identity.local_patient_identifier.issuer] , 2) = '00' 
			THEN LEFT([spell.patient.identity.local_patient_identifier.issuer], 3)
			ELSE [spell.patient.identity.local_patient_identifier.issuer] 
			END AS [provider_code],
		[spell.care_location.site_code_of_treatment] AS [site_code],
		--Seasonality of admission
		[spell.admission.date] AS [admission_date],
		[spell.admission.time] AS [admission_time],
		DATENAME(dw,[spell.admission.date]) AS [admission_dayofweek],
		--Patient Details
		[spell.patient.identity.gender] AS [patient_gender],
		[spell.patient.identity.ethnic_category] AS [patient_ethniccat],
		[spell.patient.identity.age_on_admission] AS [patient_age],
		--POD
		[spell.admission.intended_management] AS [pod_intended],
		--HRG
		[spell.commissioning.grouping.core_hrg] AS [hrg_code],
		--Admission Context
		[spell.admission.method] AS [admission_method],
		[spell.admission.source] AS [admission_source]
	
	FROM [Data_Store_SUS_Unified].[APC].[spell] spl
) sus

WHERE EXISTS (
	SELECT 1
	FROM [Data_Lab_NCL_Dev].[dbo].[ref_Trust_vw]
	WHERE [org_code] = sus.[provider_code]
)

--Limit data to non-regular activity
AND pod_intended IN (1, 2)

AND YEAR([admission_date]) = 2024 AND MONTH([admission_date]) = 6

--Remove CNWL IP data
AND sus.[provider_code] != 'RV3'

--Remove historic data mislabelling NMUH as RFL
AND [site_code] != 'RAL27'

--Remove sites known to have no beds (and therefore no possible los > 0)
AND [site_code] NOT IN ('RAL22', 'RAL80', 'RALMV', 'S2C1J', 'Y8D9M',
	 'W5Q6P', 
	 'P6H6T', 'RP603', 'RP604', 'RP605', 'RP606', 'RP608', 'RP610', 
	 'RP620', 'RP633',
	 'J1D4C', 'RRVCC', 'RRVCL', 'RRVNC', 'RRVP5', 'RRVRH')