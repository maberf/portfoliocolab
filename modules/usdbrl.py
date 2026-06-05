# %%
import pandas as pd
import numpy as np

# %%
# Portfolio daframe in BRL
# Multiply USA assets by USDBRL value (BRL quotation)
#
def usdToBrl (dfport, df):
    '''
    function to convert USD prices to BRL
    dfport - portfolio dataframe with some columns USD quoted
    df - dataframe reference with all assets and their prices in USD
    the function converts in dfport the columns that correspond to assets in USD using USDBRL quotation column
    args:
    dfport - [type]: [pandas.core.frame.DataFrame]
    df - [type]: [pandas.core.frame.DataFrame]
    returns
    [type]: [pandas.core.frame.DataFrame]
    '''

    # Identifies dfport columns that correspond to assets in USD (ignores the exchange rate column).
    cols_a_converter = [c for c in dfport.columns if c != 'USDBRL' and c in df]

    # Performs the conversion (multiplies the price in USD by the USDBRL exchange rate line by line)
    for col in cols_a_converter:
    # multiplication aligns indices; preserves NaNs where they exist.
      dfport[col] = dfport[col].multiply(dfport['USDBRL'], axis=0)

    # Displayed result: which columns were converted and initial preview of dfport.
    if cols_a_converter:
        print(f"To BRL converted: {cols_a_converter}.")
    else:
        print("No existing columns to be converted.")

    # return dataframe
    return dfport


