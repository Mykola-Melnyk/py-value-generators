import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import kstest, norm
import pyperclip
import random
import re
import statistics
from collections import Counter

def generate_normal_distribution():
    try:
        def generate_values():
            lower = float(input("\nEnter lower value: "))
            upper = float(input("Enter upper value: "))
            mean = float(input("Enter mean: "))
            std_dev = float(input("Enter standard deviation: "))
            num_values = int(input("Enter number of values: "))
            dec_sep = input("Select decimal separator (./,): ")
            digits_after_comma = int(input("Enter number of digits after comma: "))
            create_hist = input("Create histogram (y/n): ").strip().lower() == 'y'

            values = np.random.normal(mean, std_dev, num_values)
            values = values[(values >= lower) & (values <= upper)]

            while len(values) < num_values:
                extra_values = np.random.normal(mean, std_dev, num_values - len(values))
                extra_values = extra_values[(extra_values >= lower) & (extra_values <= upper)]
                values = np.concatenate([values, extra_values])

            return values[:num_values], digits_after_comma, create_hist, dec_sep

        def check_normality(values):
            k_stat, p_value = kstest(values, 'norm', args=(np.mean(values), np.std(values)))
            return p_value > 0.05

        def main():
            while True:
                values, digits_after_comma, create_hist, dec_sep = generate_values()

                if check_normality(values):
                    formatted_values = [f"{value:.{digits_after_comma}f}".replace('.', ',') for value in values]
                    result = "\n".join(formatted_values)
                    dot_formatted_values = [f"{value:.{digits_after_comma}f}" for value in values]
                    dot_result = "\n".join(dot_formatted_values)

                    if dec_sep == '.':
                        pyperclip.copy(dot_result)
                        print(dot_result)
                    elif dec_sep == ',':
                        pyperclip.copy(result)
                        print(result)
                    else:
                        print("\nInvalid choice. Using '.' as separator. \n")
                        pyperclip.copy(dot_result)
                        print(dot_result)

                    print("\nThe generated values follow a normal distribution. They have been copied to the clipboard.\n")
                    print(f"Total number of values: {len(values)}")
                    print(f"Minimum value: {min(values):.2f}")
                    print(f"Maximum value: {max(values):.2f}")
                    print(f"Mean: {np.mean(values):.2f}")
                    print(f"Standard deviation: {np.std(values):.2f}")
                    print(f"Median: {np.median(values):.2f}\n")
                    if create_hist:
                        plt.hist(np.round(values), bins='auto', edgecolor='black')
                        plt.xlabel('Value')
                        plt.ylabel('Frequency')
                        plt.title('Histogram of Generated Values')
                        plt.show()
                    break
                else:
                    retry = input("\nThe generated values do not follow a normal distribution. Do you want to try again? (y/n): \n").strip().lower()
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
                if lower_bound <= value <= upper_bound:
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
        print("\nEnter your set of values (separated by new lines or spaces, end with double enter):")
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
            lower_bound = float(input(f"Enter the lower bound (inclusive) for group {i+1}: "))
            upper_bound = float(input(f"Enter the upper bound (inclusive) for group {i+1}: "))
            group_ranges.append((lower_bound, upper_bound))

        show_histogram = input("Do you want a histogram (y/n)? ").strip().lower()

        group_counts, total_values = sort_values_into_groups(values, num_groups, group_ranges)
        generate_statistics(group_counts, group_ranges, total_values)

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

