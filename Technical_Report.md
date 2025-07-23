# Hospital Readmission Risk Analysis: Technical Report

**Project:** Hospital Readmission Risk Analyzer  
**Dataset:** Diabetes 130-US Hospitals Dataset (1999–2008)  
**Analysis Period:** 1999-2008  
**Sample Size:** 100,000+ hospital admissions across 130 US hospitals  

---

## Executive Summary

This comprehensive analysis of hospital readmission patterns among diabetic patients reveals critical insights for healthcare administrators and policy makers. Our study identified key risk factors, medication effects, and demographic patterns that significantly influence 30-day readmission rates. The analysis combines exploratory data analysis, statistical hypothesis testing, and SQL-based queries to provide actionable recommendations for reducing hospital readmissions.

**Key Findings:**
- Comorbidities increase readmission odds by 3x (OR = 3.00, 95% CI: 2.26–3.98)
- Medication changes during admission modestly increase readmission risk (RR = 1.10, 95% CI: 1.09–1.12)
- Age is the strongest demographic predictor of readmission risk
- Specific medications (Metformin, Glipizide, Pioglitazone, Rosiglitazone) are associated with lower readmission rates

---

## 1. Data Description and Preprocessing

### 1.1 Dataset Overview
The Diabetes 130-US Hospitals Dataset contains over 100,000 hospital encounters for diabetic patients from 130 US hospitals between 1999-2008. Each record represents a unique hospital admission with comprehensive clinical, demographic, and treatment information.

### 1.2 Data Cleaning Steps
**Missing Value Treatment:**
- Replaced NaN values in `max_glu_serum` and `A1Cresult` with "untested" (more informative than missing)
- Replaced '?' values in categorical columns (`race`, `payer_code`, `medical_specialty`, `weight`) with appropriate categories ("Other", "Others", "not-recorded")

**Data Type Optimization:**
- Converted 19 categorical columns from object to category dtype for memory efficiency
- Applied categorical encoding to: race, gender, age, admission_type_id, discharge_disposition_id, admission_source_id, medical specialties, diagnoses, and medication columns

**Feature Engineering:**
- Created `was_readmitted` binary indicator from readmitted column ('<30', '>30' → True, 'NO' → False)
- Generated `has_comorbidity` indicator based on presence of secondary/tertiary diagnoses
- Mapped admission types and discharge dispositions to descriptive labels for interpretability

---

## 2. Exploratory Data Analysis (EDA)

### 2.1 Medication Analysis
**Research Question:** Which medications are most associated with lower readmission rates?

**Findings:**
- **Metformin, Glipizide, Pioglitazone, and Rosiglitazone** showed the strongest association with lower hospital readmission rates
- These medications represent different classes of diabetes drugs, suggesting multiple therapeutic pathways may contribute to reduced readmission risk
- Analysis based on medication usage patterns across readmitted vs. non-readmitted patient groups

**Clinical Significance:** These findings suggest that certain diabetes medications may have protective effects beyond glucose control, potentially through improved patient stability or reduced complications.

### 2.2 Length of Stay Analysis
**Research Question:** How does length of stay (time_in_hospital) affect readmission risk?

**Findings:**
- **Length of stay does not appear to be strongly associated with readmission status** in this dataset
- After removing outliers using IQR method (Q1-1.5×IQR to Q3+1.5×IQR), the relationship remained weak
- Box plot analysis showed similar distributions across readmission categories

**Clinical Significance:** This suggests that discharge timing decisions may be appropriately calibrated, or that other factors beyond length of stay are more predictive of readmission risk.

### 2.3 Demographic Risk Factors
**Research Question:** Are there differences in readmission rates by age group or gender?

**Findings:**
- **Age Effect:** The likelihood of readmission increases significantly with patient age, especially for those over 60
- **Gender Effect:** Females have a higher readmission rate than males
- Age shows a clear dose-response relationship with readmission risk

**Clinical Significance:** Older patients require enhanced discharge planning and post-acute care coordination. Gender differences may reflect biological factors, care-seeking behaviors, or social determinants of health.

### 2.4 Primary Diagnosis Patterns
**Research Question:** What is the distribution of primary diagnoses among readmitted patients?

**Findings:**
- **ICD-9 codes 428 and 414 are the most frequent primary diagnoses** among readmitted patients
- Code 428: Heart failure conditions
- Code 414: Coronary atherosclerosis and other heart disease
- These cardiovascular conditions represent major comorbidities in diabetic patients

