import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
from data_pipeline import load_and_clean_data, aggregate_time_series, build_predictive_features

def split_and_train(data_path):
    """Processes raw data, performs chronological splits, and trains XGBoost."""
    # 1. Pipeline execution
    raw_df = load_and_clean_data(data_path)
    hourly_df = aggregate_time_series(raw_df)
    features_df = build_predictive_features(hourly_df)
    
    # 2. Setup predictive targets
    feature_cols = ['qty_lag_1h', 'qty_lag_24h', 'qty_lag_168h', 'rolling_avg_3h', 'day_of_week', 'hour_of_day']
    X = features_df[feature_cols]
    y = features_df['hourly_qty']
    
    # 3. Chronological Train-Test Split (Strictly Time-Based)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # 4. Train XGBoost Model
    print("Training XGBoost Regressor model...")
    model = xgb.XGBRegressor(
        n_estimators=200, 
        learning_rate=0.05, 
        max_depth=6, 
        objective='reg:squarederror'
    )
    model.fit(X_train, y_train)
    
    # 5. Evaluate Performance
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    # Calculate Mean Absolute Percentage Error safely
    mape = np.mean(np.abs((y_test - preds) / np.where(y_test == 0, 1, y_test))) * 100
    
    print(f"\n--- Evaluation Results ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f} units")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f} units")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    
    # Save model binary configuration to file
    with open('xgb_coffee_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("\nModel saved successfully as 'xgb_coffee_model.pkl'")
    
    return model

if __name__ == "__main__":
    # To run this script, make sure your dataset matches this filename:
    try:
        split_and_train('coffee_transactions.csv')
    except FileNotFoundError:
        print("Error: Please place your 'coffee_transactions.csv' dataset in this directory to run training.")
