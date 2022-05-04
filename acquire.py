import pandas as pd
import env
import os
from pydataset import data
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def db_conn():

    db = 'zillow'

    url = f'mysql+pymysql://{env.username}:{env.password}@{env.host}/{db}'

    return url


def get_zillow(use_cache=True):

    zillow_file = 'zillow.csv'

    if os.path.exists(zillow_file) and use_cache:

        print('Status: Acquiring data from cached csv file..')

        return pd.read_csv(zillow_file)

    qry = '''
         SELECT prop17.*, pred17.logerror, pred17.transactiondate, 
             tct.typeconstructiondesc, st.storydesc, plt.propertylandusedesc, 
             hst.heatingorsystemdesc, bct.buildingclassdesc, ast.architecturalstyledesc, 
             act.airconditioningdesc

         FROM properties_2017 prop17

         LEFT JOIN predictions_2017 pred17 USING(parcelid)

         LEFT JOIN unique_properties up USING(parcelid)

         LEFT JOIN typeconstructiontype tct USING(typeconstructiontypeid)
         LEFT JOIN storytype st USING(storytypeid)
         LEFT JOIN propertylandusetype plt USING(propertylandusetypeid)
         LEFT JOIN heatingorsystemtype hst USING(heatingorsystemtypeid)
         LEFT JOIN buildingclasstype bct USING(buildingclasstypeid)
         LEFT JOIN architecturalstyletype ast USING(architecturalstyletypeid)
         LEFT JOIN airconditioningtype act USING(airconditioningtypeid)

         WHERE (prop17.parcelid = up.parcelid) AND (

               (prop17.latitude IS NOT NULL) AND (prop17.longitude IS NOT NULL)
               
               );
    
          '''

    print('Status: Acquiring data from SQL database..')

    zillow = pd.read_sql(qry, db_conn())

    print('Status: Saving zillow data locally..')

    zillow.to_csv(zillow_file, index=False)


def missing_rows_count_percentage(df):

    # This function returns number of rows missing and their percentage

    data = pd.DataFrame({
        'row_count': df.isna().sum(),
        'row_percent': df.isna().mean(),
    })

    return data


def zillow_missing_columns_rows_percent_cols(df):
    # This function returns number of missing columns, rows and percent of columns missing

    data = pd.concat([

        df.isna().sum(axis=1).rename('n_missing_cols'),
        df.isna().mean(axis=1).rename('percent_missing_cols'),
    ], axis=1).value_counts().sort_index()

    return data


def get_iris_data():

    df = data('iris')

    # rename columns
    df = df.rename(columns={'Sepal.Length': 'sepal_length', 'Sepal.Width': 'sepal_width', 'Petal.Length': 'petal_length', 'Petal.Width': 'petal_width',
                            'Species': 'species'})

    return df


def db_conn2():

    db = 'mall_customers'

    url = f'mysql+pymysql://{env.username}:{env.password}@{env.host}/{db}'

    return url


def get_mall_data(use_cache=True):

    mall_file = 'mall.csv'

    if os.path.exists(mall_file) and use_cache:

        print('Status: Acquiring data from cached csv file..')

        return pd.read_csv(mall_file)

    qry = 'SELECT * FROM customers;'

    print('Status: Acquiring data from SQL database..')

    mall = pd.read_sql(qry, db_conn2())

    print('Status: Saving zillow data locally..')

    mall.to_csv(mall_file, index=False)


def scale_mall():

    scaler = MinMaxScaler()

    df = get_mall_data()
    
    df = df.drop(columns=['gender', 'customer_id'])

    df[['scaled_age', 'scaled_annual_income',
                'scaled_spending_score']] = scaler.fit_transform(df[['age', 'annual_income', 'spending_score']])

    return df
