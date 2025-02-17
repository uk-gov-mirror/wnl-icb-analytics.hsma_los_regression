/*Script to pull site level medically optimised (Discharge delay) data*/

SELECT
	[mo_join],
	[date_full],
	[medically_optimised] AS [smart_mo]

FROM (

	SELECT 
		--Tie each site name to a code for joining
		--RFH is using the RFL provider code as an estimate for other RFL sites
		CASE [siteName]
			WHEN 'Royal Free Hospital' THEN 'RAL01'
			WHEN 'Barnet Hospital' THEN 'RAL26'
			WHEN 'Chase Farm Hospital' THEN 'RALC7'
			WHEN 'North Middlesex Hospital' THEN 'RAP'
			WHEN 'UCLH' THEN 'RRV'
			WHEN 'Whittington Hospital' THEN 'RKE'
		END AS [mo_join],

		[reportDate] AS [date_full],

		[indicatorKeyName],
		[value_numeric]

	FROM [Data_Lab_NCL_Dev].[JakeK].[uec_daily_smart_vw]

	WHERE indicatorKeyName = 'medically_optimised'
) smrt

PIVOT (
	SUM ([value_numeric]) FOR [indicatorKeyName] IN
	([medically_optimised])
) AS pvt