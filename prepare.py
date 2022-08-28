import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from acquire import dtypes_to_list
from pydataset import data
from sklearn.model_selection import train_test_split




def prep_telco(df):
    '''
    For the Telco DB:
    Drops the Foreign Key Columns: 'internet_service_type_id', 'contract_type_id', and 'payment_type_id', 
    Maps 'gender', 'partner', 'dependents', 'phone_service', 'paperless_billing', and 'churn' into columns with int values (Female and Yes mapped as 1, Male and No mapped to 0).
    Creates Dummy Columns for 'multiple_lines', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies', 'contract_type', 'internet_service_type',  'payment_type'
    Returns the Data Frame cleaned up
    '''
    df['gender_encoded'] = df.gender.map({'Female': 1, 'Male': 0})
    df['partner_encoded'] = df.partner.map({'Yes': 1, 'No': 0})
    df['dependents_encoded'] = df.dependents.map({'Yes': 1, 'No': 0})
    df['phone_service_encoded'] = df.phone_service.map({'Yes': 1, 'No': 0})
    df['paperless_billing_encoded'] = df.paperless_billing.map({'Yes': 1, 'No': 0})
    df['churn_encoded'] = df.churn.map({'Yes': 1, 'No': 0})
    
    dummy_df = pd.get_dummies(df[['multiple_lines',
                              'online_security',
                              'online_backup',
                              'device_protection',
                              'tech_support',
                              'streaming_tv',
                              'streaming_movies',
                              'contract_type',
                              'internet_service_type',
                              'payment_type'
                            ]],
                              drop_first=True)
    df = pd.concat( [df, dummy_df], axis=1 )
    df = df[df.total_charges != ' ']
    df['total_charges'] = df.total_charges.astype(float)
    df = df.drop(columns={'Unnamed: 0', 'gender', 'partner', 'dependents', 'phone_service', 'multiple_lines', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies', 'paperless_billing', 'churn', 'contract_type', 'payment_type', 'internet_service_type', 'churn_month'})
    df = df.rename(columns={'churn_encoded' : 'churn'})
    return df

# Splits data.

def data_split(df, target):
    '''
    Takes in a DataFrame and target column; returns train, validate, test DataFrames.
    Random State is set to the most generic '123'.
    '''
    train, test = train_test_split(df, test_size=.2, random_state=123, stratify=df[target])
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train[target])
    
    return train, validate, test

# Pulling Histogram Distribution of Numeric Columns

def num_dist(df):
  '''
  Takes in a DataFrame, returns a histogram of each numeric column.
  Uses the Acquire sheet function 'dtypes_to_list' to pull out numeric column names.
  '''
  num_type, cat_type = dtypes_to_list(df)
  for col in df.columns:
    if col in num_type:
      plt.hist(df[col])
      plt.title(f'column {col}')
      plt.show()

# spliting the split data into X and y

def split_X_y(df, target):
  '''
  Takes in a DataFrame and target, returns train, validate, and test as well as those three split into X and y (all columns except the target, and only the target column)
  Works like the data_split function, but goes further, spliting the train, validate, and test results.
  '''

  train, validate, test = data_split(df, target)
  X_train = train.drop(columns=[target])
  y_train = train[target]

  X_validate = validate.drop(columns=[target])
  y_validate = validate[target]
  X_test = test.drop(columns=[target])
  y_test = test[target]
  
  return train, validate, test, X_train, y_train, X_validate, y_validate, X_test, y_test