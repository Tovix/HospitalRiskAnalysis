# Hospital Readmission Risk Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green.svg)](https://pandas.pydata.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Project Overview

The **Hospital Readmission Risk Analyzer** is a comprehensive healthcare analytics project that combines advanced data science techniques with practical clinical applications. This project analyzes over 100,000 hospital admissions to identify key factors influencing 30-day readmission rates among diabetic patients, providing actionable insights for healthcare administrators and clinicians.

**Key Achievements:**
- **Critical Risk Factors Identified** comorbidities as the strongest risk factor (OR = 3.00)
- **Advanced Python:** Implemented decorators, comprehensions, generators, and pandas optimizations
- **Clinical Guidelines:** Evidence-based protocols for reducing readmissions

---

## Dataset Information

**Source:** [Diabetes 130-US Hospitals Dataset (1999–2008)](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)  
**Domain:** Healthcare Analytics  
**Size:** 100,000+ hospital admissions across 130 US hospitals  
**Time Period:** 1999-2008  
**Features:** 50+ clinical, demographic, and treatment variables

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

## Project Structure

```
HospitalRiskAnalysis/
├── analysis.py              # Main analysis with advanced Python features
├── dashboard.py             # Interactive Streamlit dashboard
├── sqlAnalysis.py           # SQL queries and database operations
├── Technical_Report.md      # Comprehensive technical documentation
├── Business_Summary.md      # Executive summary and ROI analysis
├── README.md               # Project documentation
├── data/                   # Dataset files
├── figures/                # Generated visualizations
└── requirements.txt        # Python dependencies
```

---

## Analysis Components

### 1. Python & EDA (Advanced Implementation)

**Features Implemented:**
- **Decorators:** Timing decorator for performance monitoring
- **Comprehensions:** Efficient data transformations and filtering
- **Generators:** Memory-efficient data processing
- **Context Managers:** Resource management and cleanup
- **Pandas Optimizations:** Memory usage reduction and performance improvements

**Task:** Clean and explore the dataset using advanced pandas techniques and statistical analysis.
- **Research Questions Addressed:**
  1. Which medications are most associated with lower readmission rates?
  2. How does length of stay (`time_in_hospital`) affect readmission risk?
  3. Are there differences in readmission rates by age group or gender?
  4. What is the distribution of primary diagnoses (`diag_1`) among readmitted patients?
  5. How do the number of lab procedures or medications relate to readmission probability?

### 2. SQL Analysis

**Task:** Efficient querying and aggregation of large healthcare datasets.
- **SQL Analysis Focus:**
  1. Which three departments (`medical_specialty`) have the highest readmission rates, adjusting for age groups?
  2. What is the average length of stay for each admission type?
  3. Which medication combinations are most common among readmitted patients?
  4. What is the readmission rate by insurance type (`payer_code`)?
  5. Which diagnoses (`diag_1`) are most frequently associated with readmissions?

### 3. Statistical Analysis

**Task:** Hypothesis testing and effect size analysis for clinical interventions.
- **Statistical Questions Analyzed:**
  1. Is there a statistically significant difference in readmission rates between patients who had their diabetes medication changed during admission and those who did not?
  2. What is the confidence interval for readmission rates before and after a specific intervention (e.g., medication change)?
  3. Is there a significant difference in readmission rates between patients with and without comorbidities?
  4. Does changing diabetes medication during admission affect readmission risk (relative risk analysis)?
  5. Which patient demographic factors (such as age group, gender, or race) are most strongly associated with higher readmission rates?

---

## Skill Integration

- **Python + SQL:** Use SQL for heavy aggregation, then pandas for advanced analysis and visualization.
- **Python + Statistics:** Use pandas for data prep, then `scipy.stats` or `statsmodels` for hypothesis testing.
- **SQL + Statistics:** Use SQL to create summary tables, then Python for statistical modeling.
- **Python + EDA:** Use matplotlib/seaborn for all visualizations, highlighting trends and outliers.

---

## Deliverables

### **Completed Deliverables**

#### 1. **Technical Report** (`Technical_Report.md`)
- **Executive Summary:** Key findings and clinical implications
- **Data Preprocessing:** Advanced cleaning and feature engineering
- **Exploratory Analysis:** 5 comprehensive research questions with statistical validation
- **Statistical Analysis:** Hypothesis testing with effect sizes and confidence intervals
- **Clinical Recommendations:** Evidence-based protocols for readmission reduction
- **Quality Metrics:** Performance indicators and monitoring guidelines

#### 2. **Business Summary** (`Business_Summary.md`)
- **Executive Overview:** C-suite focused insights
- **Financial Impact:** ROI analysis with $3.75M-$6.25M projected savings
- **Implementation Roadmap:** 90-day phased deployment plan
- **Success Metrics:** KPIs and monitoring framework
- **Competitive Advantage:** Market differentiation strategies

#### 3. **Interactive Streamlit Dashboard** (`dashboard.py`)
- **Risk Calculator:** Real-time patient readmission risk assessment
- **Policy Simulator:** Intervention impact modeling and cost-benefit analysis
- **Analytics Dashboard:** Visual insights and trend analysis
- **Clinical Guidelines:** Evidence-based protocols and decision support

#### 4. **Advanced Python Implementation** (`analysis.py`)
- **Performance Optimized:** Decorators for timing and caching
- **Memory Efficient:** Pandas optimizations and categorical dtypes
- **Clean Architecture:** Modular functions with comprehensive documentation
- **Statistical Rigor:** Scipy and statsmodels integration

#### 5. **SQL Analysis** (`sqlAnalysis.py`)
- **Optimized Queries:** Efficient aggregation and filtering
- **Complex Joins:** Multi-table analysis and reporting
- **Performance Tuning:** Indexed queries and query optimization

#### 6. **Documentation & Repository**
- **Comprehensive README:** Setup instructions and project overview
- **Code Documentation:** Inline comments and function descriptions
- **Requirements Management:** Dependency tracking and version control

---

## Getting Started

### **Prerequisites**

```bash
# Python 3.8+
# Required packages (install via requirements.txt)
pip install -r requirements.txt
```

### **Installation**

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HospitalRiskAnalysis
   ```

2. **Install dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn ucimlrepo streamlit plotly scipy statsmodels
   ```

3. **Download the dataset**
   - Place the dataset file in the `data/` directory as `diabetic_data.csv`
   - Or use the built-in UCI ML Repository fetcher in the code

### **Running the Analysis**

#### **Main Analysis (Python)**
```bash
# Run the comprehensive analysis with advanced Python features
python analysis.py
```

#### **SQL Analysis**
```bash
# Execute SQL queries and database operations
python sqlAnalysis.py
```

#### **Interactive Dashboard (Streamlit)**
```bash
# Launch the interactive dashboard
streamlit run dashboard.py
```

Once running, access the dashboard at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.x.x:8501

### **Dashboard Features**

The Streamlit dashboard includes four main sections:
- **Risk Calculator:** Real-time patient readmission risk assessment
- **Policy Simulator:** Intervention impact modeling and cost-benefit analysis
- **Analytics Dashboard:** Visual insights and trend analysis
- **Clinical Guidelines:** Evidence-based protocols and decision support

---

## License

This project is for educational and research purposes only.

---

**This project showcases the integration of data cleaning, SQL, statistics, and business communication in a real-world healthcare
