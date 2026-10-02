def calculate_quantities(construction_area: float, number_of_floors: int, basement: bool):
    """
    Estimates construction material quantities using standard thumb-rule
    approximations based on total built-up area.
    These are preliminary estimates, not a substitute for detailed BOQ.
    """
    total_built_up_area = construction_area * number_of_floors

    if basement:
        total_built_up_area += construction_area * 0.6  # basement adds ~60% extra area equivalent

    cement_bags = round(total_built_up_area * 0.4, 2)
    steel_kg = round(total_built_up_area * 4, 2)
    sand_cft = round(total_built_up_area * 1.5, 2)
    aggregate_cft = round(total_built_up_area * 1.5, 2)
    bricks_units = round(total_built_up_area * 8, 2)

    return {
        "total_built_up_area": round(total_built_up_area, 2),
        "cement_bags": cement_bags,
        "steel_kg": steel_kg,
        "sand_cft": sand_cft,
        "aggregate_cft": aggregate_cft,
        "bricks_units": bricks_units,
    }