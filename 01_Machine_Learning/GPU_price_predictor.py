import sqlite3
import random
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# Name of the local SQLite database file
DB_NAME = "GPU.db"

# Global variables: fixed categories for data generation and user input
BRANDS = ("Nvidia", "AMD", "Intel")
CONDITIONS = ("Like New", "Good", "Average", "Poor")
USAGES = ("Gaming", "Office", "Mining")

# NEW: instead of long if/elif chains we use dictionaries for lookups.
# Each brand has its own models, and each model has a fixed VRAM value
# and a base price. This makes the data more realistic and the code shorter.
GPU_MODELS = {
    "Nvidia": ["RTX 4090", "RTX 4080", "RTX 4070", "RTX 3060"],
    "AMD":    ["RX 7900 XTX", "RX 7800 XT", "RX 6700 XT"],
    "Intel":  ["Arc A770", "Arc A750"],
}

GPU_VRAM_GB = {
    "RTX 4090": 24, "RTX 4080": 16, "RTX 4070": 12, "RTX 3060": 12,
    "RX 7900 XTX": 24, "RX 7800 XT": 16, "RX 6700 XT": 12,
    "Arc A770": 16, "Arc A750": 8,
}

GPU_BASE_PRICES = {
    "RTX 4090": 1600, "RTX 4080": 1100, "RTX 4070": 600, "RTX 3060": 300,
    "RX 7900 XTX": 950, "RX 7800 XT": 550, "RX 6700 XT": 350,
    "Arc A770": 320, "Arc A750": 250,
}

# Multipliers instead of fixed surcharges, since GPU prices vary a lot
CONDITION_MULTIPLIER = {"Like New": 1.15, "Good": 1.0, "Average": 0.85, "Poor": 0.65}
USAGE_MULTIPLIER = {"Gaming": 1.0, "Office": 1.05, "Mining": 0.75}  # mining cards are more worn out


def create_sql_database():
    """Creates the SQLite database and table if they don't already exist."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        # Create the table for GPU data with the corresponding columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gpus (
                id INTEGER PRIMARY KEY,
                brand TEXT,
                model TEXT,
                vram_gb INTEGER,
                condition TEXT,
                usage TEXT,
                price REAL
            )
        """)
        # Delete previous entries so we start fresh with new data every run
        cursor.execute("DELETE FROM gpus")


