import pandas as pd
import numpy as np
import re
import json

#########
# Look over two weeks
#########

files = {'week1': '20200401_duke_covid_survey_wk1',
         'week2': '20200407_duke_covid_survey_wk2'}


for f in files.keys():

    folder = files[f]
    
    # Import variable names
    # and value codes
    col_names = f'../00_raw_data/{folder}/question_names.json'
    value_labels = f'../00_raw_data/{folder}/answers.json'

    with open(col_names,'r') as json_file:
        names = json.load(json_file)

    with open(value_labels,'r') as json_file:
        labels = json.load(json_file)


    # Import data and apply names / value_labels.
    svy = pd.read_csv(f'../00_raw_data/{folder}'
                      f'/raw_survey_data_{f}.txt', 
                      delimiter='\t')

    # Keep only people who finish survey. 
    # Clarity defines as "has valid response for q17", so we'll use that too. 
    svy['Completed Survey'] = pd.notnull(svy.q17) & (svy.q17 != 127) & (svy.q17 != 4)


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

    svy['week'] = f
    
    svy.to_csv(f'../20_analysis_datasets/survey_data_{f}_CLEANED.csv', index=False)


##########
# Make merged dataset
##########

svys = [pd.read_csv(f'../20_analysis_datasets/'
                    f'survey_data_week{i}_CLEANED.csv')
        for i in range(1,3)]
merged = pd.concat(svys, sort=False)
merged.to_csv('../20_analysis_datasets/merged_surveys.csv', 
              index=False)
    
