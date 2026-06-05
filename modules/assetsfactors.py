# %%
# calculate assets key factors
import pandas as pd
import numpy as np

# %%
def assetsFactors(series):
    '''
    function to calculate asset market factors and upload in dataframe
    df['Min'] - minimum value in historical series
    df['Max'] - minimum value in historical series
    df['Ret%'] - return in percentage of the historical series
    df['Risk%'] - risk (standard deviation) in perdentage of the historical series
    df['Beta']- beta related to market index
    args:
    series - [type]: [pandas.core.frame.DataFrame]
    returns
    [type]: [pandas.core.frame.DataFrame]
    '''

    # CAGR – Compound Annual Growth Rate - calculation
    series = series.dropna()

    # adding Min column
    df = series.min().to_frame(name='min')
    df['min'] = df['min'].round(2)

    # index naming
    df.index.name = 'ticker'

    # adding Max column
    df['max'] = series.max()
    df['max'] = df['max'].round(2)

    # market percentage historic return
    # CAGR – Compound Annual Growth Rate calculation
    if len(series) < 2:
      return np.nan
    totalreturn = series.iloc[-1] / series.iloc[0] - 1
    n_days = len(series) - 1
    # annualizes to 252 working days per year.
    annualreturn = (1 + totalreturn) ** (252 / n_days) - 1
    df['returnHist'] = annualreturn.mul(100) # converts to %
    df['returnHist'] = df['returnHist'].round(1)

    # calculate daily variation
    seriesvar = series.pct_change()
    # Market risk calculation, in percentage (%). Add column in output dataframes
    risk = seriesvar.std()*np.sqrt(252)*100
    df['risk'] = risk.round(0)

    # market return variance calculation
    seriesvariance = seriesvar.var()*252
    # covariance calculation
    seriescovariance = seriesvar.cov()*252
    # reference index
    indexes = ['SP500','USRT','XFIX11','IBOV']
    index = 'IBOV' # residual value
    for column in series.columns:
      if column in indexes:
          index = column
          break  # breaks at the first match
    # beta calculation
    beta = seriescovariance[index]/seriesvariance[index]
    df['beta'] = beta.round(2)

    # Organizing columns order and making Index column as index of dataframes
    df = df.reset_index()

    # return dataframe
    return df


