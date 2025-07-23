# Imports
import io
import time
import matplotlib
import ucimlrepo
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.contingency_tables import Table2x2
# region Functions
#================================/

def fetchDataset() -> ucimlrepo.dotdict:
      # fetch dataset 
      diabetes_130_us_hospitals_for_years_1999_2008 = ucimlrepo.fetch_ucirepo(id=296)
      return diabetes_130_us_hospitals_for_years_1999_2008

def nullChecker(df: pd.DataFrame) -> pd.Series:
      return df.isna().sum()

def changeColsType(df: pd.DataFrame, columns:list, type: str) -> pd.DataFrame:
      df.astype({col: type for col in columns})
      
def timingDecorator(func):
      def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            st.text(f"|{func.__name__} took {end - start} seconds to run|")
            return result
      return wrapper

@timingDecorator
def calcMedicationPerReadmissionRate():
      return df.groupby(['readmitted'])[medication_columns].\
            apply(lambda x : x.apply(pd.Series.value_counts).sum()).\
      sort_values(by=medication_columns, ascending=True).reset_index()


@timingDecorator
def plotStackedBarPlot(id_vars: str, value_vars: list, var_name: str, value_name: str) -> matplotlib.pyplot:
      colCounts = df.melt(id_vars=id_vars, value_vars=value_vars, 
                  var_name=var_name, value_name=value_name)
      medCounts = colCounts[colCounts[value_name] != 'No']  
      plotData = medCounts.groupby([var_name, id_vars]).size().reset_index(name='count')
      plt.figure(figsize=(16, 6))
      sns.barplot(data=plotData, x=var_name, y='count', hue=id_vars)
      plt.xticks(rotation=90)
      plt.title(f'{var_name} Usage by {id_vars}')
      plt.tight_layout()
      return plt

@timingDecorator
def calcTimePerReadmission():
      return df.groupby(['readmitted']).\
      agg({"time_in_hospital": 'mean'}).\
      sort_values(by="time_in_hospital", ascending=False)

@timingDecorator
def plotBoxPlot(x: str, y: str, dataFrame: pd.DataFrame) -> matplotlib.pyplot:
      plt.figure(figsize=(16, 6))
      sns.boxplot(data=dataFrame, x=x, y=y, hue='readmitted')
      plt.xticks(rotation=90)
      plt.title(f'boxplot of {y} per {x} status')
      plt.tight_layout()
      return plt

@timingDecorator
def removeOutliers(colName: str, dataFrame: pd.DataFrame) -> pd.DataFrame:
      q1 = dataFrame[colName].quantile(0.25)
      q3 = dataFrame[colName].quantile(0.75)
      IQR = q3 - q1
      lowerBound = q1 - 1.5 * IQR
      upperBound = q3 + 1.5 * IQR
      return dataFrame[(dataFrame[colName] >= lowerBound) &  (dataFrame[colName] <= upperBound)]

@timingDecorator
def calcAgePerReadmissionRate() -> pd.DataFrame:
      df['was_readmitted'] = df['readmitted'].isin(['<30', '>30'])
      return df.groupby('age')['was_readmitted'].mean().reset_index()

@timingDecorator
def calcGenderPerReadmissionRate() -> pd.DataFrame:
      df['was_readmitted'] = df['readmitted'].isin(['<30', '>30'])
      return df.groupby('gender')['was_readmitted'].mean().reset_index()

@timingDecorator
def calcRacePerReadmissionRate() -> pd.DataFrame:
      df['was_readmitted'] = df['readmitted'].isin(['<30', '>30'])
      return df.groupby('race')['was_readmitted'].mean().reset_index()

@timingDecorator
def plotBarPlot(x: str, y:str, dataFrame:pd.DataFrame) -> matplotlib.pyplot:
      sns.barplot(data=dataFrame, x=x, y=y)
      plt.ylabel(y)
      plt.xlabel(x)
      plt.title(f'Bar plot of {y} per {x}')
      plt.tight_layout()
      return plt

@timingDecorator
def calcDiag1PerReadmissionRate() -> pd.DataFrame:
      return df.groupby('was_readmitted')['diag_1'].value_counts().reset_index().\
      sort_values(by='count', ascending=False)
      
