import math


def calculate_safety_stock(
    average_daily_sales,
    lead_time,
    safety_factor
):

    return average_daily_sales * lead_time * safety_factor


def calculate_reorder_point(
    average_daily_sales,
    lead_time,
    safety_stock
):

    return (
        average_daily_sales * lead_time
    ) + safety_stock


def calculate_eoq(
    annual_demand,
    ordering_cost,
    holding_cost
):

    eoq = math.sqrt(
        (2 * annual_demand * ordering_cost)
        / holding_cost
    )

    return round(eoq, 2)


def inventory_status(
    current_stock,
    reorder_point,
    recommended_stock
):

    if current_stock < reorder_point:
        return "Reorder Required"

    elif current_stock > recommended_stock:
        return "Overstock"

    else:
        return "Sufficient Stock"