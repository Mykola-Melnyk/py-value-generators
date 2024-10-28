import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm
import pyperclip

def generate_normal_distribution():
    try:
        def generate_values():
            lower = float(input("Enter lower value: "))
            upper = float(input("Enter upper value: "))
            mean = float(input("Enter mean: "))
            std_dev = float(input("Enter standard deviation: "))
            num_values = int(input("Enter number of values: "))
            digits_after_comma = int(input("Enter number of digits after comma: "))
            create_hist = input("Create histogram (y/n): ").strip().lower() == 'y'

            values = np.random.normal(mean, std_dev, num_values)
            values = values[(values >= lower) & (values <= upper)]

            while len(values) < num_values:
                extra_values = np.random.normal(mean, std_dev, num_values - len(values))
                extra_values = extra_values[(extra_values >= lower) & (extra_values <= upper)]
                values = np.concatenate([values, extra_values])

            return values[:num_values], digits_after_comma, create_hist

        def check_normality(values):
            k_stat, p_value = kstest(values, 'norm', args=(np.mean(values), np.std(values)))
            return p_value > 0.05

        def main():
            while True:
                values, digits_after_comma, create_hist = generate_values()

                if check_normality(values):
                    formatted_values = [f"{value:.{digits_after_comma}f}".replace('.', ',') for value in values]
                    result = "\n".join(formatted_values)
                    pyperclip.copy(result)
                    print(result)
                    print("The generated values follow a normal distribution. They have been copied to the clipboard.")
                    print(f"Total number of values: {len(values)}")
                    print(f"Minimum value: {min(values):.2f}")
                    print(f"Maximum value: {max(values):.2f}")
                    print(f"Mean: {np.mean(values):.2f}")
                    print(f"Standard deviation: {np.std(values):.2f}")
                    print(f"Median: {np.median(values):.2f}")
                    if create_hist:
                        plt.hist(np.round(values), bins='auto', edgecolor='black')
                        plt.xlabel('Value')
                        plt.ylabel('Frequency')
                        plt.title('Histogram of Generated Values')
                        plt.show()
                    break
                else:
                    retry = input("The generated values do not follow a normal distribution. Do you want to try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        break

        if __name__ == "__main__":
            main()

    
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
