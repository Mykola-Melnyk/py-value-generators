import matplotlib.pyplot as plt

def parse_input(values_input):
    values = []
    for value in values_input.split():
        try:
            values.append(float(value.replace(',', '.')))
        except ValueError:
            continue
    return values

def sort_values_into_groups(values, num_groups, group_ranges):
    total_values = len(values)
    group_counts = [0] * num_groups

    for value in values:
        for i, (lower_bound, upper_bound) in enumerate(group_ranges):
            if lower_bound <= value < upper_bound:
                group_counts[i] += 1
                break

    return group_counts, total_values

def generate_statistics(group_counts, group_ranges, total_values):
    print(f"\nTotal number of values: {total_values}\n")
    
    for i, (lower_bound, upper_bound) in enumerate(group_ranges):
        count = group_counts[i]
        percentage = (count / total_values) * 100
        print(f"Group {i+1} ({lower_bound} - {upper_bound}): {count} values, {percentage:.2f}%")

def main():
    print("Enter your set of values (separated by new lines or spaces, end with double enter):")
    values_input = []
    while True:
        line = input()
        if line == "":
            break
        values_input.append(line)
    values_input = ' '.join(values_input)
    
    values = parse_input(values_input)
    
    num_groups = int(input("Enter the number of groups: "))
    group_ranges = []

    for i in range(num_groups):
        lower_bound = float(input(f"Enter the lower bound for group {i+1}: "))
        upper_bound = float(input(f"Enter the upper bound for group {i+1}: "))
        group_ranges.append((lower_bound, upper_bound))

    group_counts, total_values = sort_values_into_groups(values, num_groups, group_ranges)
    generate_statistics(group_counts, group_ranges, total_values)

    show_histogram = input("Do you want a histogram (y/n)? ").strip().lower()
    if show_histogram == 'y':
        plt.figure(figsize=(12, 6))

        # Bar chart
        plt.subplot(1, 2, 1)
        plt.bar(range(1, num_groups+1), group_counts, tick_label=[f'Group {i+1}' for i in range(num_groups)])
        plt.xlabel('Groups')
        plt.ylabel('Number of Values')
        plt.title('Number of Values per Group')

        # Pie chart
        plt.subplot(1, 2, 2)
        plt.pie(group_counts, labels=[f'Group {i+1}' for i in range(num_groups)], autopct='%1.1f%%')
        plt.title('Percentage of Values per Group')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
