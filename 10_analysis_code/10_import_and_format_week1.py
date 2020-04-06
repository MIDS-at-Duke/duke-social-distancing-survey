import pandas as pd
import numpy as np
import re
import json

# Import variable names
# and value codes
col_names = '../00_raw_data/20200401_duke_covid_survey/question_names.json'
value_labels = '../00_raw_data/20200401_duke_covid_survey/answers.json'

with open(col_names,'r') as f:
    names = json.load(f)

with open(value_labels,'r') as f:
    labels = json.load(f)


# Import data and apply names / value_labels.
svy = pd.read_csv('../00_raw_data/20200401_duke_covid_survey'
                  '/raw_survey_data_uniqueid_only_duke_202004.txt', 
                  delimiter='\t')

for i in labels.keys():
    if i in svy.columns and i not in ['q4', 'q6', 'q7', 'q10']:
        svy[i] = svy[i].astype('str').str.replace(".0", "")
        svy[i] = svy[i].replace('nan', np.nan)
        svy[i] = svy[i].replace(labels[i])

for c in ['q4', 'q5','q6', 'q7', 'q10']:
    svy[c] = svy[c].replace(127, np.nan)

drop_rollups = [n for n in svy.columns if not re.match('.*_rollup', n)]
svy = svy[drop_rollups]
svy = svy.rename(names, axis='columns')
svy.sample().T

# Some sentinal missing codes:




svy.to_csv('../00_raw_data/20200401_duke_covid_survey/raw_survey_data_202004_LABELED.csv')