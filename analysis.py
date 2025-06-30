import ucimlrepo
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# fetch data for the first runtime
def fetchDataset() -> ucimlrepo.dotdict:
      # fetch dataset 
      diabetes_130_us_hospitals_for_years_1999_2008 = ucimlrepo.fetch_ucirepo(id=296)
      return diabetes_130_us_hospitals_for_years_1999_2008

# analyizing total null values in the dataset
def nullChecker(df: pd.DataFrame) -> pd.Series:
      return df.isna().sum()

# changing group of cols type 
def changeColsType(df: pd.DataFrame, columns:list, type: str) -> None:
      for column in columns:
            df[column] = df[column].astype(type)

if __name__ == "__main__":
      df = pd.read_csv('data/diabetic_data.csv')
      print(df.head())
      print(nullChecker(df))
      # from the null checking we can conclude that the two main cols with missing vals are
      # A1Cresult, max_glu_serum, we shall exmaine them seperately.
      print(df[['max_glu_serum', 'A1Cresult']].value_counts())
      print(df['max_glu_serum'].unique())
      print(df['A1Cresult'].unique())
      # replace nan values with untested
      df.replace({'max_glu_serum': {np.nan : "untested"}, 'A1Cresult': {np.nan: "untested"}}, inplace=True)
      print(df['max_glu_serum'].unique())
      print(df['A1Cresult'].unique())
      # we are done dealing with the null values, We move on to check other columns and their values
      print(df.info())
      # we check the gender column as it's type is object and since it's categorical data we should
      # change to to categories, same for races
      print(df['gender'].unique())
      df['gender'] = df['gender'].astype('category')
      print(df['race'].value_counts())
      # we notice that we got '?' among the categories so we replace it with 'Other' and change the 
      # the type of the column to cateogry
      df.replace({'race': {'?': 'Other'}}, inplace=True)
      # Now we move on to checking the uniqueness of both the visit id
      print(df.shape[0])
      print(df['encounter_id'].nunique())
      # we move on to the admission_type_id to check it 
      print(df['admission_type_id'].unique())
      print(df[df['admission_type_id'] == 8]['diag_1'].head(10))
      # we discover an important fact and it's as the admission type is ordered by ranking from 
      # least dangerous eg. rank : '1' to life threating admission eg. rank 8 based on the diag_1
      # col where the ICD-9 codes refer to the medical diagonsis based on a code system 
      # on checking this values we find that admission_id with high ranks such 8 is diagnosed with 
      # life-threating diseases so we map the values from 1 to 8 as the following:
      admissionTypes = {1: 'referral from clinic', 2: 'pyschiatric emergency', 3: 'minor care',
                         4: 'non-urgent', 5: 'semi-urgent', 6:'urgent', 7: 'emergent', 8: 'resuscitation'}
      df['admission_type_id'] = df['admission_type_id'].map(admissionTypes).astype('category')
      print(df['admission_type_id'].unique())
      # We shall now check the age, weight columns
      print(df['age'].unique())
      print(df['weight'].unique())
      # now we replace the '?' from the weights with not-recorded as it's more informative and we change
      # both types to categorical
      df.replace({'weight': {'?': 'not-recorded'}}, inplace=True)
      # now we drop all the medicine-related cols 
      medication_columns = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride',
                        'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone',
                        'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide',
                        'examide', 'citoglipton', 'glyburide-metformin', 'glipizide-metformin',
                        'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone']
      
      # df.drop(columns=medication_columns, inplace=True)
      print(df.info())
      # Now we move on to the analysis of the discharge_disposition_id column
      print(sorted(list(df['discharge_disposition_id'].unique())))
      # so we knew those values ranging from 1 to 29 representing the degree of the disposition 
      # so we generated a list with values matching from 1 to 29 and we are going to do the same thing
      # we did with adimission type
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
      # now, we will check the diag_1 in coresponse with discharged_position
      print(df[df['admission_type_id'] == 'resuscitation'][['diag_1', 'discharge_disposition_id']].head(20))
      df['discharge_disposition_id'] = df['discharge_disposition_id'].map(discharge_disposition_ranked)
      print(df.info())
      # now we check the admission_source_id and map values:
      print(sorted(list(df['admission_source_id'].unique())))
      print(df[df['admission_type_id'] == 'resuscitation'][['diag_1', 'admission_source_id']].head(20))
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
    25: "25-InternationalTransfer"
}
      df['admission_source_id'] = df['admission_source_id'].map(admission_source_ranked)
      print(df.info())
      # now we check the time hospital column, conclusion we move on it doesn't need anything:
      print(df['time_in_hospital'].unique())
      # now we check payer_code column, conclusion it does have the '?' which we will replace with other:
      df.replace({"payer_code": {'?': 'Others'}}, inplace=True)
      print(df['payer_code'].unique())
      # now we we check the medical_specialty column, conclusion same as payer_code:
      df.replace({"medical_specialty" : {'?': 'Others'}}, inplace=True)
      print(df['medical_specialty'].unique())
      # now we check the numerical values [from col:12 to col:17], conculsion: good to go !
      print(df.iloc[:, 12: 18].nunique())
      # the diag_1, diag_2, diag_3 are object types we change them to categorical per columns description
      # the number_diagnoses column is the same as cols from 12 to 17, we move to max_glu_serum col:
      print(df['max_glu_serum'].unique())
      # changing all columns with categorical features all once at a time, any column not mentioned above
      # doesn't have any problem just it was wrong typed as object and changed to 'category'
      df['max_glu_serum'] = df['max_glu_serum'].astype('category')
      changeColsType(df=df, columns=['race', 'gender', 'age', 'weight', 'admission_type_id',
                                      'discharge_disposition_id', 'admission_source_id', 'payer_code',
                                      'medical_specialty', 'diag_1', 'diag_2', 'diag_3', 'max_glu_serum',
                                        'A1Cresult', 'insulin', 'change', 'diabetesMed', 'readmitted'],
                                        type='category')
      print(df.info())
      # Now to answer the questions on task one:
      # 1 - Which medications are most associated with lower readmission rates ?
      print(df['readmitted'].unique())
      medperAdm = df.groupby(['readmitted'])[medication_columns].\
            apply(lambda x : x.apply(pd.Series.value_counts).sum()).\
      sort_values(by=medication_columns, ascending=True).reset_index()
      print(medperAdm)

      # plotting the result 
      medCounts = df.melt(id_vars='readmitted', value_vars=medication_columns, 
                     var_name='medication', value_name='status')
      print(medCounts['status'].unique())
      medCounts = medCounts[medCounts['status'] != 'No']  
      plotData = medCounts.groupby(['medication', 'readmitted']).size().reset_index(name='count')
      print(plotData)

      plt.figure(figsize=(16, 6))
      sns.barplot(data=plotData, x='medication', y='count', hue='readmitted')
      plt.xticks(rotation=90)
      plt.title('Medication Usage by Readmission Status')
      plt.tight_layout()

      # 2 - How does length of stay (time_in_hospital) affect readmission risk ?
      print(df['time_in_hospital'].unique())
      timePerReadmission = df.groupby(['readmitted']).\
      agg({"time_in_hospital": 'mean'}).\
      sort_values(by="time_in_hospital", ascending=False)
      print(timePerReadmission)

      # plotting the result
      plt.figure(figsize=(16, 6))
      sns.boxplot(data=df, x='readmitted', y='time_in_hospital', hue='readmitted')
      plt.xticks(rotation=90)
      plt.title('boxplot of hours per readmittion status')
      plt.tight_layout()

      # since it seems there are outliers, let's remove them and see the plots again
      q1 = df['time_in_hospital'].quantile(0.25)
      q3 = df['time_in_hospital'].quantile(0.75)
      IQR = q3 - q1
      lowerBound = q1 - 1.5 * IQR
      upperBound = q3 + 1.5 * IQR

      timeHospitalNoOutliersDf = df[(df['time_in_hospital'] >= lowerBound) & 
                                  (df['time_in_hospital'] <= upperBound)]
      plt.figure(figsize=(16, 6))
      sns.boxplot(data=timeHospitalNoOutliersDf, x='readmitted', 
                  y='time_in_hospital', hue='readmitted')
      plt.xticks(rotation=90)
      plt.title('boxplot of hours per readmittion status with no outliers')
      plt.tight_layout()
      # plt.show()
      # final conclusion : Length of stay does not appear to be strongly associated with 
      # readmission status in this dataset.

      # 3 - Are there differences in readmission rates by age group or gender ?
      df['was_readmitted'] = df['readmitted'].isin(['<30', '>30'])

      ageReadmitRate = df.groupby('age')['was_readmitted'].mean().reset_index()
      genderReadmitRate = df.groupby('gender')['was_readmitted'].mean().reset_index()

      # Plot the readmission rate by age group
      fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))
      sns.barplot(data=ageReadmitRate, x='age', y='was_readmitted', ax=axes[0, 0])
      axes[0, 0].set_ylabel('Readmission Rate')
      axes[0, 0].set_xlabel('Age Group')
      axes[0, 0].set_title('Readmission Rate by Age Group')
      sns.barplot(data=genderReadmitRate, x='gender', y='was_readmitted', ax=axes[0, 1])
      axes[0, 1].set_ylabel('Readmission Rate')
      axes[0, 1].set_xlabel('Gender Group')
      axes[0, 1].set_title('Readmission Rate by Gender Group')
      plt.tight_layout()
      plt.show()

      # The likelihood of being readmitted to the hospital increases with patient age, 
      # especially for those over 60, Females have a higher readmission rate than males.   

      # 4 - What is the distribution of primary diagnoses (diag_1) among readmitted patients ?
      
      
      


      


      

      



      
















      
      


