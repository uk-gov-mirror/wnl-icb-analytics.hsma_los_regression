CREATE TABLE [Data_Lab_NCL_Dev].[JakeK].[los_regression_preprocessing] (
	[los] INT,
    [provider_name] VARCHAR(100),
    [site_name] VARCHAR(100),
    [patient_age] INT,
    [patient_gender] VARCHAR(6),
    [flag_emergency] TINYINT
);

CREATE INDEX index1 
    ON [Data_Lab_NCL_Dev].[JakeK].[los_regression_preprocessing] 
    (provider_name ASC, site_name ASC);