def generate_values():
    # Step 1: Ask for the number of values to generate
    total_values = int(input("\nEnter the number of values to generate: "))
    
    # Step 2: Ask for the number of value types
    num_value_types = int(input("Enter the number of value types: "))
    
    value_types = []
    percentages = []
    
    # Step 3: Ask for the definition of each value type and their percentages
    for i in range(num_value_types):
        value_type = input(f"Enter the definition for value type {i+1}: ")
        value_types.append(value_type)
        if i < num_value_types - 1:
            percentage = float(input(f"Enter the percentage for value type {i+1} (0-100): "))
            percentages.append(percentage / 100)
        else:
            # Automatically calculate the percentage for the last value type
            remaining_percentage = 1 - sum(percentages)
            percentages.append(remaining_percentage)
            print(f"The automatically calculated percentage for value type {i+1} is: {remaining_percentage * 100:.2f}%")
    
    # Generate the values
    generated_values = []
    for value_type, percentage in zip(value_types, percentages):
        count = int(total_values * percentage)
        generated_values.extend([value_type] * count)
    
    # If there are any remaining due to rounding, add them to the last value type
    remaining = total_values - len(generated_values)
    generated_values.extend([value_types[-1]] * remaining)
    
    # Shuffle the values
    random.shuffle(generated_values)
    
    # Output the results
    formatted_values = [str(value).replace('.', ',') for value in generated_values]
    output = "\n".join(formatted_values)
    
    # Copy to clipboard
    pyperclip.copy(output)
    
    print("Results copied to clipboard:")
    print(output)
    
    # Display summary
    print("\nSummary:")
    actual_counts = {value_type: generated_values.count(value_type) for value_type in value_types}
    for value_type, count in actual_counts.items():
        actual_percentage = (count / total_values) * 100
        print(f"{value_type}: {count} values, {actual_percentage:.2f}%")

    print(f"\nTotal number of generated values: {total_values}")

def analyze_values():
    
    # Prompt the user to enter values
    print("\nEnter values (digits, symbols, letters) separated by spaces, commas, or new lines. End with a blank line.\n")

    # Read input until a blank line is entered
    input_data = ""
    while True:
        line = input()
        if line.strip() == "":
            break
        input_data += line + " "

    # Split the input data into values
    values = re.split(r'[,\s]+', input_data.strip())
    
    # Count the total number of values
    num_values = len(values)
    
    # Count the number of each same value
    value_counts = Counter(values)
    
    # Display the results
    print(f"Total number of values: {num_values}\n")
    for value, count in value_counts.items():
        percentage = (count / num_values) * 100
        print(f"Value: {value}, Count: {count}, Percentage: {percentage:.2f}%\n")

def generate_random():
    def generate_random_values(num_values, min_value, max_value, decimal_places):
        values = [round(random.uniform(min_value, max_value), decimal_places) for _ in range(num_values)]
        return values

    def main():
        # User inputs
        num_values = int(input("\nEnter the number of values: "))
        min_value = float(input("Enter the minimum value: "))
        max_value = float(input("Enter the maximum value: "))
        decimal_places = int(input("Enter the number of digits after comma: "))
        create_histogram = input("Would you like to create a histogram? (y/n): ").strip().lower()
        dec_sep = input("Select decimal separator (./,): ")

        # Generate random values
        values = generate_random_values(num_values, min_value, max_value, decimal_places)

        # Calculate statistics
        min_val = min(values)
        max_val = max(values)
        mean_val = statistics.mean(values)
        std_dev = statistics.stdev(values)
        median_val = statistics.median(values)

        # Display results
        if dec_sep == '.':
            print("\nGenerated Values:\n")
            for value in values:
                print(f"{value:.{decimal_places}f}")
            
            print(f"\nNumber of values: {num_values}")
            print(f"Minimum value: {min_val:.{decimal_places}f}")
            print(f"Maximum value: {max_val:.{decimal_places}f}")
            print(f"Mean value: {mean_val:.{decimal_places}f}")
            print(f"Standard deviation: {std_dev:.{decimal_places}f}")
            print(f"Median value: {median_val:.{decimal_places}f}\n")

            # Copy results to clipboard
            result_str = "\n".join([f"{value:.{decimal_places}f}" for value in values])
            pyperclip.copy(result_str)
            print("Results have been copied to the clipboard.\n")
        elif dec_sep == ',':
            print("\nGenerated Values:\n")
            for value in values:
                print(f"{value:.{decimal_places}f}".replace('.', ','))
            
            print(f"\nNumber of values: {num_values}")
            print(f"Minimum value: {min_val:.{decimal_places}f}".replace('.', ','))
            print(f"Maximum value: {max_val:.{decimal_places}f}".replace('.', ','))
            print(f"Mean value: {mean_val:.{decimal_places}f}".replace('.', ','))
            print(f"Standard deviation: {std_dev:.{decimal_places}f}".replace('.', ','))
            print(f"Median value: {median_val:.{decimal_places}f}\n".replace('.', ','))

            # Copy results to clipboard
            result_str = "\n".join([f"{value:.{decimal_places}f}".replace('.', ',') for value in values])
            pyperclip.copy(result_str)
            print("Results have been copied to the clipboard.\n")
        else:
            print("\nInvalid choice. Using '.' as separator. \n")
            print("Generated Values:\n")
            for value in values:
                print(f"{value:.{decimal_places}f}")
            
            print(f"\nNumber of values: {num_values}")
            print(f"Minimum value: {min_val:.{decimal_places}f}")
            print(f"Maximum value: {max_val:.{decimal_places}f}")
            print(f"Mean value: {mean_val:.{decimal_places}f}")
            print(f"Standard deviation: {std_dev:.{decimal_places}f}")
            print(f"Median value: {median_val:.{decimal_places}f}\n")

            # Copy results to clipboard
            result_str = "\n".join([f"{value:.{decimal_places}f}" for value in values])
            pyperclip.copy(result_str)
            print("Results have been copied to the clipboard.\n")

        if create_histogram == "y":
            # Plot histogram
            plt.hist(values, bins=10, edgecolor='black')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('Histogram of Generated Values')
            plt.grid(True)
            plt.show()

    if __name__ == "__main__":
        main()