@timingDecorator
def calcReadmittedOnlyPerLab() -> pd.DataFrame:
      return df.groupby('was_readmitted')['num_lab_procedures'].mean().\
      reset_index(name='mean').sort_values(by="mean", ascending=False)

@timingDecorator
def calcReadmittedOnlyPerMed() -> pd.DataFrame:
      return df.groupby('was_readmitted')['num_medications'].mean().\
      reset_index(name='mean').sort_values(by="mean", ascending=False)

@timingDecorator
def contingencyPlot(contingencyTable: pd.DataFrame, xLabel: str, yLabel: str, title: str) -> matplotlib.pyplot:
      contingencyTable.plot(kind='bar', figsize=(8,6))
      plt.xlabel(xLabel)
      plt.ylabel(yLabel)
      plt.title(title)
      plt.tight_layout()
      return plt

@timingDecorator
def calculateOddsRatio(colOne:str, colTwo:str) -> None:
      table = pd.crosstab(df[colOne], df[colTwo])
      st.dataframe(table)
      table_2x2 = Table2x2(table)
      odds_ratio = table_2x2.oddsratio
      ci_low, ci_high = table_2x2.oddsratio_confint()
      st.subheader(f"Odds Ratio: {odds_ratio:.2f} [{ci_low:.2f}, {ci_high:.2f}]")

@timingDecorator
def calculateRelativeRisk(cont_table):
            # For you current format:
            a = cont_table.loc[True, 'Ch']    # Readmitted + change
            b = cont_table.loc[False, 'Ch']   # Not readmitted + change
            c = cont_table.loc[True, 'No'] # Readmitted + no change
            d = cont_table.loc[False, 'No']# Not readmitted + no change
            
            risk_change = a / (a + b)
            risk_nochange = c / (c + d)
            rr = risk_change / risk_nochange
            
            # Calculate 95% CI
            log_rr = np.log(rr)
            se = np.sqrt((1/a) - (1/(a+b)) + (1/c) - (1/(c+d)))
            ci_low = np.exp(log_rr - 1.96*se)
            ci_high = np.exp(log_rr + 1.96*se)
            
            return rr, (ci_low, ci_high)

