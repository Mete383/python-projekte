# 🤖 Machine Learning Frameworks & Pipelines

This directory contains production-grade Data Science and Machine Learning projects focused on automatic data preprocessing and price prediction modeling.

## 🚀 Key Features Demonstrated
* **Database Integration:** Building and querying localized relational databases using `sqlite3`.
* **Synthetic Data Engineering:** Generating realistic hardware datasets with customized market pricing business logic and noise injection.
* **Advanced Pipeline Architectures:** Implementing Scikit-Learn `Pipeline` and `ColumnTransformer` modules to cleanly separate categorical data via `OneHotEncoder`.
* **Feature Relevance Analysis:** Extracting and sorting `feature_importances_` directly from trained trees to reveal model decision drivers.
* **Terminal Interactivity:** Custom CLI input-validation loops enabling safe real-time predictive queries.

## 📁 Projects in this Folder

### 1. Keyboard Price Predictor (`keyboard_price_predictor/`)
Trains a `RandomForestRegressor` on custom generated keyboard specifications (Brand, Layout, Condition, Connection Type) to evaluate and predict market values. Includes full scatter-plot accuracy visualization via `matplotlib`.

### 2. Mouse Price Predictor (`mouse_price_predictor/`)
A highly reusable prediction pipeline applying advanced column grouping on mouse hardware metrics (DPI steps, Wireless/Wired, Wear condition) to output robust price estimations.

### 3. GPU Price Predictor (`gpu_price_predictor/`)
Our initial proof-of-concept pipeline sorting graphics card pricing tiers dynamically through structured matrix encoding.

## 🛠️ Technology Stack
* **Language:** Python 3
* **Libraries:** Scikit-Learn, Pandas, Joblib, Matplotlib
* **Database:** SQLite3