def generate_ranges():
    def generate_random_values(num_values, ranges, decimal_places):
        values = []
        range_info = []

        for lower, upper, percentage in ranges:
            range_count = round(num_values * percentage / 100)
            range_values = [
                round(random.uniform(lower, upper), decimal_places)
                for _ in range(range_count)
            ]
            values.extend(range_values)
            range_info.append((lower, upper, percentage, range_values))

        # Adjust the number of values to match exactly num_values
        while len(values) < num_values:
            values.append(round(random.uniform(ranges[0][0], ranges[-1][1]), decimal_places))
        values = values[:num_values]  # Truncate the list if it exceeds num_values
        random.shuffle(values)
        return values, range_info

    def calculate_actual_percentages(values, ranges):
        range_counts = [0] * len(ranges)
        for value in values:
            for i, (lower, upper, _) in enumerate(ranges):
                if lower <= value <= upper:
                    range_counts[i] += 1
                    break
        return [(count / len(values)) * 100 for count in range_counts]

    def main():
        # User inputs
        num_values = int(input("Enter the total number of values: "))
        num_ranges = int(input("Enter the number of value ranges: "))

        ranges = []
        for i in range(num_ranges):
            lower = float(input(f"Enter the lower bound (inclusive) for range {i+1}: "))
            upper = float(input(f"Enter the upper bound (inclusive) for range {i+1}: "))
            percentage = float(input(f"Enter the percentage for range {i+1}: "))
            ranges.append((lower, upper, percentage))

        decimal_separator = input("Enter the decimal separator you want to use ('.' or ','): ").strip().lower()
        if decimal_separator not in ['.', ',']:
            decimal_separator = '.'

        decimal_places = int(input("Enter the number of digits after the comma: "))
        show_histogram = input("Do you want to show a histogram of the results (y/n)? ").strip().lower() == 'y'

        # Generate random values
        values, range_info = generate_random_values(num_values, ranges, decimal_places)

        # Calculate actual percentages
        actual_percentages = calculate_actual_percentages(values, ranges)

        # Display results
        print("\nGenerated Values:")
        formatted_values = [f"{value:.{decimal_places}f}".replace('.', ',' if decimal_separator == ',' else '.') for value in values]
        for value in formatted_values:
            print(value)

        # Copy results to clipboard
        result_str = "\n".join(formatted_values)
        pyperclip.copy(result_str)
        print("\nResults have been copied to the clipboard.")

        # Show summary info
        print(f"\nTotal number of generated values: {num_values}")
        for i, (lower, upper, percentage, range_values) in enumerate(range_info):
            actual_percentage = actual_percentages[i]
            print(f"\nRange [{lower}, {upper}] (Expected: {percentage}%, Actual: {actual_percentage:.2f}%):")
            print(f"  Number of values: {len(range_values)}")
            print(f"  Minimum value: {min(range_values):.{decimal_places}f}".replace('.', ',' if decimal_separator == ',' else '.'))
            print(f"  Maximum value: {max(range_values):.{decimal_places}f}".replace('.', ',' if decimal_separator == ',' else '.'))
            print(f"  Mean value: {sum(range_values)/len(range_values):.{decimal_places}f}".replace('.', ',' if decimal_separator == ',' else '.'))

        # Show histogram if required
        if show_histogram:
            plt.hist(values, bins=10, edgecolor='black')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('Histogram of Generated Values')
            plt.grid(True)
            plt.show()

    if __name__ == "__main__":
        main()

