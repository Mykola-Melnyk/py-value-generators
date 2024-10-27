import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm
import pyperclip

def generate_normal_distribution():
    try:
        lower = float(input("Enter the lower value: "))
        upper = float(input("Enter the upper value: "))
        mean = float(input("Enter the mean: "))
        std_dev = float(input("Enter the standard deviation: "))
        num_values = int(input("Enter the number of values: "))
        digits = int(input("Enter the number of digits after comma: "))
        hist = input("Do you want to create a histogram? (y/n): ").strip().lower()
        
        while True:
            values = np.random.normal(mean, std_dev, num_values)
            values = values[(values >= lower) & (values <= upper)]
            
            # Check number of values
            while len(values) < num_values:
                additional_values = np.random.normal(mean, std_dev, num_values - len(values))
                additional_values = additional_values[(additional_values >= lower) & (additional_values <= upper)]
                values = np.append(values, additional_values)
            
            # Perform Kolmogorov-Smirnov test
            ks_stat, p_value = kstest(values, 'norm', args=(mean, std_dev))
            if p_value >= 0.05:
                print("Generated values follow a normal distribution")
                break
            print("Generated values do not follow a normal distribution. Generating again...")

        # Output formatted values
        formatted_values = [f"{value:.{digits}f}".replace('.', ',') for value in values]
        output = "\n".join(formatted_values)
        pyperclip.copy(output)
        print("\nGenerated values (copied to clipboard):")
        print(output)
        print(f"Total number of values: {len(values)}")
        print(f"Minimum value: {min(values):.2f}")
        print(f"Maximum value: {max(values):.2f}")
        print(f"Mean: {np.mean(values):.2f}")
        print(f"Standard deviation: {np.std(values):.2f}")
        print(f"Median: {np.median(values):.2f}")
        # Generate histogram if needed
        if hist == 'y':
            rounded_values = np.round(values)
            plt.hist(rounded_values, bins=int(upper-lower), edgecolor='black')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('Histogram of Generated Values')
            plt.show()
    
    except Exception as e:
        print(f"An error occurred: {e}")

def sort_ranges():
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


def main():
    print("Choose a functionality to execute:")
    print("1. Generate normal distribution")
    print("2. Sort values into ranges and analyze them")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        generate_normal_distribution()
    elif choice == '2':
        sort_ranges()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
