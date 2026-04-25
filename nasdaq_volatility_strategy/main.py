import util
from nasdaq_volatility_strategy import etl as etl
from nasdaq_volatility_strategy import characteristics as cha
from nasdaq_volatility_strategy import portfolio as pf
import pandas as pd

def portfolio_main(tickers, start, end, cha_name, ret_freq_use, q):
    """
    Run the full volatility-based portfolio construction pipeline.
    """
    dict_ret = etl.aj_ret_dict(tickers, start, end)

    df_cha = cha.cha_main(dict_ret, cha_name,  ret_freq_use)

    df_portfolios = pf.pf_main(df_cha, cha_name, q)

    util.color_print('Portfolio Construction All Done!')

    return dict_ret, df_cha, df_portfolios

def get_avg(df: pd.DataFrame, year):
    """
    Calculate the average value of each column for a selected year.
    """
    df = df.sort_index()
    ret = df.loc[f"{year}-01-01":f"{year}-12-31", :]
    avg_ret = ret.mean(skipna=True)
    return avg_ret

def get_cumulative_ret(df):
    """
    Calculate buy-and-hold cumulative returns for portfolio return series.
    """
    if not isinstance(df.index, pd.PeriodIndex):
        raise ValueError("DataFrame index must be PeriodIndex.")

    growth_factors = df + 1
    cumulative_product = growth_factors.prod(axis=0, skipna=True)
    cumulative_return = cumulative_product - 1

    return cumulative_return

def t_stat(EW_LS_pf_df):
    """
    Calculate mean return, t-statistic, and sample size for the long-short portfolio.
    """
    ls = EW_LS_pf_df["ls"].dropna()

    ls_bar = round(ls.mean(), 4)
    ls_t = round(ls.mean()/(ls.std(ddof=1) / (len(ls) ** 0.5)), 4)
    n_obs = len(ls)
    df = pd.DataFrame(data=[[ls_bar, ls_t, n_obs]], index=["ls"], columns=["ls_bar", "ls_t", "n_obs"])
    return df