def continue_number_set():
    def get_user_input():
        values = []
        print("Enter values separated by spaces or new lines, and end with double new line:")
        while True:
            line = input()
            if line == "":
                break
            values.extend(map(float, line.split()))
        return values

    def get_required_count():
        total_values_needed = int(input("Enter the total number of values needed: "))
        return total_values_needed

    def analyze_distribution(values):
        k2, p = stats.normaltest(values)
        return p > 0.05  # If p > 0.05, we assume normal distribution

    def calculate_decimal_places(values):
        return max(len(str(value).split(".")[1]) if "." in str(value) else 0 for value in values)

    def generate_normal_values(mean, std, min_val, max_val, count, decimal_places):
        values = np.random.normal(mean, std, count)
        values = np.clip(values, min_val, max_val)
        return np.round(values, decimal_places)

    def generate_random_values(mean, median, min_val, max_val, count, decimal_places):
        values = np.random.uniform(min_val, max_val, count)
        adjusted_values = (values - np.mean(values)) + mean  # Adjust mean
        adjusted_values = np.clip(adjusted_values, min_val, max_val)
        return np.round(adjusted_values, decimal_places)

    def copy_to_clipboard(data):
        pyperclip.copy("\n".join(map(str, data)))
        print("New values copied to clipboard.")

    def main():
        # Step 1: Get user input
        values = get_user_input()
        print(f"Initial values: {values}")

        # Step 2: Get required count
        total_values_needed = get_required_count()
        num_new_values = total_values_needed - len(values)
        print(f"Total number of values needed: {total_values_needed}")
        print(f"Number of new values to generate: {num_new_values}")

        # Step 3: Analyze distribution
        is_normal = analyze_distribution(values)
        print(f"Values follow normal distribution: {is_normal}")

        # Step 4: Calculate decimal places
        decimal_places = calculate_decimal_places(values)
        print(f"Number of decimal places to retain: {decimal_places}")

        min_val, max_val = np.min(values), np.max(values)

        if is_normal:
            # Step 5: Generate new normal values
            mean, std = np.mean(values), np.std(values)
            print(f"Minimum: {min_val}, Maximum: {max_val}, Mean: {mean}, Standard Deviation: {std}")
            new_values = generate_normal_values(mean, std, min_val, max_val, num_new_values, decimal_places)
        else:
            # Step 6: Generate new random values
            mean, median = np.mean(values), np.median(values)
            print(f"Minimum: {min_val}, Maximum: {max_val}, Mean: {mean}, Median: {median}")
            new_values = generate_random_values(mean, median, min_val, max_val, num_new_values, decimal_places)
        
        # Step 7: Output the new values
        print("New values:")
        for value in new_values:
            print(value)
        
        # Step 8: Copy new values to clipboard
        copy_to_clipboard(new_values)

    if __name__ == "__main__":
        main()

