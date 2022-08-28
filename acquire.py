import numpy as np
import os
import pandas as pd
from env import user, password, host

def get_url(db, user=user, password=password, host=host):
    '''
    take database name for input,
    returns url, using user, password, and host pulled from your .env file.
    PLEASE save it as a variable, and do NOT just print your credientials to your document.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# Pulling Telco Data

def get_telco_data():
    '''
    Returns the telco dataset, checks local disk for telco.csv, if present loads it,
    otherwise it pulls the data from SQL, joins customer, contract_types, payment_types, internet_service_types, and customer_churn tables,
    the customer_churn has date of customer churn, as not all customers have churned, there WILL be Null Values that require tidying up, Please be aware.
    '''
    filename = 'telco_churn.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql('''SELECT * FROM customers
        JOIN contract_types
        USING(contract_type_id)
        JOIN payment_types
        USING(payment_type_id)
        JOIN internet_service_types
        USING(internet_service_type_id)
        LEFT JOIN customer_churn
        USING(customer_id);''', get_url('telco_churn'))
        df.to_csv(filename)
        return df

# Sending column names to lists depending upon their data type (number, categorical)

def dtypes_to_list(df):
    '''
    Takes in a dataframe, returns two lists, 
    one of num type column names, and one of categorical type column names.
    '''
    num_type_list, cat_type_list = [], []
    for column in df:
        col_type =  df[column].dtype
        if col_type == "object" :
            cat_type_list.append(column)
        if np.issubdtype(df[column], np.number) and \
            ((df[column].max() + 1) / df[column].nunique())  == 1 :
            cat_type_list.append(column)
        if np.issubdtype(df[column], np.number) and \
            ((df[column].max() + 1) / df[column].nunique()) != 1 :
            num_type_list.append(column)
    return num_type_list, cat_type_list

# range of values in a column

def col_range(df):
    '''
    Takes in a data frame, returns the 'describe' of the data frame with a new entry 'range'.
    'Range' is the difference between the 'max' and 'min' columns.
    '''
    stats_df = df.describe().T
    stats_df['range'] = stats_df['max'] - stats_df['min']
    return stats_df