**Clinical Significance:** The prevalence of cardiovascular diagnoses among readmitted patients highlights the importance of integrated diabetes-cardiovascular care management.

### 2.5 Healthcare Utilization Patterns
**Research Question:** How do the number of lab procedures or medications relate to readmission probability?

**Statistical Analysis:**
- **Lab Procedures:** t-test revealed significant difference (p = 5.33×10⁻³⁶)
- **Medications:** t-test revealed significant difference (p = 2.15×10⁻⁵⁰)
- **Correlation Analysis:** Weak positive correlation between readmission and both lab procedures (r ≈ 0.04) and medications (r ≈ 0.05)

**Findings:**
- Patients who are readmitted have significantly higher average numbers of lab procedures and medications during their initial stay
- While statistically significant, the correlation is weak, suggesting these are markers of patient complexity rather than direct causal factors

**Clinical Significance:** Higher healthcare utilization may indicate more complex patients who require intensive monitoring and care coordination to prevent readmissions.

---

## 3. Statistical Analysis

### 3.1 Medication Change Impact (Chi-Square Test)
**Hypothesis:** Is there a statistically significant difference in readmission rates between patients who had their diabetes medication changed during admission and those who did not?

**Statistical Test:** Chi-square test of independence
- **Null Hypothesis:** No association between medication changes and readmission rates
- **Alternative Hypothesis:** Association exists between medication changes and readmission rates

**Results:**
- **Chi-square statistic:** Highly significant (p = 1.36×10⁻⁴⁷)
- **Conclusion:** Reject H₀ → Significant evidence that medication changes affect readmission rates

### 3.2 Intervention Effect Size (Odds Ratio Analysis)
**Research Question:** What is the confidence interval for readmission rates before and after medication changes?

**Statistical Method:** Odds Ratio calculation with 95% confidence intervals

**Results:**
- **Odds Ratio:** 1.20 (95% CI: 1.17–1.23)
- **Interpretation:** Patients whose diabetes medication was changed during hospitalization had 1.2 times higher odds of readmission compared to those without medication changes

**Clinical Significance:** While the effect is modest, it suggests that medication changes during admission may indicate clinical instability or require adjustment periods that increase short-term readmission risk.

### 3.3 Comorbidity Impact Analysis
**Research Question:** Is there a significant difference in readmission rates between patients with and without comorbidities?

**Statistical Test:** Chi-square test followed by odds ratio calculation
- **Chi-square result:** Highly significant (p = 1.89×10⁻¹⁵)
- **Odds Ratio:** 3.00 (95% CI: 2.26–3.98)

**Findings:**
- **Patients with comorbidities had 3 times higher odds of readmission** compared to those without
- This represents the strongest risk factor identified in our analysis

**Clinical Significance:** Comorbidity management is critical for readmission prevention. Patients with multiple conditions require comprehensive care coordination and enhanced discharge planning.

### 3.4 Medication Change Risk Assessment (Relative Risk)
**Research Question:** Does changing diabetes medication during admission affect readmission risk?

**Statistical Method:** Relative Risk calculation with 95% confidence intervals

**Results:**
- **Relative Risk:** 1.10 (95% CI: 1.09–1.12)
- **Interpretation:** Changing diabetes medication during admission was associated with a 10% higher risk of readmission

**Clinical Significance:** While the relative increase is modest, the precision of the estimate (narrow confidence interval) and statistical significance suggest this is a real, clinically relevant effect that should inform medication management protocols.

### 3.5 Demographic Risk Factor Analysis
**Research Question:** Which patient demographic factors are most strongly associated with higher readmission rates?

**Statistical Method:** Chi-square tests for each demographic factor

**Results:**
- **Age:** Highly significant association (p < 0.05, highest chi-square statistic)
- **Gender:** Significant association (p < 0.05)
- **Race:** Significant association (p < 0.05)

**Findings:**
- **Age group exhibits the strongest association** with readmission risk
- All three demographic factors are significantly associated with readmission rates
- Age is the most influential demographic predictor

**Clinical Significance:** Age-stratified interventions may be most effective, with enhanced resources allocated to older patient populations. Gender and racial disparities also require attention in care delivery models.

---

## 4. SQL Analysis Summary

The SQL component of this analysis focused on efficient data aggregation and complex queries to identify patterns across large datasets. Key SQL operations included:

