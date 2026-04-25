import util
import sys
import numpy as np
import pandas as pd

def vol_input_sanity_check(ret, cha_name, ret_freq_use: list):
    """
    Validate inputs for volatility factor calculation.

    Parameters
    ----------
    ret : dict
        Dictionary containing daily and monthly return DataFrames.
    cha_name : str
        Characteristic name, such as 'vol'.
    ret_freq_use : list
        Return frequency used for characteristic calculation.
    """
    keys = {"Daily", "Monthly"}
    if not isinstance(ret, dict) or set(ret.keys()) != keys:
        return sys.exit("The input file, `ret`, must be a dictionary with two keys: 'Daily' and 'Monthly'.")

    if not isinstance(cha_name, str):
        return sys.exit("`cha_name` must be a string")

    function_name = cha_name + "_cal"
    if function_name not in globals() or not callable(globals()[function_name]):
        return sys.exit("{} must be an existing function to calculate the characteristic.".format(function_name))

    if not isinstance(ret_freq_use, list) or not set(ret_freq_use).issubset(keys):
        return sys.exit("`ret_freq_use` must be a list containing 'Daily', 'Monthly', both or blank.")

    return util.color_print('Sanity checks for inputs of characteristics script passed.')

def vol_cal(ret, cha_name, ret_freq_use: list):
    """
    Calculate monthly volatility factor for each stock.

    Volatility is measured as the standard deviation of daily returns within each month.
    A month is included only if it has at least 18 valid daily return observations.

    Parameters
    ----------
    ret : dict
        Dictionary containing daily and monthly return DataFrames.
    cha_name : str
        Characteristic name used as column suffix.
    ret_freq_use : list
        Return frequency used for volatility calculation.

    Returns
    -------
    pandas.DataFrame
        Monthly volatility factor table indexed by year-month.
    """
    daily = ret[ret_freq_use[0]].copy()
    daily.index = pd.to_datetime(daily.index)
    daily.index = daily.index.to_period('M')
    vol_dict = {}
    for col in daily.columns:
        monthly_vol = daily[col].groupby(daily.index).agg(
            lambda x: x.std() if x.count() >= 18 else np.nan
        )
        vol_dict[col + f'_{cha_name}'] = monthly_vol
    df_vol = pd.DataFrame(vol_dict)
    df_vol = df_vol.dropna(how='all')
    df_vol.index.name = 'Year_Month'
    return df_vol

def merge_tables(ret, df_cha, cha_name):
    """
    Merge monthly returns with lagged characteristic factors.

    The characteristic values are shifted by one period to avoid look-ahead bias,
    ensuring that only past information is used for return prediction.

    Parameters
    ----------
    ret : dict
        Dictionary containing return DataFrames.
    df_cha : pandas.DataFrame
        DataFrame of characteristic factors.
    cha_name : str
        Name of the characteristic.

    Returns
    -------
    pandas.DataFrame
        Merged dataset of monthly returns and lagged characteristics.
    """
    monthly = ret['Monthly'].copy()
    df_cha = df_cha.copy()
    df_cha = df_cha.shift(1)
    df_m = pd.merge(monthly, df_cha, how='left', left_index=True, right_index=True)
    df_m = df_m.rename_axis('Date')
    return df_m

def cha_main(ret, cha_name, ret_freq_use: list):
    """
    Run the characteristic construction pipeline.

    Steps:
    1. Validate input return datasets
    2. Calculate monthly volatility factor
    3. Merge monthly returns with lagged factor values

    Parameters
    ----------
    ret : dict
        Dictionary containing daily and monthly return DataFrames.
    cha_name : str
        Characteristic name, such as 'vol'.
    ret_freq_use : list
        Return frequency used for factor calculation.

    Returns
    -------
    pandas.DataFrame
        Monthly return and lagged characteristic dataset.
    """
    vol_input_sanity_check(ret, cha_name, ret_freq_use)
    df_cha = vol_cal(ret, cha_name, ret_freq_use)
    df_m = merge_tables(ret, df_cha, cha_name)
    return df_m
