/*Script to pull provider level vacancy data*/
--Notes:
---Staff group is filtered to all staff ('Total') but may be more suitable to use specific staff group(s) (i.e. Clinical)

--CTE to duplicate RFL data for NMUH
WITH Org_map (source_code, destination_code) AS (
    SELECT 'RAL', 'RAL' UNION ALL
    SELECT 'RAL', 'RAP' UNION ALL
	SELECT 'RRV', 'RRV' UNION ALL
	SELECT 'RKE', 'RKE' UNION ALL
	SELECT 'RP4', 'RP4' UNION ALL
	SELECT 'RP6', 'RP6' UNION ALL
	SELECT 'RAN', 'RAN'
)

SELECT
	om.[destination_code] AS [provider_code],
	YEAR([date_data]) AS [date_year],
	MONTH([date_data]) AS [date_month],
	[vacancy] AS [vac_vacancy],
    [sub_sip] AS [vac_sub_sip]

FROM [Data_Lab_NCL_Dev].[JakeK].[wf_pwr_kpi_vw] vac

LEFT JOIN Org_map om
ON vac.[org_code] = om.[source_code]

WHERE [type] = 'Total'
AND [org_code] IN ('RAL', 'RRV', 'RKE', 'RAN', 'RP4', 'RP6')