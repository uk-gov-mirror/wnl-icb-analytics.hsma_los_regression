SELECT
	--PRIMARY KEY ID
	spl.[PRIMARYKEY_ID] AS [pid],
	--LoS
	[spell.discharge.length_of_hospital_stay] AS [los],
	--ID of patient to join to other datasets
	[spell.patient.identity.nhs_number.value Pseudo] AS [nhs_pseudo],
	--Hospital Details
	[spell.patient.identity.local_patient_identifier.issuer] AS [provider_code],
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
	[spell.admission.admission_type] AS [pod_actual],
	--HRG
	[spell.commissioning.grouping.core_hrg] AS [hrg_code],
	--Admission Context
	[spell.admission.method] AS [admission_method],
    [spell.admission.source] AS [admission_source]
	

FROM [Data_Store_SUS_Unified].[APC].[spell] spl
WHERE YEAR([spell.admission.date]) = 2024 AND MONTH([spell.admission.date]) = 6