def calculate_risks(construction_area: float, number_of_floors: int, basement: bool, parking_cars: int):
    """
    Rule-based preliminary risk/safety checks.
    These are advisory flags, not a substitute for professional structural
    or safety review.
    """
    warnings = []

    if basement:
        warnings.append({
            "level": "warning",
            "category": "Structural",
            "message": "Basement selected — additional waterproofing and drainage review is required.",
        })

    if number_of_floors >= 3:
        warnings.append({
            "level": "warning",
            "category": "Life Safety",
            "message": "Multiple floors (G+2 or higher) — staircase width and life-safety exits require professional verification.",
        })

    if number_of_floors >= 4:
        warnings.append({
            "level": "critical",
            "category": "Structural",
            "message": "4+ floors selected — detailed structural design by a licensed engineer is mandatory, not optional.",
        })

    if construction_area > 5000:
        warnings.append({
            "level": "warning",
            "category": "Fire Safety",
            "message": "Large built-up area — fire safety and emergency exit planning recommended.",
        })

    if parking_cars >= 3 and basement:
        warnings.append({
            "level": "info",
            "category": "Ventilation",
            "message": "Basement parking for 3+ cars — mechanical ventilation may be required by local building codes.",
        })

    if not warnings:
        warnings.append({
            "level": "info",
            "category": "General",
            "message": "No major preliminary risk flags identified. Standard construction review still recommended.",
        })

    # Simple risk scoring
    critical_count = sum(1 for w in warnings if w["level"] == "critical")
    warning_count = sum(1 for w in warnings if w["level"] == "warning")

    if critical_count > 0:
        overall_risk = "High"
    elif warning_count >= 2:
        overall_risk = "Medium"
    elif warning_count == 1:
        overall_risk = "Low-Medium"
    else:
        overall_risk = "Low"

    return {
        "overall_risk": overall_risk,
        "warnings": warnings,
    }