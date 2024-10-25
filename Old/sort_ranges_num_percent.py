def sort_values_into_groups():
    print("Enter your set of values (one per line or separated by space, end with a double enter):")
    values_input = []
    while True:
        line = input()
        if line == "":
            break
        values_input.extend(line.split())
    
    values = [float(value) for value in values_input]
    total_values = len(values)
    
    num_groups = int(input("Enter the number of groups: "))
    group_ranges = []

    for i in range(num_groups):
        lower_bound = float(input(f"Enter the lower bound for group {i+1}: "))
        upper_bound = float(input(f"Enter the upper bound for group {i+1}: "))
        group_ranges.append((lower_bound, upper_bound))

    group_counts = [0] * num_groups

    for value in values:
        for i, (lower_bound, upper_bound) in enumerate(group_ranges):
            if lower_bound <= value < upper_bound:
                group_counts[i] += 1
                break

    print(f"\nTotal number of values: {total_values}\n")
    
    for i, (lower_bound, upper_bound) in enumerate(group_ranges):
        count = group_counts[i]
        percentage = (count / total_values) * 100
        print(f"Group {i+1} ({lower_bound} - {upper_bound}): {count} values, {percentage:.2f}%")

sort_values_into_groups()
