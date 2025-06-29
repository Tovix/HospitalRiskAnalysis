# Hospital Readmission Risk Analyzer

## Overview

The **Hospital Readmission Risk Analyzer** is a healthcare analytics project focused on understanding and reducing hospital readmissions among diabetic patients. Using the [Diabetes 130-US Hospitals Dataset (1999–2008)](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008), this project demonstrates data cleaning, exploratory data analysis (EDA), SQL querying, and statistical analysis to uncover actionable insights.

---

## Dataset

- **Source:** UCI Machine Learning Repository  
- **Rows:** 100,000+ hospital admissions  
- **Columns:** 50+ features including demographics, diagnoses, medications, and outcomes  
- **Key columns:**  
  - `encounter_id`, `patient_nbr`, `race`, `gender`, `age`, `admission_type_id`, `discharge_disposition_id`, `admission_source_id`, `time_in_hospital`, `payer_code`, `medical_specialty`, `num_lab_procedures`, `num_procedures`, `num_medications`, `number_outpatient`, `number_emergency`, `number_inpatient`, `diag_1`, `diag_2`, `diag_3`, `max_glu_serum`, `A1Cresult`, medication columns, `change`, `diabetesMed`, `readmitted`, `weight`

---
| Column Name                | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| encounter_id               | Unique identifier for each hospital visit                                   |
| patient_nbr                | Unique identifier for each patient                                          |
| race                       | Patient’s race                                                              |
| gender                     | Patient’s gender                                                            |
| age                        | Patient’s age group (e.g., [70-80))                                         |
| admission_type_id          | Type of admission (e.g., emergency, urgent, resuscitation)                  |
| discharge_disposition_id   | Discharge status (e.g., home, expired)                                      |
| admission_source_id        | Source of admission (e.g., physician referral)                              |
| time_in_hospital           | Length of stay (in days)                                                    |
| payer_code                 | Primary payment method                                                      |
| medical_specialty          | Specialty of admitting physician                                            |
| num_lab_procedures         | Number of lab tests performed                                               |
| num_procedures             | Number of procedures (other than lab) performed                             |
| num_medications            | Number of medications administered                                          |
| number_outpatient          | Number of outpatient visits in the year prior                               |
| number_emergency           | Number of emergency visits in the year prior                                |
| number_inpatient           | Number of inpatient visits in the year prior                                |
| diag_1, diag_2, diag_3     | Primary, secondary, and tertiary diagnoses (ICD-9 codes)                    |
| max_glu_serum              | Maximum glucose serum test result                                           |
| A1Cresult                  | Most recent A1C test result                                                 |
| metformin, insulin, ...    | Medication columns (e.g., metformin, insulin, glyburide, etc.)              |
| change                     | Whether medications were changed during the encounter                       |
| diabetesMed                | Whether diabetes medication was prescribed                                  |
| readmitted                 | Whether the patient was readmitted within 30 days ("<30", ">30", "NO")      |
| weight                     | Patient's weight (may contain '?')                                          |

## Project Stages & Sample Questions

### 1. Python & EDA

- **Task:** Clean and explore the dataset using pandas and matplotlib.
- **Sample Questions:**
  1. Which medications are most associated with lower readmission rates?
  2. How does length of stay (`time_in_hospital`) affect readmission risk?
  3. Are there differences in readmission rates by age group or gender?
  4. What is the distribution of primary diagnoses (`diag_1`) among readmitted patients?
  5. How do the number of lab procedures or medications relate to readmission probability?

### 2. SQL

- **Task:** Query and aggregate large datasets efficiently.
- **Sample Questions:**
  1. Which three departments (`medical_specialty`) have the highest readmission rates, adjusting for age groups?
  2. What is the average length of stay for each admission type?
  3. Which medication combinations are most common among readmitted patients?
  4. What is the readmission rate by insurance type (`payer_code`)?
  5. Which diagnoses (`diag_1`) are most frequently associated with readmissions?

### 3. Statistics

- **Task:** Test the impact of interventions and policies.
- **Sample Questions:**
  1. Was the 2020 nurse-to-patient ratio policy change statistically significant in reducing readmissions?
  2. What is the confidence interval for readmission rates before and after a specific intervention?
  3. Is there a significant difference in readmission rates between patients with and without comorbidities?
  4. Does changing diabetes medication during admission affect readmission risk (chi-square test)?
  5. What is the effect size (Cohen’s d or odds ratio) of a new medication protocol on readmission rates?

---

## Skill Integration

- **Python + SQL:** Use SQL for heavy aggregation, then pandas for advanced analysis and visualization.
- **Python + Statistics:** Use pandas for data prep, then `scipy.stats` or `statsmodels` for hypothesis testing.
- **SQL + Statistics:** Use SQL to create summary tables, then Python for statistical modeling.
- **Python + EDA:** Use matplotlib/seaborn for all visualizations, highlighting trends and outliers.

---

## Deliverables

1. **Technical Report (PDF):**
   - Data description and cleaning steps
   - EDA findings with visualizations
   - Key SQL queries and explanations
   - Statistical test results (p-values, confidence intervals, effect sizes)
   - Actionable insights

2. **GitHub Repository:**
   - `data_cleaning.py` (pandas cleaning and EDA)
   - `queries.sql` (optimized SQL queries)
   - `statistical_analysis.ipynb` (Jupyter notebook with stats and plots)
   - `README.md` (project overview and instructions)

3. **Business Summary (1-pager):**
   - Key findings and recommendations for reducing readmissions

4. **(Optional) Streamlit Dashboard:**
   - Interactive readmission risk calculator
   - Policy impact simulation

---

## Getting Started

1. Clone this repository.
2. Download the dataset and place it in the `data/` directory as `diabetic_data.csv`.
3. Install requirements:
    ```bash
    pip install pandas numpy matplotlib seaborn ucimlrepo
    ```
4. Run the analysis:
    ```bash
    python analysis.py
    ```

---

## License

This project is for educational and research purposes only.

---

**This project showcases the integration of data cleaning, SQL, statistics, and business communication in a real-world healthcare
