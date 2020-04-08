# Load the cleaned, and labeled version 
# of the survey. 
# The code that generates this cleaned data
# can be found in `10_import_and_format_week1.py`. 

import pandas as pd
import numpy as np

svy = pd.read_csv('../20_analysis_datasets/merged_surveys.csv')

###########
# Add sample convenience vars
###########

svy['week1'] = svy['week'] == 'week1'
svy['week2'] = svy['week'] == 'week2'
svy['full_sample'] = 1

###########
# Demographic cleaning
###########

# Collapse small race vars
race = 'Q19-20. Race + Ethnicity'
svy[race].value_counts(dropna=False)

svy[race] = svy[race].replace({'Asian': 'Other',
                               'Hispanic or Latino': 'Other',
                               'Another race': 'Other'})
svy[race].value_counts(dropna=False)

##########
# Process COVID vars
##########

# Add num close interaction counts. 
svy['close_interactions'] = (svy['Q6. Non-HH Face to Face Count'] - 
                            svy['Q7. Six Feet Away? (If Q6 > 0)'])

svy.loc[svy['Q6. Non-HH Face to Face Count'] == 0, 'close_interactions'] = 0

# If 9, then it's actually ">=9", so can't do math. Ignore these people for now. 
svy.loc[svy['Q6. Non-HH Face to Face Count'] == 9, 'close_interactions'] = np.nan

# Some people list more "safe" interactions than total distances. 
svy.loc[svy['close_interactions'] < 0, 'close_interactions'] = 0

# Most variation is 0-1. 
svy['any_close_interactions'] = (svy['close_interactions'] > 0)
svy.loc[pd.isnull(svy.close_interactions), 'any_close_interactions'] = np.nan
svy['any_close_interactions'].value_counts(dropna=False)

# Ever in a big group?
big_group = 'Q10. Times in Group > 20 in Last Week'
svy['ever_in_group']= (svy[big_group] > 0) & pd.notnull(svy[big_group])
svy.loc[pd.isnull(svy[big_group]), 'ever_in_group'] = np.nan

working = 'Q8. HH Member Going to Work'
svy['someone_working'] = svy[working] == 'Yes'
svy.loc[~svy[working].isin(["No", "Yes"]), 'someone_working'] = np.nan

# Race shorthand
svy['race'] = svy['Q19-20. Race + Ethnicity']

##########
# Save
##########


svy.to_csv('../20_analysis_datasets/merged_surveys_w_analysis_vars.csv')
