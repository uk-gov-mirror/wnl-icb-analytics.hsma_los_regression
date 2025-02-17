/*Script to pull provider level data on Hospital Acquired Infections*/
--Note this is pulling "Hospital-onset, healthcare associated" figures but this may change to "Total Cases" later.
SELECT
	[Year] AS [date_year], [Month] AS [date_month],
	[Organisation code] AS [provider_code], 
	SUM(Figure) AS [trust_hai_cases]

FROM [Data_Store_Performance].[pmct].[InfectionControlAppendReviseProvComm]
WHERE [Organisation code] IN ('RAP', 'RAL', 'RKE', 'RRV', 'RAN', 'RP4', 'RP6')
AND [Metric] = 'Hospital-onset, healthcare associated'
AND ([Year] >= 2021 OR ([Year] = 2022 AND [Month] > 10))

GROUP BY [Year], [Month], [Organisation code]
