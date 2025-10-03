sandwich_orders = ["Tuna sandwich", "Pastrami sandwich", "Avocado sandwich", "Pastrami sandwich", "Egg sandwich", "Chicken sandwich", "Pastrami sandwich"]

finished_sandwiches = []

while "Pastrami sandwich" in sandwich_orders:
    sandwich_orders.remove("Pastrami sandwich")

while sandwich_orders:
    current_sandwich = sandwich_orders.pop(0)
    print(f"I made your {current_sandwich}")
    finished_sandwiches.append(current_sandwich)
    
print(f"sandwich_orders = {sandwich_orders}")
print(f"finished_sandwiches = {finished_sandwiches}")