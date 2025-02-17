/*Script to pull provider level sickness data*/
--Notes:
---Staff Group is filtered to all staff but may be more appropiate to use specific staff group(s) (i.e. Clinical)
---Potential issue with future data not including NMUH as its own organisation
SELECT 
	[org_code] As [provider_code],
	YEAR([date]) AS [date_year],
	MONTH([date]) AS [date_month],
	[days_lost] AS [sick_days_lost],
	[days_available] AS [sick_days_available]

FROM [Data_Lab_NCL_Dev].[JakeK].[wf_sickness_vw]

WHERE [staffgroup] = 'All staff groups'
AND [org_code] IN ('RAL', 'RAP', 'RRV', 'RKE', 'RAN', 'RP4', 'RP6') 