# region Main     
if __name__ == "__main__":
      # region preprocessing
      # -----------------------------------------------------------------------------
      st.title("Diabetes 130-US Hospitals for Years 1999-2008 Data cleaning EDA\n_____________________________________")
      st.subheader("The main DataFrame before any modification:")
      df = pd.read_csv('data/diabetic_data.csv')
      st.dataframe(df)
      
      st.subheader("The dataFrame head:")
      st.dataframe(df.head())
      
      st.subheader("Checking null values in the DataFrame:")
      st.dataframe(nullChecker(df))
      
      st.text("From the null checking we can conclude that the two main cols with missing vals are A1Cresult,"
              "max_glu_serum, we shall exmaine them seperately.")
      st.text("max_glu_serum, A1Cresult values count:")
      st.dataframe(df[['max_glu_serum', 'A1Cresult']].value_counts())
      
      st.text("max_glu_serum unique values:")
      st.dataframe(df['max_glu_serum'].unique())
      
      st.text("A1Cresult unique values:")
      st.dataframe(df['A1Cresult'].unique())
      
      st.subheader("replace nan values with 'untested'")
      df.replace({'max_glu_serum': {np.nan : "untested"}, 'A1Cresult': {np.nan: "untested"}}, inplace=True)
      
      st.subheader("we are done dealing with the null values, We move on to check other columns and their values")
      st.text("__________________________________________________________________________________")
      
      buffer = io.StringIO()
      df.info(buf=buffer)
      s = buffer.getvalue()
      st.text(s)
      st.text("__________________________________________________________________________________")
      st.subheader("we check the gender column as it's type is object and since it's categorical data we should change to to categories, same for races")
      st.text("Gender column unique values:")
      st.dataframe(df['gender'].unique())
      df['gender'] = df['gender'].astype('category')
      
      st.text("Race Column values count:")
      st.dataframe(df['race'].value_counts())
      
      st.text("we notice that we got '?' among the categories so we replace it with 'Other' and change the the type of the column to cateogry")
      df.replace({'race': {'?': 'Other'}}, inplace=True)
      
      st.text("Now we move on to checking the uniqueness of both the visit id and all values are unique so we move on.")
      df['encounter_id'].nunique()
      
      st.subheader("we move on to the admission_type_id to check it") 
      st.dataframe(df['admission_type_id'].unique())
      st.dataframe(df[df['admission_type_id'] == 8]['diag_1'].head(10))
      
      st.text("we discover an important fact and it's as the admission type is ordered by ranking from least dangerous eg."
              "rank : '1' to life threating admission eg. rank 8 based on the diag_1 col where the ICD-9 codes refer to "
              " the medical diagonsis based on a code system on checking this values we find that admission_id with high ranks such 8 is diagnosed with "
              " life-threating diseases so we map the values from 1 to 8 as the following:")
      admissionTypes = {1: 'referral from clinic', 2: 'pyschiatric emergency', 3: 'minor care',
                         4: 'non-urgent', 5: 'semi-urgent', 6:'urgent', 7: 'emergent', 8: 'resuscitation'}
      df['admission_type_id'] = df['admission_type_id'].map(admissionTypes).astype('category')
      st.text("admission_type_id column unique values after mapping values:")
      st.dataframe(df['admission_type_id'].unique())
      
      st.subheader("now we replace the '?' from the weights with not-recorded as it's more informative and we change"
      " both types to categorical")
      df.replace({'weight': {'?': 'not-recorded'}}, inplace=True)
      
      medication_columns = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride',
                        'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone',
                        'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide',
                        'examide', 'citoglipton', 'glyburide-metformin', 'glipizide-metformin',
                        'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone']
      
      st.subheader("Now we move on to the analysis of the discharge_disposition_id column")
      st.text(sorted(list(df['discharge_disposition_id'].unique())))
      
      st.text("# so we knew those values ranging from 1 to 29 representing the degree of the disposition so we generated a "
              " list with values matching from 1 to 29 and we are going to do the same thing we did with adimission type")
      discharge_disposition_ranked = {
            29: "29-Home(RoutineDischarge)",
            28: "28-HomeWithHomeHealthServices",
            27: "27-HomeWithSelfCareAssistance",
            26: "26-HomeHospice",
            25: "25-OutpatientRehabilitation",
            24: "24-PhysiciansOfficeFollowUp",
            23: "23-SkilledNursingFacility(ShortTerm)",
            22: "22-AssistedLivingFacility",
            21: "21-PsychiatricFacility(Voluntary)",
            20: "20-SubstanceAbuseTreatment",
            19: "19-LongTermAcuteCareHospital",
            18: "18-InpatientRehabilitationFacility",
            17: "17-SkilledNursingFacility(LongTerm)",
            16: "16-HospiceFacility",
            15: "15-PsychiatricFacility(Involuntary)",
            14: "14-FederalHealthcareFacility",
            13: "13-PrisonJail",
            12: "12-GroupHome",
            11: "11-BoardAndCareHome",
            10: "10-IntermediateCareFacility",
            9: "9-LeftAgainstMedicalAdvice",
            8: "8-Expired(DiedInHospital)",
            7: "7-HomelessShelter",
            6: "6-UnknownNoFixedAddress",
            5: "5-AcuteCareHospitalTransfer",
            4: "4-StillPatient(DischargePending)",
            3: "3-Morgue",
            2: "2-ForensicCustodialFacility",
            1: "1-Nowhere(AbandonedUnclaimed)"
            }
      
      st.subheader("now, we will check the diag_1 in coresponse with discharged_position")
      st.dataframe(df[df['admission_type_id'] == 'resuscitation'][['diag_1', 'discharge_disposition_id']].head(20))
      df['discharge_disposition_id'] = df['discharge_disposition_id'].map(discharge_disposition_ranked)
      
      st.subheader("now we check the admission_source_id and map values:")
      st.text(sorted(list(df['admission_source_id'].unique())))
      st.dataframe(df[df['admission_type_id'] == 'resuscitation'][['diag_1', 'admission_source_id']].head(20))
      st.dataframe(df['discharge_disposition_id'].unique())
      admission_source_ranked = {
            # Top 5 Common Sources
            1: "1-EmergencyRoom",
            2: "2-PhysicianReferral",
            3: "3-TransferFromAcuteCareHospital",
            4: "4-TransferFromSNF",
            5: "5-ClinicReferral",
            
            # Mid-Tier Sources
            6: "6-HMOReferral",
            7: "7-Court/LawEnforcement",
            8: "8-Birth(Newborn)",
            9: "9-Other",
            10: "10-Unknown",
            11: "11-HomeHealthCare",
            12: None,  # Gap
            
            # Special Cases
            13: "13-Readmission",
            14: "14-InterhospitalTransfer",
            15: None,  # Gap
            16: None,  # Gap
            17: "17-NormalDelivery",
            18: None,  # Gap
            19: None,  # Gap
            20: "20-PrematureDelivery",
            21: None,  # Gap
            22: "22-Hospice",
            23: None,  # Gap
            24: None,  # Gap
            
            # Rare Cases
            25: "25-InternationalTransfer"}                
      df['admission_source_id'] = df['admission_source_id'].map(admission_source_ranked)
      st.subheader("now, we will check the addmission_source_id column after remapping")
      st.dataframe(df['admission_source_id'].unique())
      
      st.subheader("Now we check the time hospital column, conclusion we move on it doesn't need anything.")
      st.dataframe(df['time_in_hospital'].unique())
      
      st.subheader("Now we check payer_code column, conclusion it does have the '?' which we will replace with others:")
      df.replace({"payer_code": {'?': 'Others'}}, inplace=True)
      st.dataframe(df['payer_code'].unique())
      
      st.subheader("now we we check the medical_specialty column, conclusion same as payer_code:")
      df.replace({"medical_specialty" : {'?': 'Others'}}, inplace=True)
      st.dataframe(df['medical_specialty'].unique())
      
      st.subheader("now we check the numerical values [from col:12 to col:17], conculsion: Nothing unsual.")
      st.text(df.iloc[:, 12: 18].nunique())
      
      st.subheader("the diag_1, diag_2, diag_3 are object types we change them to categorical per columns description "
      "the number_diagnoses column is the same as cols from 12 to 17, we move to max_glu_serum col:")
      st.subheader("changing all columns with categorical features all once at a time, any column not mentioned above"
      "doesn't have any problem just it was wrong typed as object and changed to 'category'")
      df['max_glu_serum'] = df['max_glu_serum'].astype('category')
      changeColsType(df=df, columns=['race', 'gender', 'age', 'weight', 'admission_type_id',
                                      'discharge_disposition_id', 'admission_source_id', 'payer_code',
                                      'medical_specialty', 'diag_1', 'diag_2', 'diag_3', 'max_glu_serum',
                                        'A1Cresult', 'insulin', 'change', 'diabetesMed', 'readmitted'],
                                        type='category')
      # endregion
      # -----------------------------------------------------------------------------
      # region analysis
      # -----------------------------------------------------------------------------
      st.header("Now to answer the questions on task one:")
      st.subheader("1 - Which medications are most associated with lower readmission rates ?")
      st.dataframe(calcMedicationPerReadmissionRate())
      st.text("Plotting the result:")
      st.pyplot(plotStackedBarPlot(id_vars='readmitted', value_vars=medication_columns,
                                   var_name='medication', value_name='status'),clear_figure=True, use_container_width=False)
      st.subheader("Based on the chart, Metformin, Glipizide, Pioglitazone, and Rosiglitazone appear to be the medications"
                   "most associated with lower hospital readmission rates.")

      st.subheader("2 - How does length of stay (time_in_hospital) affect readmission risk ?")
      st.dataframe(calcTimePerReadmission())
      st.text("Plotting the result:")
      st.pyplot(plotBoxPlot(x='readmitted', y='time_in_hospital', dataFrame=df), clear_figure=True)
      st.text("since it seems there are outliers, let's remove them and see the plots again")
      timeHospitalNoOutliersDf = removeOutliers(colName='time_in_hospital', dataFrame=df)
      st.pyplot(plotBoxPlot(x='readmitted', y='time_in_hospital', dataFrame=timeHospitalNoOutliersDf), clear_figure=True)
      st.subheader("final conclusion : Length of stay does not appear to be strongly associated with" 
      " readmission status in this dataset.")

      st.subheader("3 - Are there differences in readmission rates by age group or gender ?")
      st.dataframe(calcAgePerReadmissionRate())
      st.dataframe(calcGenderPerReadmissionRate())
      # Plot the readmission rate by age group
      st.pyplot(plotBarPlot(x='age', y='was_readmitted', dataFrame=calcAgePerReadmissionRate()), clear_figure=True)
      st.pyplot(plotBarPlot(x='gender', y='was_readmitted', dataFrame=calcGenderPerReadmissionRate()), clear_figure=True)
      st.subheader("The likelihood of being readmitted to the hospital increases with patient age, "
      "especially for those over 60, Females have a higher readmission rate than males.")  

      st.subheader("4 - What is the distribution of primary diagnoses (diag_1) among readmitted patients ?")
      st.dataframe(calcDiag1PerReadmissionRate())
      pltData = calcDiag1PerReadmissionRate()[calcDiag1PerReadmissionRate()['was_readmitted']].head(10)
      pltData['diag_1'] = pltData['diag_1'].astype(str).str.strip()
      st.pyplot(plotBarPlot(x='diag_1', y='count', dataFrame=pltData), clear_figure=True)
      st.subheader("Final conclusion 428, 414 are the most diagnosis per readmitted patients")

      st.subheader("5 - How do the number of lab procedures or medications relate to readmission probability ?")
      readmittedOnlyPerLab = calcReadmittedOnlyPerLab()
      readmittedOnlyPerMed = calcReadmittedOnlyPerMed()

      st.dataframe(readmittedOnlyPerLab)
      st.dataframe(readmittedOnlyPerMed)

      plt.figure(figsize=(12, 10))  
      sns.barplot(data=readmittedOnlyPerLab, y='was_readmitted', x='mean', orient='h')
      plt.xlabel('Readmission Counts')
      plt.ylabel('Number of procedures mean')
      plt.title('Number of procedures mean Vs Readmission Rate')
      plt.yticks(fontsize=10)
      st.pyplot(plt, clear_figure=True) 
      plt.figure(figsize=(12, 10))  
      sns.barplot(data=readmittedOnlyPerMed, y='was_readmitted', x='mean', orient='h')
      plt.xlabel('Readmission Counts')
      plt.ylabel('Number of Medications mean')
      plt.title('Number of Medications mean Vs Readmission Rate')
      plt.yticks(fontsize=10)  
      plt.tight_layout()
      st.pyplot(plt, clear_figure=True)
      st.subheader("statisical test (t test)")
      trueReadmPerLabProcedures = df[df['was_readmitted'] == True]['num_lab_procedures']
      st.dataframe(trueReadmPerLabProcedures)
      falseReadmPerLabProcedures = df[df['was_readmitted'] == False]['num_lab_procedures']
      tStatistic, pValue = stats.ttest_ind(trueReadmPerLabProcedures, falseReadmPerLabProcedures)
      st.text("T-Stat: {} pValue: {}".format(tStatistic, pValue))
      st.subheader(" p-value = 5.3321e-36 which is smaller than significance value (0.05) which means There is a statistically"
      " significant difference in the average number of lab procedures between readmitted and non-readmitted patients."
      " This suggests that the number of lab procedures is associated with readmission probability in your dataset.")
      trueReadmPerMediciation = df[df['was_readmitted'] == True]['num_medications']
      falseReadmPerMediciation = df[df['was_readmitted'] == False]['num_medications']
      tStatistic, pValue = stats.ttest_ind(trueReadmPerMediciation, falseReadmPerMediciation)
      st.text("T-Stat: {} pValue: {}".format(tStatistic, pValue))
      st.subheader(" p-value = 2.1451963e-50 which is smaller than significance value (0.05) which means There is a statistically"
      " significant difference in the average number of mediciations between readmitted and non-readmitted patients."
      " This suggests that the number of mediciations is associated with readmission probability in your dataset.")
      st.subheader("calcuating correlation between the three columns")
      correlationMatrix = df[['was_readmitted', 'num_medications', 'num_lab_procedures']].corr()
      st.text(correlationMatrix)
      plt.figure(figsize=(8, 6))
      sns.heatmap(correlationMatrix,annot=True,cmap='coolwarm',vmin=0.039253,vmax=1)
      plt.title("Correlation Heatmap")
      st.pyplot(plt)
      st.subheader(" based on the correlation matrix, there is a weak positive correlation between readmission"
      " and num of procedures pair and the readmission and num of medications")
      st.subheader("now the last thing is to plot the box plots of the values for each column")
      st.pyplot(plotBoxPlot(x='was_readmitted', y='num_lab_procedures', dataFrame=df), clear_figure=True)
      st.subheader("Boxplot for num_medications by readmission status")
      st.pyplot(plotBoxPlot(x='was_readmitted', y='num_medications', dataFrame=df), clear_figure=True)
      # endregion
      # -----------------------------------------------------------------------------
      # region statisical analysis
      # -----------------------------------------------------------------------------
      st.header("Statisical Questions:")
      st.subheader("Q1: Is there a statistically significant difference in readmission"
                   " rates between patients who had their diabetes medication changed during admission and"
                   "those who did not?")
      st.subheader("statisical test (chi-square test)")
      st.text("null hypothesis: there is a no association between readmission rate and mediciation change")
      st.text("alternative hypothesis: there is an association between readmission rate and mediciation change")
      df['readmitted'] = df['readmitted'].map({">30": "Yes", "<30": "Yes", "NO": "No"})
      contingencyTable = pd.crosstab(df['readmitted'], df['change'])
      st.dataframe(contingencyTable)
      chi2, pValue, dof, expected = stats.chi2_contingency(contingencyTable)
      st.text("chi2:{}, p-values: {}, dof: {}".format(chi2, pValue, dof))
      st.subheader("Conclusion: Since p-val: 1.362060823556665e-47, Reject H₀ → Significant evidence that medication changes affect readmission rates.")
      st.pyplot(contingencyPlot(contingencyTable, 'Readmission Status', 'Number of Patients', 'Readmission Status by Medication Change'))
      
      st.subheader("Q2: What is the confidence interval for readmission rates before and after a specific intervention (e.g., medication change)?")
      st.text("I will use Odds Ratio (OR) (for retrospective/case-control studies).")
      subset = contingencyTable.loc[['Yes', 'No'], :]
      table = Table2x2(subset.values)
      oddsratio = table.oddsratio
      ciLow, ciHigh = table.oddsratio_confint()
      st.subheader(f"Odds Ratio ('Yes', 'No'): {oddsratio:.2f} [{ciLow:.2f}, {ciHigh:.2f}]")
      st.subheader("Conclusion: Patients whose diabetes medication was changed during hospitalization had 1.2 times higher odds of"
                   " readmission compared to those without medication changes (OR = 1.20; 95% CI: 1.17–1.23). This association was statistically significant,"
                   " suggesting that medication changes may modestly increase the risk of readmission.")

      st.subheader("Q3: Is there a significant difference in readmission rates between patients with and without comorbidities")
      df['has_comorbidity'] = df.apply(
      lambda row: any(val != '?' for val in [row['diag_2'], row['diag_3']]),axis=1)
      st.dataframe(df[['diag_1', 'diag_2', 'diag_3', 'has_comorbidity']])
      st.dataframe(df['has_comorbidity'].value_counts())
      st.subheader("statisical test (chi-square test)")
      st.text("null hypothesis: there is a no association between readmission rate and comorbidities")
      st.text("alternative hypothesis: there is an association between readmission rate and comorbidities")
      contingencyTable = pd.crosstab(df['readmitted'], df['has_comorbidity'])
      st.dataframe(contingencyTable)
      chi2, pValue, dof, expected = stats.chi2_contingency(contingencyTable)
      st.text("chi2:{}, p-values: {}, dof: {}".format(chi2, pValue, dof))
      st.subheader("Since p-val: 1.8934145321376148e-15, Reject H₀ → Significant evidence that comorbidities affect readmission rates.")
      st.pyplot(contingencyPlot(contingencyTable, 'Readmission Status', 'Number of Patients', 'Readmission Status by comorbidities'), clear_figure=True)
      df['readmitted'] = df['readmitted'].map({'Yes': True, 'No': False})
      table = pd.crosstab(df['has_comorbidity'], df['readmitted'])
      st.dataframe(table)
      table_2x2 = Table2x2(table)
      odds_ratio = table_2x2.oddsratio
      ci_low, ci_high = table_2x2.oddsratio_confint()
      st.subheader(f"Odds Ratio: {odds_ratio:.2f} [{ci_low:.2f}, {ci_high:.2f}]")
      st.subheader("Conclusion: Patients with comorbidities had 3 times higher odds of readmission compared to those without (OR = 3.00; 95% CI: 2.26–3.98).")
      st.subheader("Q4: Does changing diabetes medication during admission affect readmission risk ?")
      contingencyTable = pd.crosstab(df['readmitted'], df['change'])
      st.dataframe(contingencyTable)
      rr, ci = calculateRelativeRisk(cont_table=contingencyTable)
      st.subheader(f"Relative Risk: {rr:.2f} [95% CI: {ci[0]:.2f}, {ci[1]:.2f}]")
      st.subheader("Conclusion: Changing diabetes medication during admission was associated with a" 
                   " 10'%' higher risk of readmission (RR = 1.10, 95% CI: 1.09–1.12, p < 0.001). This effect was statistically significant and"
                   " clinically relevant, suggesting that medication changes may modestly increase readmission likelihood") 
      
      
      st.subheader("Q5: Which patient demographic factors (such as age group, gender, or race) are most strongly associated with higher readmission rates?")
      st.dataframe(df[['age', 'gender', 'race', 'readmitted']])
      st.subheader("statisical test (chi-square test)")
      st.text("null hypothesis: there is a no association between readmission rate and age/gender/race")
      st.text("alternative hypothesis: there is an association between readmission rate and age/gender/race")
      contingencyTableAge = pd.crosstab(df['readmitted'], df['age'])
      st.dataframe(contingencyTableAge)
      contingencyTableGender = pd.crosstab(df['readmitted'], df['gender'])
      st.dataframe(contingencyTableGender)
      contingencyTableRace = pd.crosstab(df['readmitted'], df['race'])
      st.dataframe(contingencyTableRace)
      AgeChi2, AgePValue, AgeDof, AgeExpected = stats.chi2_contingency(contingencyTableAge)
      GenChi2, GenPValue, GenDof, GenExpected = stats.chi2_contingency(contingencyTableGender)
      RaceChi2, RacePValue, RaceDof, RaceExpected = stats.chi2_contingency(contingencyTableRace)
      st.text("Age, chi2:{}, p-values: {}, dof: {}".format(AgeChi2, AgePValue, AgeDof))
      st.pyplot(contingencyPlot(contingencyTableAge, 'Readmission Status', 'Number of Patients', 'Readmission Status by Age'))
      st.text("Gender, chi2:{}, p-values: {}, dof: {}".format(GenChi2, GenPValue, GenDof))
      st.pyplot(contingencyPlot(contingencyTableGender, 'Readmission Status', 'Number of Patients', 'Readmission Status by Gender'))
      st.text("Race, chi2:{}, p-values: {}, dof: {}".format(RaceChi2, RacePValue, RaceDof))
      st.pyplot(contingencyPlot(contingencyTableRace, 'Readmission Status', 'Number of Patients', 'Readmission Status by Race'))
      st.subheader("Since all p-values are less than our siginficance value (0.05),"
                   " Reject H₀ → Significant evidence that age/gender/race affect readmission rates.")
      st.subheader("Conclusion: Our analysis shows that age group, gender, and race are all significantly associated with hospital "
                   "readmission rates (p < 0.05 for each, chi-square test). Among these factors, age group exhibits the " 
                   "strongest association with readmission, as indicated by the highest chi-square statistic. "
                   "This suggests that patient age is the most influential demographic factor for predicting readmission " 
                   "risk in this dataset, followed by race and gender. Targeted interventions for higher-risk age groups "
                   "may be most effective in reducing readmissions.")
# endregion
# ----------------------------------------------------------------------------------


      
            
      

            

      
      


      


      

      



      
















      
      


