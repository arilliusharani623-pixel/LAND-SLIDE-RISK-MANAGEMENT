import json
from pathlib import Path

p = Path(r'c:\Users\DELL\Downloads\LAND SLIDE RISK MONITORING SYSTEM (1)\EARLY WARNING AND LAND SLIDE RISK MONITORING SYSTEM IN NER\Untitled0 (1).ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

new_date = """import pandas as pd

print("\n--- Extracting Date Features from df_landslide ---")

# Convert date columns to datetime objects if not already done.
# The dataset stores dates in a US-style format (MM/DD/YYYY), so pandas should infer the format
# instead of using a strict YYYY-MM-DD format that would convert every row to NaT.
if 'event_date' in df_landslide.columns:
    df_landslide['event_date'] = pd.to_datetime(df_landslide['event_date'], errors='coerce')
    df_landslide = df_landslide.dropna(subset=['event_date']).copy()

    if df_landslide.empty:
        print("The current df_landslide is empty; reloading the source dataset and retrying date parsing.")
        df_landslide = pd.read_csv(base_path / 'Global_Landslide_Catalog_Export.csv')
        df_landslide['event_date'] = pd.to_datetime(df_landslide['event_date'], errors='coerce')
        df_landslide = df_landslide.dropna(subset=['event_date']).copy()

    df_landslide['event_year'] = df_landslide['event_date'].dt.year
    df_landslide['event_month'] = df_landslide['event_date'].dt.month
    df_landslide['event_day'] = df_landslide['event_date'].dt.day
    df_landslide['event_day_of_week'] = df_landslide['event_date'].dt.dayofweek
    df_landslide['event_quarter'] = df_landslide['event_date'].dt.quarter
    df_landslide['event_is_weekend'] = (df_landslide['event_date'].dt.dayofweek >= 5).astype(int)
    df_landslide['event_day_of_year'] = df_landslide['event_date'].dt.dayofyear

    print("Extracted features: event_year, event_month, event_day, event_day_of_week, event_quarter, event_is_weekend, event_day_of_year")
    print("df_landslide shape after date feature extraction and NaT removal:", df_landslide.shape)
    display(df_landslide[['event_date', 'event_year', 'event_month', 'event_day', 'event_day_of_week', 'event_is_weekend']].head())
else:
    print("Column 'event_date' not found in df_landslide.")
""".splitlines(keepends=True)

new_encode = """import pandas as pd
from sklearn.preprocessing import OneHotEncoder

print("\n--- Encoding Categorical Features ---")

# --- df_landslide ---
print("\n*** Encoding for df_landslide ***")
# Identify categorical columns for one-hot encoding, excluding high-cardinality or already processed ones
landslide_categorical_cols = [
    'landslide_category', 'landslide_trigger', 'landslide_setting',
    'country_name', 'admin_division_name'
]

# Filter for columns that actually exist, are not all missing, and are object/category dtype
landslide_categorical_cols = [
    col for col in landslide_categorical_cols
    if (col in df_landslide.columns and (
        pd.api.types.is_object_dtype(df_landslide[col]) or pd.api.types.is_categorical_dtype(df_landslide[col])
    ))
]

if df_landslide.empty:
    print("df_landslide is empty; reloading the source dataset before encoding.")
    df_landslide = pd.read_csv(base_path / 'Global_Landslide_Catalog_Export.csv')

if landslide_categorical_cols:
    X_landslide = df_landslide[landslide_categorical_cols].copy()
    X_landslide = X_landslide.fillna('Unknown')
    if not X_landslide.empty and len(X_landslide) > 0:
        print(f"Applying One-Hot Encoding to: {landslide_categorical_cols}")
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_features = encoder.fit_transform(X_landslide)
        encoded_df = pd.DataFrame(
            encoded_features,
            columns=encoder.get_feature_names_out(landslide_categorical_cols),
            index=df_landslide.index
        )
        df_landslide = pd.concat([df_landslide.drop(columns=landslide_categorical_cols), encoded_df], axis=1)
        print("df_landslide shape after encoding:", df_landslide.shape)
        display(df_landslide.head())
    else:
        print("No rows available to encode in df_landslide.")
else:
    print("No suitable categorical columns found for encoding in df_landslide.")

# --- df_rainfall ---
print("\n*** Encoding for df_rainfall ***")
# 'STATE_UT_NAME' and 'DISTRICT' are categorical
rainfall_categorical_cols = ['STATE_UT_NAME', 'DISTRICT']

rainfall_categorical_cols = [
    col for col in rainfall_categorical_cols
    if (col in df_rainfall.columns and (
        pd.api.types.is_object_dtype(df_rainfall[col]) or pd.api.types.is_categorical_dtype(df_rainfall[col])
    ))
]

if rainfall_categorical_cols:
    X_rainfall = df_rainfall[rainfall_categorical_cols].copy().fillna('Unknown')
    if not X_rainfall.empty and len(X_rainfall) > 0:
        print(f"Applying One-Hot Encoding to: {rainfall_categorical_cols}")
        encoder_rainfall = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_features_rainfall = encoder_rainfall.fit_transform(X_rainfall)
        encoded_df_rainfall = pd.DataFrame(
            encoded_features_rainfall,
            columns=encoder_rainfall.get_feature_names_out(rainfall_categorical_cols),
            index=df_rainfall.index
        )
        df_rainfall = pd.concat([df_rainfall.drop(columns=rainfall_categorical_cols), encoded_df_rainfall], axis=1)
        print("df_rainfall shape after encoding:", df_rainfall.shape)
        display(df_rainfall.head())
    else:
        print("No rows available to encode in df_rainfall.")
else:
    print("No suitable categorical columns found for encoding in df_rainfall.")

# --- df_flood ---
print("\n*** Encoding for df_flood ***")
# 'city_name', 'admin_ward', 'soil_group', 'storm_drain_type', 'rainfall_source'
# 'risk_labels' could be ordinal, but for simplicity, we'll one-hot encode for now. Or use Label Encoding.
flood_nominal_categorical_cols = ['city_name', 'admin_ward', 'soil_group', 'storm_drain_type', 'rainfall_source']
flood_nominal_categorical_cols = [
    col for col in flood_nominal_categorical_cols
    if (col in df_flood.columns and (
        pd.api.types.is_object_dtype(df_flood[col]) or pd.api.types.is_categorical_dtype(df_flood[col])
    ))
]

if flood_nominal_categorical_cols:
    X_flood_nominal = df_flood[flood_nominal_categorical_cols].copy().fillna('Unknown')
    if not X_flood_nominal.empty and len(X_flood_nominal) > 0:
        print(f"Applying One-Hot Encoding to: {flood_nominal_categorical_cols}")
        encoder_flood_nominal = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_features_flood_nominal = encoder_flood_nominal.fit_transform(X_flood_nominal)
        encoded_df_flood_nominal = pd.DataFrame(
            encoded_features_flood_nominal,
            columns=encoder_flood_nominal.get_feature_names_out(flood_nominal_categorical_cols),
            index=df_flood.index
        )
        df_flood = pd.concat([df_flood.drop(columns=flood_nominal_categorical_cols), encoded_df_flood_nominal], axis=1)
        print("df_flood shape after nominal encoding:", df_flood.shape)
    else:
        print("No rows available to encode in df_flood nominal features.")

if 'risk_labels' in df_flood.columns and pd.api.types.is_object_dtype(df_flood['risk_labels']):
    print("Applying One-Hot Encoding to 'risk_labels' as a nominal feature.")
    X_risk_labels = df_flood[['risk_labels']].copy().fillna('Unknown')
    encoder_risk_labels = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_risk_labels = encoder_risk_labels.fit_transform(X_risk_labels)
    encoded_df_risk_labels = pd.DataFrame(
        encoded_risk_labels,
        columns=encoder_risk_labels.get_feature_names_out(['risk_labels']),
        index=df_flood.index
    )
    df_flood = pd.concat([df_flood.drop(columns=['risk_labels']), encoded_df_risk_labels], axis=1)
    print("df_flood shape after 'risk_labels' encoding:", df_flood.shape)
    display(df_flood.head())
else:
    print("No 'risk_labels' column or it's not object type in df_flood. Skipping encoding for it.")

# --- df_landslide2 ---
print("\n*** Encoding for df_landslide2 ***")
landslide2_remaining_object_cols = df_landslide2.select_dtypes(include='object').columns.tolist()
if landslide2_remaining_object_cols:
    X_landslide2 = df_landslide2[landslide2_remaining_object_cols].copy().fillna('Unknown')
    if not X_landslide2.empty and len(X_landslide2) > 0:
        print(f"Applying One-Hot Encoding to remaining object columns in df_landslide2: {landslide2_remaining_object_cols}")
        encoder_landslide2_rem = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_features_landslide2_rem = encoder_landslide2_rem.fit_transform(X_landslide2)
        encoded_df_landslide2_rem = pd.DataFrame(
            encoded_features_landslide2_rem,
            columns=encoder_landslide2_rem.get_feature_names_out(landslide2_remaining_object_cols),
            index=df_landslide2.index
        )
        df_landslide2 = pd.concat([df_landslide2.drop(columns=landslide2_remaining_object_cols), encoded_df_landslide2_rem], axis=1)
        print("df_landslide2 shape after encoding:", df_landslide2.shape)
        display(df_landslide2.head())
    else:
        print("No rows available to encode in df_landslide2.")
else:
    print("No remaining categorical columns found for encoding in df_landslide2.")

print("\nCategorical feature encoding complete.")
""".splitlines(keepends=True)

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if i == 23 and 'event_date' in src and 'pd.to_datetime' in src:
        cell['source'] = new_date
    if i == 25 and 'Applying One-Hot Encoding to:' in src:
        cell['source'] = new_encode

p.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('updated cells', [i for i, cell in enumerate(nb['cells']) if i in (23, 25)])
