# 📈 NASDAQ Volatility Strategy

A quantitative trading strategy that constructs long-short portfolios based on stock return volatility using NASDAQ-listed companies.

---

## 🧠 Strategy Overview

This project implements a **volatility-sorted equity strategy**:

- Calculate stock **daily and monthly returns**
- Estimate **monthly volatility** (standard deviation of daily returns)
- Sort stocks into **quantile portfolios**
- Construct **long-short portfolios** based on volatility ranking

---

## ⚙️ Methodology

### 1. Data Collection
- Source: Yahoo Finance (via `yfinance`)
- Universe: NASDAQ stocks
- Period: 2000 – 2021

### 2. Feature Engineering
- Daily returns
- Monthly returns
- Volatility (monthly standard deviation of daily returns)

### 3. Portfolio Construction
- Stocks sorted into quantiles (e.g., 3 groups)
- Equal-weighted portfolios:
  - Low volatility
  - Medium volatility
  - High volatility
- Long-Short:
  - Long: High volatility
  - Short: Low volatility

---

## 📊 Results

### Cumulative Returns

![Strategy Result](assets/results.png)

---

## 🔍 Key Findings

- High-volatility stocks significantly outperform low-volatility stocks
- Long-short strategy produces **negative cumulative return**
- T-statistic ≈ 0 → **no statistical significance**
- Indicates weak predictive power of volatility alone

---

## ⚠️ Limitations

- Survivorship bias (static ticker list)
- No transaction costs considered
- Single-factor strategy (volatility only)

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python analysis.py
