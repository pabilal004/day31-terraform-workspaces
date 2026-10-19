def calculate_total(price, quantity):
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    return price * quantity