- **Department-level readmission rate calculations** adjusted for age groups
- **Medication combination analysis** among readmitted patients
- **Insurance type impact assessment** on readmission patterns
- **Diagnosis-specific readmission rate calculations**

These queries enabled rapid analysis of subgroup patterns and supported the statistical findings presented above.

---

## 5. Key Insights and Clinical Implications

### 5.1 Primary Risk Factors (Ranked by Effect Size)
1. **Comorbidities** (OR = 3.00) - Strongest predictor
2. **Age** - Most influential demographic factor
3. **Medication Changes** (RR = 1.10) - Modest but significant effect
4. **Gender** - Females at higher risk
5. **Race** - Significant disparities exist

### 5.2 Protective Factors
- **Specific Medications:** Metformin, Glipizide, Pioglitazone, Rosiglitazone
- **Appropriate Length of Stay:** Current discharge timing appears well-calibrated

### 5.3 Healthcare Utilization Markers
- Higher lab procedures and medications indicate patient complexity
- These serve as early warning indicators for readmission risk

---

## 6. Recommendations for Reducing Readmissions

### 6.1 Immediate Actions (High Impact)
1. **Enhanced Comorbidity Management**
   - Implement comprehensive care coordination for patients with multiple conditions
   - Develop integrated care pathways for diabetes-cardiovascular patients
   - Target ICD-9 codes 428 (heart failure) and 414 (coronary disease) for specialized protocols

2. **Age-Stratified Interventions**
   - Allocate additional resources for patients over 60
   - Implement geriatric-focused discharge planning
   - Enhance post-acute care coordination for elderly patients

### 6.2 Medication Management Protocols
1. **Optimize Diabetes Medication Selection**
   - Consider preferential use of Metformin, Glipizide, Pioglitazone, and Rosiglitazone when clinically appropriate
   - Develop evidence-based medication selection guidelines

2. **Medication Change Protocols**
   - Implement enhanced monitoring for patients with medication changes during admission
   - Develop transition-of-care protocols for medication adjustments
   - Consider delayed discharge or enhanced follow-up for patients with medication changes

### 6.3 Targeted Population Health Initiatives
1. **Gender-Specific Interventions**
   - Develop targeted programs addressing higher female readmission rates
   - Investigate underlying causes of gender disparities

2. **Health Equity Initiatives**
   - Address racial disparities in readmission rates
   - Implement culturally competent care delivery models

### 6.4 Quality Improvement Monitoring
1. **Risk Stratification Tools**
   - Develop predictive models incorporating identified risk factors
   - Implement real-time risk scoring during admission

2. **Performance Metrics**
   - Monitor readmission rates by risk factor categories
   - Track intervention effectiveness over time

---

## 7. Limitations and Future Research

### 7.1 Study Limitations
- **Temporal Scope:** Data from 1999-2008 may not reflect current practice patterns
- **Single Disease Focus:** Limited to diabetic patients
- **Observational Design:** Cannot establish causality for identified associations

### 7.2 Future Research Directions
1. **Validation Studies:** Replicate findings in contemporary datasets
2. **Intervention Trials:** Test effectiveness of targeted interventions
3. **Cost-Effectiveness Analysis:** Evaluate economic impact of recommendations
4. **Machine Learning Models:** Develop predictive algorithms for real-time risk assessment

---

## 8. Conclusion

This comprehensive analysis of hospital readmission patterns among diabetic patients provides evidence-based insights for healthcare quality improvement. The identification of comorbidities as the strongest risk factor (3x increased odds) and age as the most influential demographic predictor offers clear targets for intervention. The modest but significant effects of medication changes and specific medication types provide actionable guidance for clinical practice.

The statistical rigor of our analysis, combining exploratory data analysis with hypothesis testing, provides confidence in these findings. Implementation of the recommended interventions, particularly enhanced comorbidity management and age-stratified care protocols, has the potential to significantly reduce hospital readmissions and improve patient outcomes.

Healthcare administrators should prioritize resource allocation toward high-risk populations identified in this analysis, while maintaining focus on medication optimization and comprehensive discharge planning. The integration of these findings into clinical decision support systems and quality improvement initiatives represents a data-driven approach to reducing preventable readmissions.

---

**Report Prepared By:** Hospital Risk Analysis Team  
**Date:** January 2025  
**Dataset Source:** UCI Machine Learning Repository - Diabetes 130-US Hospitals Dataset  
**Analysis Tools:** Python (pandas, scipy, statsmodels), SQL, Statistical Analysis
