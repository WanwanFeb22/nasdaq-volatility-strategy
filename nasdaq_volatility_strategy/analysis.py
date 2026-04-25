from nasdaq_volatility_strategy import main as m
import config as cfg
import matplotlib.pyplot as plt

dict_ret, df_cha, df_portfolios = m.portfolio_main(
    tickers=cfg.TICKERS,
    start='2000-12-29',
    end='2021-08-31',
    cha_name='vol',
    ret_freq_use=['Daily'],
    q=3
)

print("Portfolio Returns:")
print(df_portfolios.head())

print("\nCumulative Returns:")
print(m.get_cumulative_ret(df_portfolios))

print("\nLong-Short T-statistics:")
print(m.t_stat(df_portfolios))

cumulative_returns = (1 + df_portfolios).cumprod() - 1
cumulative_returns.plot(title="Cumulative Returns of Volatility-Sorted Portfolios")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.savefig("results.png", dpi=300)
plt.show()