SELECT
	--PRIMARY KEY ID
	spl.[PRIMARYKEY_ID] AS [pid],
	--LoS
	[spell.discharge.length_of_hospital_stay] AS [los],
	--Mortality Details
	CASE [spell.discharge.method]
		WHEN 4 THEN 1
		ELSE 0
	END AS [death_flag],
	--Hospital Details
	CASE
		WHEN RIGHT([spell.patient.identity.local_patient_identifier.issuer] , 2) = '00' 
		THEN LEFT([spell.patient.identity.local_patient_identifier.issuer], 3)
		ELSE [spell.patient.identity.local_patient_identifier.issuer] 
		END AS [provider_code],
	[spell.care_location.site_code_of_treatment] AS [site_code],
	--Age
	[spell.patient.identity.age_on_admission] AS [patient_age]
	
FROM [Data_Store_SUS_Unified].[APC].[spell] spl

--Date in range
WHERE YEAR([spell.admission.date]) = 2024

--Remove people with no known los (or not yet discharged)
AND [spell.discharge.length_of_hospital_stay] IS NOT NULL

--Trim LoS data
AND [spell.discharge.length_of_hospital_stay] <= 100

--Adults only
AND [spell.patient.identity.age_on_admission] >= 18

--Limit data to non-regular activity
AND [spell.admission.intended_management] = 1

--Remove CNWL IP data
AND [spell.patient.identity.local_patient_identifier.issuer] != 'RV3'

--Remove historic data mislabelling NMUH as RFL
AND [spell.care_location.site_code_of_treatment] != 'RAL27'

--Remove sites known to have no beds (and therefore no possible los > 0)
AND [spell.care_location.site_code_of_treatment] NOT IN (
	 'RAL22', 'RAL80', 'RALMV', 'S2C1J', 'Y8D9M',
	 'W5Q6P', 
	 'P6H6T', 'RP603', 'RP604', 'RP605', 'RP606', 'RP608', 'RP610', 
	 'RP620', 'RP633',
	 'J1D4C', 'RRVCC', 'RRVCL', 'RRVNC', 'RRVP5', 'RRVRH')

--Remove non-relevant activity
--Maternity
AND LEFT([spell.commissioning.grouping.core_hrg], 2) != 'NZ'

--Mental Health
AND LEFT([spell.commissioning.grouping.core_hrg], 2) != 'WD'

--COVID
AND LEFT([spell.commissioning.grouping.core_hrg], 2) != 'DX'

--Paediatric Cystic Fibrosis
AND LEFT([spell.commissioning.grouping.core_hrg], 4) != 'PD13'

--Acute Drug Inoxication
AND LEFT([spell.commissioning.grouping.core_hrg], 4) != 'WH22'

--Acute Alcohol Intoxication
AND LEFT([spell.commissioning.grouping.core_hrg], 4) != 'WH21'

--Other
AND [spell.commissioning.grouping.core_hrg] NOT IN (
	'LA97B', 'WH50A', 'WH50B', 'BZ35A', 'BZ35B', 'AA82Z', 'PT52A', 'PT53A', 'WH01C')