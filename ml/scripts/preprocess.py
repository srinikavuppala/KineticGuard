import pandas as pd
import numpy as np
import os
import math
import json
from pathlib import Path


def extract_features(raw_df):
    features_list = []

    for index, row in raw_df.iterrows():
        landmark_list = json.loads(row['landmarks'])
        coords = np.array(landmark_list).reshape(21, 2)

        distances = []
        for i in range(21):
            for j in range(i + 1, 21):
                dist = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
                distances.append(dist)

        features_list.append({
            'gesture': row['gesture'],
            'frame': row['frame'],
            'features': np.array(distances)
        })

    result_df = pd.DataFrame(features_list)

    Path('data/processed').mkdir(exist_ok=True)
    result_df.to_csv(Path('data/processed/features_extracted.csv'), index=False)

    print(f"Extracted {len(result_df)} samples with {len(result_df['features'].iloc[0])} distance features each.")
    return result_df


if __name__ == "__main__":
    print("Loading raw data...")
    raw_df = pd.read_csv(Path('data/raw/dummy_raw_data.csv'))

    print("Running spatial feature extraction...")
    processed_df = extract_features(raw_df)

    print("Feature Preview (First 5 rows):")
    print(processed_df.head())