import json
from pathlib import Path

scenario = {
    "route": "JFK-LAX",
    "capacity": 180,
    "booking_horizon_days": 30,

    "fare_classes": {
        "low": {
            "price": 150,
            "expected_demand": 120
        },
        "high": {
            "price": 400,
            "expected_demand": 50
        }
    }
}

output_path = Path("data/processed/base_scenario.json")

with open(output_path, "w") as file:
    json.dump(scenario, file, indent=4)

print(f"Scenario saved to {output_path}")