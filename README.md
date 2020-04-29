# Duke Forge/SSRI COVID19 Digital Lab Social Distancing Survey
**WELCOME** to the Github repository for the Duke Forge/SSRI COVID19 Digital Lab Social Distancing Survey.
The aim of this survey--that will occurring on weekly waves planned for ~6 weeks total--is to survey North Carolina residents on their social mitigation practices and attitudes during the SARS-CoV-2/COVID-19.
As a service to the community and open research, these data are made available under a [Creative Commons Attribution-NonCommercial 4.0. License](http://creativecommons.org/licenses/by-nc/4.0/).

The Duke Forge/Duke University Social Science Research Institute (SSRI) COVID19 Digital Lab commissioned this survey, which is being conducted by Clarity+Campaign Labs (CCL) from March 29-31, 2020 through the next 5 weeks.

Full details of the survey methodology, the questionnaire instrument, and the data may be accessed and freely used here.

You can find an example analysis notebook in the `10_analysis_code` [file here](https://github.com/MIDS-at-Duke/duke-social-distancing-survey/blob/master/10_analysis_code/Example_Analysis_Notebook.ipynb) with details on how to work with this data in Python.

A cleaned merged survey file with value labels can be found in `20_analysis_datasets/merged_surveys_w_analysis_vars.csv`

* **Don Taylor, PhD**, Director of the Duke Social Science Research Institute
* **Erich S. Huang, MD, PhD**, Director of Duke Forge

## Methodology

This survey is composed of two samples: individuals who answered automated (IVR) surveys (via landlines), and individuals who answered (live) cell-phone survey calls. 

The universe of phone numbers from which individuals were selected comes from commercial appends to voter registration data in addition to commercially collected numbers of non-registered individuals consolidated by TargetSmart. 

Youth in the survey are also over-sampled to compensate for lower response rates.

Data is then re-weighted to be representative of the North Carolina adult (>18) population. 

Note that because this is a WEIGHTED survey, raw averages do not constitute consistent estimates of population attributes.
Top-line summary statistics can be found in `40_reports/Survey_Summaries`.
Survey instrument can be found in `SurveyQuestions.pdf`.

Response rates can be found in `40_reports/estimated_response_rates_20200421.xlsx`. 

## ERRATA: 

Between weeks 3 and 4 of our survey, it was discovered that an error had been in calculating weights for college educated respondents. **ALL** data and reports were updated with correct weights in commit [66de10](https://github.com/MIDS-at-Duke/duke-social-distancing-survey/commit/66de10801c8921968e27f16cba02e762cef07154), but some press releases made prior to this commit do reflect this error. As far as we can tell, the error was quite small and did not have any substantively meaningful effect on results, but be sure to use updated data for all analyses!

___
<img src="https://github.com/dukeforge/duke-social-distancing-survey/raw/master/assets/socialDistancePolling.png" width="400">
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
