# myapp/ml_model.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

def train_model():
    df = pd.read_csv("D:\Shipmet\ML\eshipment.csv")
    # Dropping unwanted columns
    df.drop(["Time_Order_picked","Type_of_vehicle","Road_traffic_density","Vehicle_condition"], axis=1, inplace=True)
    # Label encoding
    le = LabelEncoder()
    df["Weatherconditions"] = le.fit_transform(df["Weatherconditions"])
    df["multiple_deliveries"] = le.fit_transform(df["multiple_deliveries"])
    df["Festival"] = le.fit_transform(df["Festival"])
    # Test train split
    X = df.iloc[:,:-1]
    y = df.iloc[:,-1]
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=1)
    # Model training
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    return rf, scaler

def make_prediction(model, scaler, input_data):
    data = scaler.transform([input_data])
    return model.predict(data)
