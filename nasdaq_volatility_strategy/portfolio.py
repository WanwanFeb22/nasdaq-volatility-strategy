
from nasdaq_volatility_strategy import etl
from nasdaq_volatility_strategy import characteristics as cha
import pandas as pd
import util
import sys


def pf_input_sanity_check(df_cha, cha_name):
    """
    Validate input data for portfolio construction.

    Ensures:
    - Monthly frequency index
    - Correct alignment between return columns and characteristic columns

    Parameters
    ----------
    df_cha : pandas.DataFrame
        DataFrame containing returns and lagged characteristics.
    cha_name : str
        Characteristic name (e.g., 'vol').
    """
    position = -len('_{}'.format(cha_name))

    cols = list(df_cha.columns)
    tics = [i for i in df_cha.columns if i.find('_{}'.format(cha_name)) == -1]
    tics.sort()

    tics_cha = list(set(cols) - set(tics))
    tics_cha = [i[:position] for i in tics_cha]
    tics_cha.sort()

    if not isinstance(cha_name, str):
        return sys.exit("`cha_name` must be a string")

    if df_cha.index.dtype == 'period[M]':
        print("df_cha table is in monthly frequency")
    else:
        sys.exit("Please make sure df_cha table is in monthly frequency")

    if tics_cha == tics:
        print("df_cha includes stocks' monthly returns and respective characteristics")
    else:
        sys.exit("Please make sure df_cha includes stocks' monthly returns and respective characteristics")

    return util.color_print('Sanity checks for inputs of long short portfolio construction passed')


def df_reshape(df_cha, cha_name):
    """
    Reshape the wide return-factor table into long format for portfolio sorting.

    Parameters
    ----------
    df_cha : pandas.DataFrame
        Wide table containing monthly returns and factor values.
    cha_name : str
        Characteristic name used for sorting.

    Returns
    -------
    pandas.DataFrame
        Long-format table with columns: Ret, factor value, and ticker.
    """
    tickers = [i for i in df_cha.columns if i.find('_{}'.format(cha_name)) == -1]
    df_collect = pd.DataFrame()

    for ticker in tickers:
        temp = df_cha[[ticker, ticker + '_{}'.format(cha_name)]]
        temp = temp.rename({'{}'.format(ticker): 'Ret',
                            '{}_{}'.format(ticker, cha_name): '{}'.format(cha_name)}, axis=1)
        temp['ticker'] = '{}'.format(ticker)
        df_collect = pd.concat([df_collect, temp], axis=0)

    df_reshaped = df_collect.copy()

    util.color_print('df_reshape function done')
    return df_reshaped


def stock_sorting(df_reshaped, cha_name, q):
    """
    Sort stocks into quantile portfolios based on a characteristic.

    Stocks are grouped by month and assigned to quantiles using the specified factor.
    This is a standard cross-sectional sorting step in factor investing.

    Parameters
    ----------
    df_reshaped : pandas.DataFrame
        Long-format table with returns, factor values, and ticker.
    cha_name : str
        Characteristic used for sorting.
    q : int
        Number of quantile groups.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional 'rank' column indicating quantile assignment.
    """
    df_reshaped.dropna(inplace=True)
    rank_ser = df_reshaped.groupby(level=0)['{}'.format(cha_name)]\
        .transform(lambda x: pd.qcut(x, q, labels=False, duplicates='drop')).rename('rank')
    df_sorted = pd.concat([df_reshaped, rank_ser], axis=1)
    df_sorted.dropna(inplace=True)

    util.color_print('stock_sorting function done')
    return df_sorted


def pf_cal(df_sorted, cha_name, q):
    """
    Construct equal-weighted quantile portfolios and a long-short portfolio.

    The long-short portfolio is defined as:
    high-characteristic portfolio return minus low-characteristic portfolio return.

    Parameters
    ----------
    df_sorted : pandas.DataFrame
        DataFrame containing monthly returns, factor values, ticker, and quantile rank.
    cha_name : str
        Characteristic used for sorting.
    q : int
        Number of quantile portfolios.

    Returns
    -------
    pandas.DataFrame
        Monthly returns of equal-weighted quantile portfolios and long-short portfolio.
    """
    portfolio_ret = df_sorted.groupby([df_sorted.index.name, 'rank'])['Ret']\
        .mean().to_frame('_ew').reset_index(level='rank')

    lst = []
    for i in range(q):
        temp = portfolio_ret[portfolio_ret['rank'] == float(i)]\
            .drop('rank', axis=1)\
            .rename({'_ew': 'ewp_rank_{}'.format(i+1)}, axis=1)

        lst += [temp]

    df = pd.concat(lst, axis=1)
    df['ls'] = df['ewp_rank_{}'.format(q)] - df['ewp_rank_1']

    util.color_print('pf_cal function done')
    return df


def pf_main(df_cha, cha_name, q):
    """
    Run the portfolio construction pipeline.

    Steps:
    1. Validate portfolio input data
    2. Reshape return-factor data into long format
    3. Sort stocks into quantile portfolios
    4. Construct equal-weighted and long-short portfolio returns

    Parameters
    ----------
    df_cha : pandas.DataFrame
        Monthly return and lagged factor dataset.
    cha_name : str
        Characteristic used for sorting.
    q : int
        Number of quantile groups.

    Returns
    -------
    pandas.DataFrame
        Monthly returns of quantile portfolios and long-short strategy.
    """
    pf_input_sanity_check(df_cha, cha_name)

    df_reshaped = df_reshape(df_cha, cha_name)

    df_sorted = stock_sorting(df_reshaped, cha_name, q)

    df_f = pf_cal(df_sorted, cha_name, q)

    util.color_print('portfolio script done')

    return df_f
