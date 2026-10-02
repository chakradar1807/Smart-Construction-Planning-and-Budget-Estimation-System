"""
Generates synthetic 'historical' construction project data for ML training.
Cost is computed using category-based rate tiers (Economy/Standard/Premium/Luxury),
matching the engineering cost engine, with added noise for realism.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N_SAMPLES = 4000

CATEGORY_RATES = {
    "Economy": (1300, 1600),
    "Standard": (1700, 2000),
    "Premium": (2200, 2700),
    "Luxury": (3000, 4000),
}

LOCATIONS = ["Chennai", "Bangalore", "Hyderabad", "Coimbatore", "Madurai"]

records = []

for _ in range(N_SAMPLES):
    construction_area = np.random.uniform(800, 4000)
    number_of_floors = np.random.randint(1, 4)
    basement = np.random.choice([0, 1], p=[0.7, 0.3])
    location = np.random.choice(LOCATIONS)
    category = np.random.choice(list(CATEGORY_RATES.keys()))
    parking_cars = np.random.randint(0, 3)

    total_built_up_area = construction_area * number_of_floors
    if basement:
        total_built_up_area += construction_area * 0.6

    low, high = CATEGORY_RATES[category]
    rate = np.random.uniform(low, high)  # simulate variation within the tier

    base_cost = total_built_up_area * rate

    # Add noise (+/- 6%) to simulate real-world unpredictability
    noise_factor = np.random.uniform(0.94, 1.06)
    total_cost = base_cost * noise_factor

    # Duration estimate (weeks) - higher category = slightly longer (more finishing work)
    category_duration_factor = {"Economy": 0.9, "Standard": 1.0, "Premium": 1.15, "Luxury": 1.3}[category]
    base_duration = (10 + (total_built_up_area / 150) + (number_of_floors * 2) + (basement * 3))
    duration_weeks = base_duration * category_duration_factor * np.random.uniform(0.9, 1.15)

    records.append({
        "construction_area": construction_area,
        "number_of_floors": number_of_floors,
        "basement": basement,
        "location": location,
        "category": category,
        "parking_cars": parking_cars,
        "total_built_up_area": total_built_up_area,
        "total_cost": total_cost,
        "duration_weeks": duration_weeks,
    })

df = pd.DataFrame(records)
df.to_csv("notebooks/training_data.csv", index=False)

print(f"Generated {len(df)} synthetic project records.")
print(df.head())
print("\nSaved to notebooks/training_data.csv")