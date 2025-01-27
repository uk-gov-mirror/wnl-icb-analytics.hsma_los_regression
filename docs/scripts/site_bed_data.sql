/*Script to pull provider level data on Hospital Acquired Infections*/
SELECT 
	[date_full],
	[site_code],
	[provider_code],
	[G&ATotalBedsOpen] AS [site_beds_open],
	[G&ATotalBedsOccupied] AS [site_beds_occupied]

FROM (
	SELECT 
		[Period] AS [date_full],
		[Site_Code] AS [site_code],
		[OrgCode] AS [provider_code],
		[MetricName], [Value]

	FROM [Data_Store_UDAL].[UDAL].[UDAL_Daily_sitrep]
	WHERE OrgCode IN ('RAL', 'RAP', 'RKE', 'RRV')
) src

PIVOT (
	SUM(Value)
	FOR [MetricName] IN ([G&ATotalBedsOpen], [G&ATotalBedsOccupied])
) pvt