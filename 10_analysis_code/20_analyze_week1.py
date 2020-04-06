import pandas as pd
import numpy as np
import re

svy = pd.read_csv('../00_raw_data/20200401_duke_covid_survey/'
                  'raw_survey_data_202004_CLEANED.csv')

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
    temp = data[[question, 'weight']]
    temp = temp[pd.notnull(temp[question])]
    wsvy = DescrStatsW(temp[question], temp['weight'])
    return wsvy.mean

for num in ['None', 'One', 'Two']:
    svy[num] = svy['Q5. Children in HH'] == num
    svy['dummy'] = 1

    raw = svy[num].mean()

    w = svy.groupby('dummy').apply(lambda x: get_group_mean(x, num))
    w = w.iloc[0]
    
    print(f'Share households with {num} kids:')
    print(f'\t raw share: {raw:.3f}')
    print(f'\t weighted share: {w:.3f}')

    if num == 'None':
        assert np.abs(w - 0.6) < 0.005
    if num == 'One':
        assert np.abs(w - 0.15) < 0.005
    if num == 'Two':
        assert np.abs(w - 0.17) < 0.005
        
##########
# In a big group in last week?
##########


from statsmodels.stats.weightstats import DescrStatsW

big_group = 'Q10. Times in Group > 20 in Last Week'
svy['any_big_group']= (svy[big_group] > 0) & pd.notnull(svy[big_group])
svy.loc[pd.isnull(svy[big_group]), 'any_big_group'] = np.nan

svy.groupby('Q19-20. Race + Ethnicity').apply(
    lambda x: get_group_mean(x, big_group))

svy.groupby('Q19-20. Race + Ethnicity').apply(
    lambda x: get_group_mean(x, 'any_big_group'))


########
# How many NON-distanced contacts did people have?
########


# Note codes vary by survey type. For IVR, 
# topcode of 9:


# For non-IVR, topcode of... 127??
svy[svy['Survey Mode'] != 'IVR']['Q6. Non-HH Face to Face Count'].value_counts(normalize=True).sort_index()


svy['non_distanced_contacts'] = svy['Q6. Non-HH Face to Face Count'] - svy['Q7. Six Feet Away? (If Q6 > 0)']