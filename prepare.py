import acquire
from acquire import get_zillow
import pandas as pd
import numpy as np
import datetime

import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer



def remove_outliers(df, k, col_list):
    ''' this function take in a dataframe, k value, and specified columns 
    within a dataframe and then return the dataframe with outliers removed
    '''
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df
#---------------------


def prepare_zillow():
    
    # Acquire zilloW df from acquire module
    zillow = get_zillow()
        
    # Renaming cols for readability
    zillow = zillow.rename(columns = ({'bedroomcnt':'bed_count','bathroomcnt':'bath_count',
                                     'calculatedfinishedsquarefeet':'square_feet',
                                       'taxvaluedollarcnt':'assessed_value', 'fips':'fips',
                                       'yearbuilt':'year_built','transactiondate':'trans_date'}))
                           
    # Drop nulls                       
    zillow = zillow.dropna()
    
    # Drop duplicate columns
    zillow = zillow.drop_duplicates()

    # Reset index
    zillow = zillow.reset_index(drop = True)
    
    zillow['trans_date'] = pd.to_datetime(zillow['trans_date'], format = '%Y-%m-%d')
    
    zillow['trans_month'] = pd.to_datetime(zillow['trans_date']).dt.month
#---------------------

    # Apply a function to remove outliers
    zillow = remove_outliers(zillow, 2.7, ['bed_count', 'bath_count', 'square_feet', 
                                           'assessed_value','trans_month'])
    
    # Remove more of the outliers for sqft
    zillow = zillow[(zillow.square_feet > 500) & (zillow.square_feet < 2500)]
    
    # Remove more of the outliers for taxvalue
    zillow = zillow[(zillow.assessed_value > 500) & (zillow.assessed_value < 800000)]    
#---------------------
    
    train_validate, test = train_test_split(zillow, test_size=0.2, 
                                                random_state=123)
    
    train, validate = train_test_split(train_validate,
                                        test_size=0.3,
                                       random_state=123)

    # Function return
    return train, validate, test


        



  
    
  
    
    