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

# Keep only people who finish survey. 
svy = svy[pd.notnull(svy.q17)].copy()

# Non-IVR people exceed top-codes regularly. Recode those:
quant_questions = ['q4', 'q6', 'q7', 'q10', 'q12']

for q in ['q4', 'q6', 'q7', 'q10', 'q12']:
    svy.loc[(svy[q] > 9) & (svy[q] != 127), q] = 9

# Children had a top-code issue AND a entering zero issue
svy.loc[(svy['q5'] > 3) & (svy['q5'] < 9) & (svy[q] != 127), 'q5'] = 3
svy.loc[(svy['q5'] == 0), 'q5'] = 9

# Add value labels. 
for i in labels.keys():
    if i in svy.columns and i not in quant_questions:
        svy[i] = svy[i].astype('str').str.replace(".0", "")
        svy[i] = svy[i].replace('nan', np.nan)
        svy[i] = svy[i].replace('127', np.nan)
        svy[i] = svy[i].replace(labels[i])

# Values of 127 are refuse-to-answer, so make missing for now. 
for c in quant_questions:
    svy[c] = svy[c].replace(127, np.nan)

    
drop_rollups = [n for n in svy.columns if not re.match('.*_rollup', n)]
svy = svy[drop_rollups]
svy = svy.rename(names, axis='columns')
svy.sample().T

svy.to_csv('../00_raw_data/20200401_duke_covid_survey/raw_survey_data_202004_LABELED.csv')