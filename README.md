# Understanding the Drivers of Length of Stay - HSMA #6010 

This project is seeking to create a model to understand the growth in Length of Stay (LoS) in NCL since April 2019.
The code contains a Python pipeline to iteratively modfiy the model and evaluation.

## Changelog

### [1.0.0] - 2025-06-23
#### Added
- First working version release. Model features include Age, Gender, Emergency Admission by Site
- The model can alternate between a Poisson Regression and a Random Forest Regressor model

## Usage
The working directory for this project contains the .env file and the Python notebook used to explore and validate the data.
The working directory is currently saved on the N Drive in the UEC and Productivity Team directory:

...\UEC and Productivity Team\UEC\HSMA Regression\archive


To use the code, copy the .env file into the top level directory of this project, setup the virtual environment, and run these scripts in sequence:
* a_data_pull.py
* b_data_validation.ipynb (optional)
* c_data_preprocessing.py
* d_evaluation.py

These scripts require site level directories in the data and output directories for each site listed in the config.toml. For example with default settings, the following directories need to exist to process RAL01 data:
* ./data/sites/RAL01
* ./output/sites/RAL01

The REGRESSOR variable in the .env file determines which regression model is used in c_data_preprocessing.py. This settings needs to be kept consistent when running d_evaluation.py meaning you need to re-run both c_data_preporcessing.py and evaluation.py whenever you edit this variable.

## Future Development

Further development of this project would include adding more sophisticated features to capture the type of diagnosis and activity the admission relates to. 

Potential features include: Previous Admissions, Primary Diagnosis, Comorbidities, Admission Type

## Licence
This repository is dual licensed under the [Open Government v3]([https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) & MIT. All code can outputs are subject to Crown Copyright.

## Contact
Jake Kealey - jake.kealey@nhs.net

Project Link: https://github.com/ncl-cancer-alliance/hsma_los_regression