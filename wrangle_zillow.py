import acquire, prepare

def handle_missing_values(df):
    '''
    Function handles missing values. If columns has missing values over 60%, and rows over 75% that column and row
    will be dropped.
    '''
    
    prop_required_column = float(input('Enter % of cols to drop: '))
    prop_required_row = float(input('Enter % of rows to drop: '))
    
    threshold = int(round(prop_required_column * len(df.index),0))
    df.dropna(axis = 1, thresh=threshold, inplace = True)
    threshold = int(round(prop_required_row * len(df.columns),0))
    df.dropna(axis = 0, thresh = threshold, inplace = True)
    return df


def single_family_properties():
    
    '''
    This function creates single property homes. 
    room count < 10
    bed count < 6
    
    '''
    
    df = prepare.prepare_zillow()
    
    df = df[(df.property_land_use_desc == 'Single Family Residential') & (df.room_count <= 10.0) & (df.bed_count <= 6.0)]
    
    return df
    
    