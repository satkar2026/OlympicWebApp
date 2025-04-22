import pandas as pd
import numpy as np


def preprocess(df,region):
    #filtering summer omplyics
    df = df[df['Season'] == 'Summer']
    #merge with region_df
    df = df.merge(region,on='NOC',how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding medal
    df =pd.concat([df, pd.get_dummies(df['Medal'])],axis=1)
    return df