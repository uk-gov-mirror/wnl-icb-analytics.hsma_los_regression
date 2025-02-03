/*Script to pull provider level sickness data*/
SELECT 
	[org_code] As [provider_code],
	YEAR([date]) AS [date_year],
	MONTH([date]) AS [date_month],
	[days_lost],
	[days_available]

FROM [Data_Lab_NCL_Dev].[JakeK].[wf_sickness_vw]

WHERE [staffgroup] = 'All staff groups'
AND [org_code] IN ('RAL', 'RAP', 'RRV', 'RKE') 