# import the libraries

import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials

start_date = '2010-01-01'
end_date = '2020-07-12'
tickers = ['GOOGL', 'MSFT', 'AMZN']
all_tickers = []
    
def ticker_data (ticker):
    yahoo_financials = YahooFinancials( ticker )
    stock_prices = yahoo_financials.get_historical_price_data( \
    start_date, end_date, 'daily' )

    stock_df = pd.DataFrame( stock_prices[ticker]['prices'] )
    stock_df['formatted_date'] = pd.to_datetime( stock_df['formatted_date'] )
    stock_df = stock_df.drop( ['high', 'low', 'open', 'close', 'volume', 'date'],\
                             axis = 1 ).set_index( 'formatted_date' )
    stock_df['simple_return'] = stock_df['adjclose'].pct_change()
    
    stock_df['simple_return_std'] = stock_df['simple_return'].rolling( window = 21 )\
        .agg( ['std'] )
    stock_df['simple_return_mean'] = stock_df['simple_return'].rolling( window = 21 )\
        .agg( ['mean'] )
    
    mu = stock_df['simple_return_mean']
    sigma = stock_df['simple_return_std']
    stock_df['upper_limit'] = mu + ( 3 * sigma )
    stock_df['lower_limit'] = mu - ( 3 * sigma )
    condition = (stock_df['simple_return'] > stock_df['upper_limit']) | (stock_df['simple_return'] < stock_df['lower_limit'])
    stock_df['is_outlier'] = np.where(condition, 1, 0)

    stock_df['symbol'] = ticker
    return stock_df


for ticker in tickers:
    df = ticker_data( ticker )
    all_tickers.append( df )

all_tickers_df = pd.concat( all_tickers )
all_tickers_df = all_tickers_df.reset_index()
