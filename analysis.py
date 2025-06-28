import ucimlrepo
import numpy as np
import pandas as pd

# fetch data for the first runtime
def fetchDataset() -> ucimlrepo.dotdict:
      # fetch dataset 
      diabetes_130_us_hospitals_for_years_1999_2008 = ucimlrepo.fetch_ucirepo(id=296)
      return diabetes_130_us_hospitals_for_years_1999_2008

# analyizing total null values in the dataset
def nullChecker(df: pd.DataFrame) -> pd.Series:
      return df.isna().sum()


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
      df['race'] = df['race'].astype('category')
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
      df['weight'] = df['weight'].astype('category')
      df['age'] = df['age'].astype('category')
      # now we drop all the medicine-related cols 
      medication_columns = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride',
                        'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone',
                        'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide',
                        'examide', 'citoglipton', 'glyburide-metformin', 'glipizide-metformin',
                        'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone']
      
      df.drop(columns=medication_columns, inplace=True)
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
      df['discharge_disposition_id'] = df['discharge_disposition_id'].map(discharge_disposition_ranked).astype('category')
      print(df.info())
      # now we check the admission_source_id:
      print(sorted(list(df['admission_source_id'].unique())))










      
      