def generate_1000_gpu_records():
    """Generates 1000 random GPU records based on predefined logic."""
    gpu_list = []

    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()

        for i in range(1000):
            # Randomly pick the properties
            brand = random.choice(BRANDS)
            model = random.choice(GPU_MODELS[brand])  # pick a model that matches the brand
            vram = GPU_VRAM_GB[model]
            condition = random.choice(CONDITIONS)
            usage = random.choice(USAGES)

            # Price logic: combine the model's base price with the multipliers
            base_price = GPU_BASE_PRICES[model]
            price = base_price * CONDITION_MULTIPLIER[condition] * USAGE_MULTIPLIER[usage]

            # Add realistic price variation (+/- 40 dollars) and enforce a minimum price
            final_price = max(50, price + random.randint(-40, 40))
            gpu_list.append((brand, model, vram, condition, usage, round(final_price, 2)))

        # Efficiently insert all 1000 records into the SQL database
        cursor.executemany("""
            INSERT INTO gpus (brand, model, vram_gb, condition, usage, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, gpu_list)
        print(f"📊 Data generator: successfully created {len(gpu_list)} GPUs!")


def load_data_from_db() -> pd.DataFrame:
    """Loads the generated data from the SQL database into a Pandas DataFrame."""
    try:
        with sqlite3.connect(DB_NAME) as connection:
            sql_query = "SELECT brand, model, vram_gb, condition, usage, price FROM gpus"
            # Converts the SQL result directly into a tabular Pandas structure
            return pd.read_sql_query(sql_query, connection)
    except Exception as e:
        print(f"❌ Error loading the data: {e}")
        return pd.DataFrame()


def train_and_save_pipeline(df: pd.DataFrame):
    """Prepares the data, trains the ML model, evaluates it, and saves it."""
    if df.empty:
        print("❌ No data available to train on.")
        return

    # Split into features (X) and target (y - the price)
    X = df[['brand', 'model', 'vram_gb', 'condition', 'usage']]
    y = df['price']

    # Split into training data (80%) and test data (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # NEW: vram_gb is a number and is NOT one-hot encoded, it passes straight
    # through as a number via 'remainder=passthrough'.
    categorical_columns = ['brand', 'model', 'condition', 'usage']

    encoder = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
        ],
        remainder='passthrough'
    )

    # Machine learning pipeline: links data preparation and the AI model (RandomForest)
    pipeline = Pipeline(steps=[
        ('encoder', encoder),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Train the AI model with the training data
    pipeline.fit(X_train, y_train)

    # Generate predictions on the unseen test data
    y_pred = pipeline.predict(X_test)

    # Calculate error AND goodness of fit (not just MAE like before)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"📊 Mean Absolute Error (MAE) on test data: ${mae:.2f}")
    print(f"📈 R² score (explained variance): {r2:.3f}")

    # Saves the entire pipeline (preprocessing + model) to a file
    joblib.dump(pipeline, "gpu_pipeline.pkl")
    print("💾 Pipeline successfully saved as 'gpu_pipeline.pkl'")

    # Creates a scatter plot to visualize prediction accuracy
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)  # ideal line
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title(f'GPU Pipeline Performance Check (R² = {r2:.3f})')
    plt.show()


def safe_input(prompt, allowed_values):
    """Validates terminal user input to catch typos."""
    while True:
        user_input = input(prompt).strip()
        if user_input in allowed_values:
            return user_input
        else:
            print(f"❌ Invalid input. Please choose from: {', '.join(allowed_values)}")


def show_feature_importance():
    """Analyzes and prints which features have the biggest influence on price."""
    # Load the model for analysis
    pipeline = joblib.load("gpu_pipeline.pkl")
    encoder = pipeline.named_steps['encoder']
    ai_brain = pipeline.named_steps['regressor']

    # Retrieve the transformed column names and their weights
    column_names = encoder.get_feature_names_out()
    importances = ai_brain.feature_importances_

    # Store in a clear table and sort it
    importance_df = pd.DataFrame({
        'Feature': column_names,
        'Importance (%)': importances * 100
    }).sort_values(by='Importance (%)', ascending=False)

    print("\n" + "=" * 50)
    print("📊 RELEVANCE ANALYSIS: WHAT DOES THE AI CARE ABOUT MOST?")
    print("=" * 50)
    print(importance_df.head(8).to_string(index=False))  # show the top 8 features
    print("=" * 50)


def main():
    print("🚀 Starting the automated GPU pipeline...")
    print("=" * 50)

    # 1. Pipeline steps: create database, feed data in, load it back out, and train the AI
    create_sql_database()
    generate_1000_gpu_records()
    my_data = load_data_from_db()
    train_and_save_pipeline(my_data)

    # 2. Print out the feature importance analysis
    show_feature_importance()

    # 3. Load the just-saved pipeline directly for interactive predictions
    trained_model = joblib.load("gpu_pipeline.pkl")

    # --- INTERACTIVE LOOP ---
    while True:
        print("\n" + "=" * 50)
        print("🔮 INTERACTIVE GPU PRICE PREDICTION")
        print("=" * 50)

        # First ask for the brand ...
        input_brand = safe_input("Which brand? (Nvidia, AMD, Intel): ", BRANDS)
        # ... then only offer the models that match that brand (NEW, smarter than before)
        input_model = safe_input(
            f"Which model? ({', '.join(GPU_MODELS[input_brand])}): ",
            GPU_MODELS[input_brand]
        )
        # No need to enter VRAM manually anymore, the model already tells us
        vram = GPU_VRAM_GB[input_model]
        input_condition = safe_input("What condition? (Like New, Good, Average, Poor): ", CONDITIONS)
        input_usage = safe_input("What was it used for? (Gaming, Office, Mining): ", USAGES)

        # Put the inputs into exactly the same DataFrame structure used during training
        new_gpu_df = pd.DataFrame([{
            'brand': input_brand,
            'model': input_model,
            'vram_gb': vram,
            'condition': input_condition,
            'usage': input_usage
        }])

        # Have the model estimate the price
        estimated_price = float(trained_model.predict(new_gpu_df)[0])

        print("-" * 50)
        print(f"💰 The estimated price for this GPU is: ${estimated_price:.2f}")
        print("=" * 50)

        # Ask whether to run another round or quit
        again = input("\nWould you like to estimate another GPU? (yes/no): ").strip().lower()
        if again != 'yes':
            print("\n👋 Program ended. See you next time!")
            break


# Main program (only runs when this file is executed directly)
if __name__ == "__main__":
    main()
