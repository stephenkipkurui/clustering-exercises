import acquire
from acquire import get_zillow
import pandas as pd
import numpy as np
import datetime

import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


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
    df = get_zillow()
        
    # Renaming cols for readability
    df = df.rename(columns = ({'id':'id', 'parcelid':'parcel_id',
                               'airconditioningtypeid':'air_cond_id',
                               'architecturalstyletypeid': 'architect_style_id',
                               'basementsqft':'basement_sqft', 
                               'bathroomcnt':'bath_count', 'bedroomcnt':'bed_count', 
                               'buildingclasstypeid':'building_class_id',
                               'buildingqualitytypeid':'building_quality_id', 
                               'calculatedbathnbr':'calc_bath_n_bed', 
                               'decktypeid':'deck_id',
                               'finishedfloor1squarefeet':'finished_floor_1_sqft',
                               'calculatedfinishedsquarefeet':'calc_finished_sqft',
                               'finishedsquarefeet12':'finished_sqft_12', 
                               'finishedsquarefeet13':'finished_sqft_13',
                               'finishedsquarefeet15':'finished_sqft_15',
                               'finishedsquarefeet50':'finished_sqft_50',
                               'finishedsquarefeet6':'finished_sqft_6', 'fips':'fips', 
                               'fireplacecnt':'fireplace_count','fullbathcnt':'full_bath_count', 
                               'garagecarcnt':'garage_car_count', 
                               'garagetotalsqft':'garage_total_sqft', 
                               'hashottuborspa':'has_hot_tub_or_spa',
                               'heatingorsystemtypeid':'heating_or_system_id', 'latitude':'latitude', 
                               'longitude':'longitude', 
                               'lotsizesquarefeet':'lot_size_sqft','poolcnt':'pool_count', 
                               'poolsizesum':'pool_size_sum', 
                               'pooltypeid10':'pool_id_10','pooltypeid2':'pool_id_2',
                               'pooltypeid7':'pool_id_7',
                               'propertycountylandusecode':'property_county_land_use_code', 
                               'propertylandusetypeid':'property_land_use_id',
                               'propertyzoningdesc':'property_zoning_desc',
                               'rawcensustractandblock':'raw_census_tract_and_block', 
                               'regionidcity':'region_id_city','regionidcounty':'region_id_county', 
                               'regionidneighborhood':'region_id_neighborhood', 
                               'regionidzip':'region_id_zip', 
                               'roomcnt':'room_count','storytypeid':'story_id', 
                               'threequarterbathnbr':'three_quarter_bath_n_br', 
                               'typeconstructiontypeid':'construction_id',
                               'unitcnt':'unit_count', 'yardbuildingsqft17':'yard_bldg_sqft_17', 
                               'yardbuildingsqft26':'yar_bldg_sqft_26', 'yearbuilt':'year_built',
                               'numberofstories':'num_stories', 'fireplaceflag':'fire_place_flag', 
                               'structuretaxvaluedollarcnt':'structure_tax_value',
                               'taxvaluedollarcnt':'tax_value', 'assessmentyear':'assessment_year', 
                               'landtaxvaluedollarcnt':'land_tax_value',
                               'taxamount':'tax_amount', 'taxdelinquencyflag':'tax_delinquency_flag', 
                               'taxdelinquencyyear':'tax_delinquency_year',
                               'censustractandblock':'census_tract_and_block', 
                               'logerror':'log_error', 
                               'transactiondate':'transaction_date',
                               'typeconstructiondesc':'construction_desc', 'storydesc':'story_desc', 
                               'propertylandusedesc':'property_land_use_desc',
                               'heatingorsystemdesc':'heating_or_system_desc', 
                               'buildingclassdesc':'bldg_class_desc', 
                               'architecturalstyledesc':'architect_style_desc',
                               'airconditioningdesc':'air_con_desc'}))
    
#         # Drop nulls                       
    df['log_error'] = df.log_error.dropna()
    
#     # Drop duplicate columns
#     df = df.drop_duplicates()

    # Reset index
    df = df.reset_index(drop = True)
    
    return df

# def impute_zillow():
    
#     df = prepare_zillow()
    
#     df['centra_ac_imputed'] = df.air_con_desc == 'Central'
    
#     return, df



def split_zillow(df):
    
    # Splits into train, validate and test
    
    train_validate, test = train_test_split(df, test_size=0.2, random_state=123)
    
    train, validate = train_test_split(train_validate, test_size=0.2, random_state=123)
    
    return train, validate, test
    
    
def scale_zillow(train, validate, test):
    
    columns_to_scale = ['census_tract_and_block']
    
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    scaler = MinMaxScaler()
    scaler.fit(train[columns_to_scale])
    
    train_scaled[columns_to_scale] = scaler.transform(train[columns_to_scale])
    validate_scaled[columns_to_scale] = scaler.transform(validate[columns_to_scale])
    test_scaled[columns_to_scale] = scaler.transform(test[columns_to_scale])
    
    return train_scaled, validate_scaled, test_scaled


def get_exploration_data():
    
    df = prepare_zillow()
    
    train, validate, test = split_zillow(df)
    
    return train

def get_modeling_data(scale_data = False):
    
    df = get_zillow()
    
#     df = one_hot_encode(df)
    
    train, validate, test = split(df)
    
    if scale_data:
        
        return scale(train, validate, test)
    
    else:
        
        return train, validate, 
   

# def single_unit_homes():
    
#     df = prepare_zillow()
        
#     single_units =  df[(df.bed_count < 4) & (df.calc_finished_sqft <= 5000)]

#     null_single_units = single_units[single_units.unit_count.isna() == True]
    
#     return null_single_units


def cols_nulls(df):
    
    data = pd.DataFrame({'cols_null_count': df.isna().sum(),
                        'cols_null_percent': df.isna().mean()
                        })

    return data

def rows_nulls(df):
    
    data = pd.concat([df.isna().sum(axis =1).rename('num_missing_values'),
                      df.isna().mean(axis = 1).rename('percent_missing_values'), 
                     ], axis = 1).value_counts().sort_index()
    return data
    

# def handle_missing_values(df, prop_required_column, prop_required_row):
    
#     cols_null_percent = df.isna().mean()
#     rows_null_percent = df.isna().mean(axis = 1)

#     return df
