import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    """Loads raw transactions and handles type conversions."""
    # load data
    df = pd.read_csv(file_path)
    
    # transform date strings to active datetime objects
    df['transaction_time'] = pd.to_datetime(df['transaction_time'])
    df['date'] = df['transaction_time'].dt.date
    df['hour'] = df['transaction_time'].dt.hour
    
    # compute revenue per row
    df['revenue'] = df['transaction_qty'] * df['unit_price']
    return df

def aggregate_time_series(df):
    """Aggregates transactional entries into structured Hourly and Daily dataframes."""
    # hourly aggregation for operational demand forecasting
    hourly_df = df.groupby(['store_id', 'date', 'hour']).agg(
        hourly_qty=('transaction_qty', 'sum'),
        hourly_revenue=('revenue', 'sum'),
        transaction_count=('transaction_id', 'count')
    ).reset_index()
    
    # build explicit datetime column
    hourly_df['datetime'] = pd.to_datetime(
        hourly_df['date'].astype(str) + ' ' + hourly_df['hour'].astype(str) + ':00:00'
    )
    hourly_df = hourly_df.sort_values(['store_id', 'datetime']).reset_index(drop=True)
    return hourly_df

def build_predictive_features(hourly_df):
    """Generates lag elements and temporal calendar attributes."""
    # shift records to get historical context
    hourly_df['qty_lag_1h'] = hourly_df.groupby('store_id')['hourly_qty'].shift(1)
    hourly_df['qty_lag_24h'] = hourly_df.groupby('store_id')['hourly_qty'].shift(24)
    hourly_df['qty_lag_168h'] = hourly_df.groupby('store_id')['hourly_qty'].shift(168) # 1 week lag
    
    # structural rolling metrics
    hourly_df['rolling_avg_3h'] = hourly_df.groupby('store_id')['hourly_qty'].rolling(3).mean().reset_index(0, drop=True)
    
    # calendar categorical feature indices
    hourly_df['day_of_week'] = hourly_df['datetime'].dt.dayofweek
    hourly_df['hour_of_day'] = hourly_df['datetime'].dt.hour
    
    # fill null rows created by historical lagging shifts
    hourly_df.fillna(0, inplace=True)
    return hourly_df

if __name__ == "__main__":
    print("Running Data Pipeline verification...")
    # Example test run (assuming a file named 'coffee_transactions.csv' exists)
    # raw_data = load_and_clean_data('coffee_transactions.csv')
    # hourly_data = aggregate_time_series(raw_data)
    # complete_data = build_predictive_features(hourly_data)
    # print(complete_data.head())
