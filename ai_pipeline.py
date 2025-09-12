import os
import sys
import sqlite3
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense

DB_PATH = "example.db"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "trained_model.h5")

# --- Database ---
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_data TEXT,
        output_data TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def insert_data(input_data, output_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO ai_data (input_data, output_data) VALUES (?, ?)',
        (str(input_data), str(output_data))
    )
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM ai_data", conn)
    conn.close()
    return df

# --- Data prep ---
def load_data(file_path):
    return pd.read_csv(file_path)

def preprocess_data(df):
    return df.dropna()

def feature_engineering(df):
    if 'existing_feature' in df.columns:
        df['new_feature'] = df['existing_feature'] * 2
    else:
        raise ValueError("Expected column 'existing_feature' not found.")
    return df

# --- Model ---
def build_model(input_dim):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_dim,)),
        Dense(32, activation='relu'),
        Dense(1)  # regression output
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def train_model(df):
    os.makedirs(MODEL_DIR, exist_ok=True)
    X = df.drop(columns=['new_feature']).values
    y = df['new_feature'].values
    model = build_model(X.shape[1])
    model.fit(X, y, epochs=5, verbose=1)
    model.save(MODEL_PATH)
    return MODEL_PATH

def evaluate_model(df):
    X = df.drop(columns=['new_feature']).values
    y = df['new_feature'].values
    model = load_model(MODEL_PATH)
    loss, mae = model.evaluate(X, y, verbose=0)
    print(f"Test MAE: {mae:.4f}")
    return model

# --- Predict + log ---
def predict_and_log(model, df):
    X = df.drop(columns=['new_feature']).values
    preds = model.predict(X)
    for inp_row, pred in zip(X, preds):
        insert_data(inp_row.tolist(), float(pred))
    print(f"Logged {len(preds)} predictions into {DB_PATH}")

# --- Personality ---
def react_to_input(input_data):
    if input_data.lower() == 'hello':
        print('Hi there!')
    else:
        print('I am here to assist you.')

def self_awareness():
    print('I am a program designed to assist with AI tasks.')

# --- Main ---
def run_pipeline():
    setup_database()
    data_file = "data/dataset.csv"
    if not os.path.exists(data_file):
        print(f"⚠️ No dataset at {data_file}, skipping training.")
        return
    df = load_data(data_file)
    df = preprocess_data(df)
    df = feature_engineering(df)
    train_model(df)
    model = evaluate_model(df)
    predict_and_log(model, df)
    print("Done.")

def show_history():
    setup_database()
    df = get_all_data()
    if df.empty:
        print("⚠️ No data logged yet.")
    else:
        print("\n--- Logged Predictions ---")
        print(df)

if __name__ == "__main__":
    if "--show" in sys.argv:
        show_history()
    else:
        run_pipeline()
        react_to_input("Hello")
        self_awareness()