def continue_char_set():
    def get_user_input():
        values = []
        print("Enter values separated by spaces or new lines, and end with double new line:")
        while True:
            line = input()
            if line == "":
                break
            values.extend(line.split())
        return values

    def get_required_count():
        total_values_needed = int(input("Enter the total number of values needed: "))
        return total_values_needed

    def analyze_values(values):
        count = Counter(values)
        total_values = len(values)
        analysis = {value: (freq, (freq / total_values)) for value, freq in count.items()}
        return analysis

    def create_new_values(analysis, num_new_values):
        new_values = []
        remaining_values = num_new_values

        for value, (freq, proportion) in analysis.items():
            num_to_generate = int(proportion * num_new_values)
            new_values.extend([value] * num_to_generate)
            remaining_values -= num_to_generate

        # Adjust to ensure the exact number of values
        while remaining_values > 0:
            for value in analysis.keys():
                if remaining_values > 0:
                    new_values.append(value)
                    remaining_values -= 1
                else:
                    break

        random.shuffle(new_values)
        return new_values

    def copy_to_clipboard(data):
        pyperclip.copy("\n".join(map(str, data)))
        print("New values copied to clipboard.")

    def main():
        # Step 1: Get user input
        values = get_user_input()
        print(f"Initial values: {values}")

        # Step 2: Get required count
        total_values_needed = get_required_count()
        num_new_values = total_values_needed - len(values)
        print(f"Total number of values needed: {total_values_needed}")
        print(f"Number of new values to generate: {num_new_values}")

        # Step 3: Analyze values
        analysis = analyze_values(values)
        print("Value analysis (value: (frequency, percent)):")
        for value, (freq, percent) in analysis.items():
            print(f"{value}: ({freq}, {percent*100:.2f}%)")

        # Step 4: Create new values
        new_values = create_new_values(analysis, num_new_values)

        # Step 5: Output the new values
        print("New values:")
        for value in new_values:
            print(value)

        # Step 6: Copy new values to clipboard
        copy_to_clipboard(new_values)

    if __name__ == "__main__":
        main()

def analyze_data_set():
    def main():
        print("Enter values separated by spaces or new lines, and end with a double new line (press Enter twice):")
        user_input = []
        while True:
            line = input().strip()
            if line == "":
                break
            user_input.extend(line.split())
        
        values = np.array(user_input, dtype=float)
        num_values = len(values)
        
        # Descriptive statistics
        mean = np.mean(values)
        std_dev = np.std(values)
        minimum = np.min(values)
        maximum = np.max(values)
        median = np.median(values)
        
        print(f"\nNumber of values: {num_values}")
        
        # Test for normality using the Shapiro-Wilk test
        shapiro_test = stats.shapiro(values)
        print("\nShapiro-Wilk Test:")
        print(f"Test Statistic: {shapiro_test.statistic}")
        print(f"P-value: {shapiro_test.pvalue}")
        
        if shapiro_test.pvalue > 0.05:
            print("\nThe data follows a normal distribution (fail to reject the null hypothesis).")
            print("\nStatistics for Normally Distributed Data:")
            print(f"Mean: {mean}")
            print(f"Standard Deviation: {std_dev}")
            print(f"Minimum Value: {minimum}")
            print(f"Maximum Value: {maximum}")
        else:
            print("\nThe data does not follow a normal distribution (reject the null hypothesis).")
            print("\nStatistics for Non-Normally Distributed Data:")
            print(f"Mean: {mean}")
            print(f"Median: {median}")
            print(f"Minimum Value: {minimum}")
            print(f"Maximum Value: {maximum}")

    if __name__ == "__main__":
        main()

def main():
    while True:
        print("""\nChoose a functionality to execute:\n
1. Generate normal distribution
2. Sort values into ranges and analyze them
3. Generate custom values by their percentage
4. Analyze custom values for their count and percentage
5. Generate random values
6. Generate random values in ranges with specific boundaries and percentages
7. Continue a given set of numerical values
8. Continue a given set of character values
9. Analyze a given set of values for normality and descriptive statistics
0. Exit\n""")
        choice = input("Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9 or 0): \n\n")
        
        if choice == '1':
            generate_normal_distribution()
        elif choice == '2':
            sort_ranges()
        elif choice == '3':
            generate_values()
        elif choice == '4':
            analyze_values()
        elif choice == '5':
            generate_random()
        elif choice == '6':
            generate_ranges()
        elif choice == '7':
            continue_number_set()
        elif choice == '8':
            continue_char_set()
        elif choice == '9':
            analyze_data_set()
        elif choice == '0':
            print("\nExiting the program. Goodbye!\n")
            break             
        else:
            print("\nInvalid choice. Choose 1, 2, 3, 4, 5, 6, 7, 8, 9 or 0\n")

if __name__ == "__main__":
    main()
