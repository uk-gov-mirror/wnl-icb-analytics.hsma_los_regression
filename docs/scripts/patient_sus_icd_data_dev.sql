SELECT DISTINCT icd.[PRIMARYKEY_ID], code
FROM [Data_Store_SUS_Unified].[APC].[spell.episodes.clinical_coding.diagnosis.icd] icd

INNER JOIN [Data_Store_SUS_Unified].[APC].[spell.episodes] ep
ON ep.PRIMARYKEY_ID = icd.PRIMARYKEY_ID
AND ep.EPISODES_ID = icd.EPISODES_ID

INNER JOIN [Data_Store_SUS_Unified].[APC].[spell] spl
ON spl.PRIMARYKEY_ID = ep.PRIMARYKEY_ID

WHERE (ep.[dominant_episode_flag] != 1
OR ICD_ID != 1)
AND YEAR(spl.[spell.admission.date]) = 2024 AND MONTH(spl.[spell.admission.date]) = 6