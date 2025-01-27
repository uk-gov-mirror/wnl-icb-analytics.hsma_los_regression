SELECT
	[Year] AS [date_year], [Month] AS [date_month],
	[Organisation code] AS [provider_code], 
	SUM(Figure) AS [trust_hai_cases]

FROM [Data_Store_Performance].[pmct].[InfectionControlAppendReviseProvComm]
WHERE [Organisation code] IN ('RAP', 'RAL', 'RKE', 'RRV')
AND [Metric] = 'Hospital-onset, healthcare associated'
AND ([Year] >= 2021 OR ([Year] = 2022 AND [Month] > 10))

GROUP BY [Year], [Month], [Organisation code]
