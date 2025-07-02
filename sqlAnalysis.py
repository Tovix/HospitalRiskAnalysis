import psycopg2
import pandas as pd

# cleaning the data
def cleanDataForLoading(dataPath: str) -> None:
      expectedColumns = [
      'encounter_id', 'patient_nbr', 'race', 'gender', 'age',
      'admission_type_id', 'discharge_disposition_id', 'admission_source_id',
      'time_in_hospital', 'payer_code', 'weight',
      'medical_specialty', 'num_lab_procedures', 'num_procedures',
      'num_medications', 'number_outpatient', 'number_emergency',
      'number_inpatient', 'diag_1', 'diag_2', 'diag_3', 'number_diagnoses',
      'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide',
      'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide',
      'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol',
      'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin',
      'glyburide_metformin', 'glipizide_metformin', 'glimepiride_pioglitazone',
      'metformin_rosiglitazone', 'metformin_pioglitazone', 'change',
      'diabetesMed', 'readmitted'
      ]

      df = pd.read_csv(dataPath)
      print(df.columns)
      # Reorder and trim columns
      df = df[expectedColumns]
      # Replace '? with None (interpreted as NULL in SQL)
      df.replace('?', None, inplace=True)

# cleanDataForLoading("data/diabetes_cleaned.csv")


# Esablishing a connection
connection = psycopg2.connect(database="Hospital_Readmission_Risk",host="localhost",user="postgres",
                              password="postgres",port="5433")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS diabetes_hospital_data (
    encounter_id BIGINT PRIMARY KEY,
    patient_nbr BIGINT NOT NULL,
    race TEXT,
    gender TEXT,
    age TEXT,
    admission_type_id SMALLINT,
    discharge_disposition_id SMALLINT,
    admission_source_id SMALLINT,
    time_in_hospital SMALLINT,
    payer_code TEXT,
    weight TEXT,
    medical_specialty TEXT,
    num_lab_procedures SMALLINT,
    num_procedures SMALLINT,
    num_medications SMALLINT,
    number_outpatient SMALLINT,
    number_emergency SMALLINT,
    number_inpatient SMALLINT,
    diag_1 TEXT,
    diag_2 TEXT,
    diag_3 TEXT,
    number_diagnoses SMALLINT,
    max_glu_serum TEXT,
    A1Cresult TEXT,
    metformin TEXT,
    repaglinide TEXT,
    nateglinide TEXT,
    chlorpropamide TEXT,
    glimepiride TEXT,
    acetohexamide TEXT,
    glipizide TEXT,
    glyburide TEXT,
    tolbutamide TEXT,
    pioglitazone TEXT,
    rosiglitazone TEXT,
    acarbose TEXT,
    miglitol TEXT,
    troglitazone TEXT,
    tolazamide TEXT,
    examide TEXT,
    citoglipton TEXT,
    insulin TEXT,
    glyburide_metformin TEXT,
    glipizide_metformin TEXT,
    glimepiride_pioglitazone TEXT,
    metformin_rosiglitazone TEXT,
    metformin_pioglitazone TEXT,
    change TEXT,
    diabetesMed TEXT,
    readmitted TEXT);
""")

connection.commit()

# inserting all the values from our CSV file
def insertRecordsIntoTable(cursor) -> None:
      with open('data/diabetes_cleaned.csv', 'r') as f:
            next(f)  # Skip the header
            cursor.copy_expert("""
                  COPY diabetes_hospital_data FROM STDIN WITH CSV HEADER DELIMITER ','
            """, f)

# insertRecordsIntoTable(cursor=cursor)
cursor.execute('''
SELECT * FROM diabetes_hospital_data LIMIT 1
''')

rows = cursor.fetchall()
for row in rows:
      print(row)


# Which three departments (medical_specialty) have the highest readmission rates, adjusting for age groups ?
cursor.execute("""
SELECT
    medical_specialty,
    AVG(readmission_rate) AS avg_readmission_rate
FROM (
    SELECT
        medical_specialty,
        age,
        COUNT(CASE WHEN readmitted != 'NO' THEN 1 END)::float / COUNT(*) AS readmission_rate
    FROM
        diabetes_hospital_data
    WHERE
        medical_specialty IS NOT NULL
    GROUP BY
        medical_specialty, age
) AS rates_by_age
GROUP BY
    medical_specialty
ORDER BY
    avg_readmission_rate DESC
LIMIT 3;
""")

rows = cursor.fetchall()
for row in rows:
      print(row)
      
# the top 3 departments per readmission rate based on age groups 
# are Pediatrics-AllergyandImmunology, Dermatology and Pediatrics-InfectiousDiseases

#  What is the average length of stay for each readmission type and for each admission type?

cursor.execute("""
      SELECT
            readmitted,
            AVG(time_in_hospital)
      FROM 
            diabetes_hospital_data
      GROUP BY 
            readmitted
""")

rows = cursor.fetchall()
for row in rows:
      print(row)

cursor.execute("""
      SELECT
      admission_type_id,
      AVG(time_in_hospital)
      FROM 
      diabetes_hospital_data
      GROUP BY 
      admission_type_id
""")

rows = cursor.fetchall()
for row in rows:
      print(row)

# Which medication combinations are most common among readmitted patients?







# What is the readmission rate by insurance type (payer_code)?
# Which diagnoses (diag_1) are most frequently associated with readmissions?