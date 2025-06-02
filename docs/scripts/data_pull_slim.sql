CREATE TABLE [Data_Lab_NCL_Dev].[JakeK].[los_regression_slim] (
	[los] INT,
    [admission_date] DATE,
    [provider_code] VARCHAR(5),
    [site_code] VARCHAR(5),
    [patient_age] INT,
    [patient_gender] INT,
    [admission_method] CHAR(2),
    [hrg_code] CHAR(5)
);

CREATE INDEX index1 
    ON [Data_Lab_NCL_Dev].[JakeK].[los_regression_slim] 
    (admission_date ASC, provider_code ASC, site_code ASC);