import pandas as pd
import env
import os

def db_conn():
    
    db = 'zillow'
    
    url = f'mysql+pymysql://{env.username}:{env.password}@{env.host}/{db}'
        
    return url


def get_zillow(use_cache = True):
    
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

               (latitude IS NOT NULL) AND (longitude IS NOT NULL)
               
               );
    
          '''
    
    print('Status: Acquiring data from SQL database..')
    
    zillow = pd.read_sql(qry, db_conn())
    
    print('Status: Saving zillow data locally..')
    
    zillow.to_csv(zillow_file, index = False)
    
    
    