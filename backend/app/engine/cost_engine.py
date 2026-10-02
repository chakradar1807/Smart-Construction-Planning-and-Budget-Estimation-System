CATEGORY_RATES = {
    "Economy": (1300, 1600),
    "Standard": (1700, 2000),
    "Premium": (2200, 2700),
    "Luxury": (3000, 4000),
}


def calculate_cost(total_built_up_area: float, category: str = "Standard"):
    low, high = CATEGORY_RATES.get(category, CATEGORY_RATES["Standard"])
    avg_rate = (low + high) / 2

    total_cost = total_built_up_area * avg_rate

    material_cost = total_cost * 0.55
    labour_cost = total_cost * 0.30
    contingency = total_cost * 0.05
    other_cost = total_cost - material_cost - labour_cost - contingency

    return {
        "category": category,
        "rate_range_low": low,
        "rate_range_high": high,
        "material_cost": round(material_cost, 2),
        "labour_cost": round(labour_cost, 2),
        "contingency": round(contingency, 2),
        "other_cost": round(other_cost, 2),
        "total_cost": round(total_cost, 2),
        "cost_per_sqft": round(avg_rate, 2),
    }