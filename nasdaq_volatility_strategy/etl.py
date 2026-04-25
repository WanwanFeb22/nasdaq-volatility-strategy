import config as cfg
import yfinance as yf
import pandas as pd
import os

def download_prc_to_csv(start, end, tickers=cfg.TICKERS):
    """
    Download historical price data for selected tickers and save each ticker as a CSV file.

    Parameters
    ----------
    start : str
        Start date in YYYY-MM-DD format.
    end : str
        End date in YYYY-MM-DD format.
    tickers : list
        List of stock tickers to download.

    Returns
    -------
    None
        CSV files are saved to the configured data directory.
    """
    for i in tickers:
        df = yf.download(i, start=start, end=end, auto_adjust=False, multi_level_index=False)
        if df.empty:
            print(f"No data found for {i}. Skipping...")
            continue
        df.reset_index(inplace=True)
        filename = f"{i.lower()}_prc.csv"
        pth = os.path.join(cfg.DATADIR, filename)
        df.to_csv(pth, index=False)

def read_prc_csv(tic, start, end, prc_col='Adj Close'):
    """
    Load adjusted price data for a given ticker from CSV.

    Parameters
    ----------
    tic : str
        Stock ticker.
    start : str
        Start date (YYYY-MM-DD).
    end : str
        End date (YYYY-MM-DD).
    prc_col : str, optional
        Column name for price data (default: 'Adj Close').

    Returns
    -------
    pandas.Series
        Time series of adjusted prices indexed by date.
    """
    filename = f"{tic.lower()}_prc.csv"
    pth = os.path.join(cfg.DATADIR, filename)
    df = pd.read_csv(pth, index_col='Date', parse_dates=True)
    ser = df[prc_col].dropna()
    ser = ser.loc[start:end]
    ser.name = tic.lower()
    return ser

def daily_return_cal(prc):
    """
    Compute daily returns from a price series.

    Parameters
    ----------
    prc : pandas.Series
        Time series of adjusted prices.

    Returns
    -------
    pandas.Series
        Daily return series (percentage change), with NaN values removed.
    """
    ret = prc.pct_change()
    ret = ret.dropna()
    ret.name = prc.name
    return ret

def monthly_return_cal(prc):
    """
    Compute monthly returns from a daily adjusted price series.

    A month is included only if it has at least 18 valid trading-day observations.

    Parameters
    ----------
    prc : pandas.Series
        Daily adjusted price series.

    Returns
    -------
    pandas.Series
        Monthly return series indexed by year-month.
    """
    to_period = prc.to_period('M')
    condition = to_period.groupby(to_period.index).count() >= 18
    resample = prc.resample('ME').last().to_period('M')
    resample = resample.pct_change()
    resample = resample[condition]
    resample = resample.dropna()
    resample.index.name = 'Year_Month'
    return resample

def aj_ret_dict(tickers, start, end):
    """
       Build daily and monthly return datasets for a list of tickers.

       Pipeline:
       1. Download historical price data
       2. Compute daily returns
       3. Compute monthly returns
       4. Combine into DataFrames

       Parameters
       ----------
       tickers : list
           List of stock tickers.
       start : str
           Start date (YYYY-MM-DD).
       end : str
           End date (YYYY-MM-DD).

       Returns
       -------
       dict
           {
               "Daily": DataFrame of daily returns,
               "Monthly": DataFrame of monthly returns
           }
       """
    end_included = (pd.to_datetime(end) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    download_prc_to_csv(start=start, end=end_included, tickers=tickers)
    daily_returns = {}
    monthly_returns = {}
    for tic in tickers:
        tic_lower = tic.lower()
        try:
            prc = read_prc_csv(tic, start, end)
            daily_ret = daily_return_cal(prc)
            monthly_ret = monthly_return_cal(prc)
            daily_returns[tic_lower] = daily_ret
            monthly_returns[tic_lower] = monthly_ret
        except FileNotFoundError:
            print(f"Price file for {tic} not found. Skipping...")
        except Exception as e:
            print(f"Error processing {tic}: {e}. Skipping...")
    daily_df = pd.concat(daily_returns.values(), axis=1)
    daily_df.columns = daily_returns.keys()
    daily_df.index.name = 'Date'

    monthly_df = pd.concat(monthly_returns.values(), axis=1)
    monthly_df.columns = monthly_returns.keys()
    monthly_df.index.name = 'Year_Month'
    return {
        "Daily": daily_df,
        "Monthly": monthly_df
    }

