import pandas as pd
import numpy as np
import os


def generate_dummy_data(num_samples: int = 1000):
    np.random.seed(42)
    gestures = ['GESTURE', 'RANDOM_MOVEMENT', 'DROP_ARM', 'NO_GUESTURE']
    data = []

    for _ in range(num_samples):
        base_hand = np.random.uniform(-0.5, 0.5, size=(21, 2))

        roll = gestures[np.random.randint(0, len(gestures))]

        if roll == 'GESTURE':
            base_hand[0] += 0.002
        elif roll == 'DROP_ARM':
            base_hand[:, 1] -= np.linspace(0, 0.3, 21)
        else:
            base_hand += np.random.uniform(-0.05, 0.05, size=(21, 2))

        data.append({
            "gesture": roll,
            "frame": np.random.randint(0, 10),
            "landmarks": base_hand.flatten().tolist()
        })

    df = pd.DataFrame(data)
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/dummy_raw_data.csv', index=False)
    print(f"Generated {len(df)} fake gesture samples.")
    return df


if __name__ == "__main__":
    generate_dummy_data()