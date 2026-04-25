import os
import pandas as pd
import config as cfg
from nasdaq_volatility_strategy import main as main

OUTDIR = os.path.join(cfg.ROOTDIR, 'outcome')
os.makedirs(OUTDIR, exist_ok=True)

daily_csv = os.path.join(OUTDIR, 'DM_Ret_dict_Daily.csv')
monthly_csv = os.path.join(OUTDIR, 'DM_Ret_dict_Monthly.csv')
cha_csv = os.path.join(OUTDIR, 'Vol_Ret_mrg_df.csv')
pf_csv = os.path.join(OUTDIR, 'EW_LS_pf_df.csv')

def generate_data(tickers, start, end, cha_name, ret_freq_use, q):
    """
    Run the strategy pipeline and save intermediate outputs.
    """
    dict_ret, df_cha, df_portfolios = main.portfolio_main(
        tickers, start, end, cha_name, ret_freq_use, q
    )

    dict_ret['Daily'].to_csv(daily_csv)
    dict_ret['Monthly'].to_csv(monthly_csv)
    df_cha.to_csv(cha_csv)
    df_portfolios.to_csv(pf_csv)

    return dict_ret, df_cha, df_portfolios

def load_or_generate_data():
    """
    Load existing output files if available; otherwise run the full pipeline.
    """
    print("Checking missing data...")

    need_generate = []

    dict_ret = {}
    df_cha = None
    df_portfolios = None

    if os.path.exists(daily_csv):
        print("Reading Daily return data")
        dict_ret['Daily'] = pd.read_csv(daily_csv, index_col=0, parse_dates=True)
    else:
        need_generate.append("Daily")

    if os.path.exists(monthly_csv):
        print("Reading Monthly return data")
        dict_ret['Monthly'] = pd.read_csv(monthly_csv, index_col=0)
        dict_ret['Monthly'].index = pd.to_datetime(dict_ret['Monthly'].index).to_period('M')
    else:
        need_generate.append("Monthly")

    if os.path.exists(cha_csv):
        print("Reading feature (df_cha) data")
        df_cha = pd.read_csv(cha_csv, index_col=0)
        df_cha.index = pd.to_datetime(df_cha.index).to_period('M')
    else:
        need_generate.append("cha")

    if os.path.exists(pf_csv):
        print("Reading portfolio (df_portfolios) data")
        df_portfolios = pd.read_csv(pf_csv, index_col=0)
        df_portfolios.index = pd.to_datetime(df_portfolios.index).to_period('M')
    else:
        need_generate.append("portfolio")

    if need_generate:
        print(f"The following data is missing and will be regenerated: {','.join(need_generate)}")

        full_dict_ret, full_df_cha, full_df_portfolios = generate_data(
            cfg.TICKERS, '2000-12-29', '2021-08-31', 'vol', ['Daily'], 3
        )

        if "Daily" in need_generate:
            dict_ret['Daily'] = full_dict_ret['Daily']
        if "Monthly" in need_generate:
            dict_ret['Monthly'] = full_dict_ret['Monthly']
        if "cha" in need_generate:
            df_cha = full_df_cha
        if "portfolio" in need_generate:
            df_portfolios = full_df_portfolios
    else:
        print("All data files already exist, there is no need to download them again.")

    return dict_ret, df_cha, df_portfolios

if __name__ == "__main__":
    dict_ret, df_cha, df_portfolios = load_or_generate_data()
    print("[INFO] Data pipeline completed.")