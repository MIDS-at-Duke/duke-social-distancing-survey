import pandas as pd
import numpy as np
import re

svy = pd.read_csv('../00_raw_data/20200401_duke_covid_survey/'
                  'raw_survey_data_202004_LABELED.csv')

#########
# Set to common top-codes
#########
svy['Q10. Times in Group > 20 in Last Week'].value_counts(dropna=False)
svy.loc[svy['Q10. Times in Group > 20 in Last Week'] >9, 
        'Q10. Times in Group > 20 in Last Week'] = 9

#########
# Race is MOSTLY black and white, so re-group:
#########
race = 'Q19-20. Race + Ethnicity'
svy[race].value_counts()

svy[race] = svy[race].replace({'Asian': 'Other',
                               'Hispanic or Latino': 'Other',
                               'Another race': 'Other'})

##########
# In a big group in last week?
##########

# Check using weights like surveyors. 
# They say 15% of respondents have one children in 
# house, and 17% have two, and 60% have none. 
from statsmodels.stats.weightstats import DescrStatsW

def get_group_mean(data, question):
    temp = data[[question, 'weight2']]
    temp = temp[temp[question] !=127]
    temp = temp[pd.notnull(temp[question])]
    wsvy = DescrStatsW(temp[question], temp['weight2'])
    return wsvy.mean


for num in ['None', 'One', 'Two']:
    svy['zero_children'] = svy['Q5. Children in HH'] == num
    svy['dummy'] = 1

    # Raw average of 62% is high. 
    raw = svy['zero_children'].mean()

    w = svy.groupby('dummy').apply(lambda x: get_group_mean(x, 'zero_children'))
    w = w.iloc[0]
    
    print(f'raw avg with {num} kids: ')
    print(f'raw share: {raw:.3f}')
    print(f'weighted straight: {w:.3f}')

##########
# In a big group in last week?
##########


from statsmodels.stats.weightstats import DescrStatsW

def get_group_mean(data, question):
    temp = data[[question, 'weight']]
    temp = temp[temp[question] !=127]
    temp = temp[pd.notnull(temp[question])]
    wsvy = DescrStatsW(temp[question], temp['weight'])
    return wsvy.mean

svy.groupby('Q19-20. Race + Ethnicity').apply(
    lambda x: get_group_mean(x, 'Q10. Times in Group > 20 in Last Week'))


########
# How many NON-distanced contacts did people have?
########


# Note codes vary by survey type. For IVR, 
# topcode of 9:


# For non-IVR, topcode of... 127??
svy[svy['Survey Mode'] != 'IVR']['Q6. Non-HH Face to Face Count'].value_counts(normalize=True).sort_index()


svy['non_distanced_contacts'] = svy['Q6. Non-HH Face to Face Count'] - svy['Q7. Six Feet Away? (If Q6 > 0)']