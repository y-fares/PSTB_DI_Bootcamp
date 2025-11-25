def safe_sum(my_list):
    total = 0
    for item in my_list:
        if isinstance(item, (int, float)):  # check if number
            total += item
        else:
            print(f"Skipping invalid item: {item}")
    return total

my_list = [2, 3, 1, 2, "four", 42, 1, 5, 3, "imanumber"]
print("Total =", safe_sum(my_list))
