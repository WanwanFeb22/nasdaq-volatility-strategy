"""
Configuration file for NASDAQ Volatility Strategy project.

Defines:
- Project directories
- Data storage paths
- Stock universe (NASDAQ tickers)
"""

import os
import toolkit_config as cfg

ROOTDIR = os.path.join(cfg.PRJDIR, 'nasdaq_volatility_strategy')
DATADIR = os.path.join(ROOTDIR, 'data')

# We choose the US market and the NASDAQ exchange for our analysis.
TICMAP = {
    'AAPL': 'Apple Inc.',
    'ADBE': 'Adobe Inc.',
    'ADI': 'Analog Devices, Inc.',
    'ADP': 'Automatic Data Processing, Inc.',
    'ADSK': 'Autodesk, Inc.',
    'AKAM': 'Akamai Technologies, Inc.',
    'AMAT': 'Applied Materials, Inc.',
    'AMD': 'Advanced Micro Devices, Inc.',
    'AMZN': 'Amazon.com, Inc.',
    'ANSS': 'ANSYS, Inc.',
    'AVGO': 'Broadcom Inc.',
    'BB': 'BlackBerry Limited',
    'BMC': 'BMC Software, Inc.',
    'CDNS': 'Cadence Design Systems, Inc.',
    'CIEN': 'Ciena Corporation',
    'CRM': 'Salesforce.com, Inc.',
    'CSCO': 'Cisco Systems, Inc.',
    'CTSH': 'Cognizant Technology Solutions Corporation',
    'DELL': 'Dell Technologies Inc.',
    'EBAY': 'eBay Inc.',
    'GOOG': 'Alphabet Inc. Class C',
    'GOOGL': 'Alphabet Inc. Class A',
    'HPQ': 'HP Inc.',
    'HPE': 'Hewlett Packard Enterprise Company',
    'IBM': 'International Business Machines Corporation',
    'INTC': 'Intel Corporation',
    'INTU': 'Intuit Inc.',
    'JNPR': 'Juniper Networks, Inc.',
    'KLAC': 'KLA Corporation',
    'LRCX': 'Lam Research Corporation',
    'MCHP': 'Microchip Technology Incorporated',
    'META': 'Meta Platforms, Inc.',
    'MSFT': 'Microsoft Corporation',
    'MU': 'Micron Technology, Inc.',
    'NFLX': 'Netflix, Inc.',
    'NTAP': 'NetApp, Inc.',
    'NVDA': 'NVIDIA Corporation',
    'NXPI': 'NXP Semiconductors N.V.',
    'ORCL': 'Oracle Corporation',
    'PAYX': 'Paychex, Inc.',
    'PYPL': 'PayPal Holdings, Inc.',
    'QCOM': 'Qualcomm Incorporated',
    'SNPS': 'Synopsys, Inc.',
    'STX': 'Seagate Technology Holdings PLC',
    'TSLA': 'Tesla, Inc.',
    'TTWO': 'Take-Two Interactive Software, Inc.',
    'TXN': 'Texas Instruments Incorporated',
    'VRSN': 'VeriSign, Inc.',
    'WDC': 'Western Digital Corporation',
    'ZM': 'Zoom Video Communications, Inc.'
}


TICKERS = sorted(TICMAP.keys())

def standardise_colnames(df):
    """
    Standardize DataFrame column names.

    - Convert all column names to lowercase
    - Replace spaces with underscores
    - Avoid duplicate column names
    """
    cols = set(df.columns)
    def _parse_name(colname):
        new_name = colname.lower().replace(' ', '_')
        if new_name == colname:
            return colname
        elif new_name in cols:
            return '_' + new_name
        else:
            return new_name
    return df.rename(columns=_parse_name)




