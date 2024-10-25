import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import normaltest

def parse_input(values_input):
    values = []
    for value in values_input.split():
        try:
            values.append(float(value.replace(',', '.')))
        except ValueError:
            continue
    return values

def generate_statistics(values):
        
    sorted_values = sorted(values)
    formatted_values = [f"{value:.2f}".replace('.', ',') for value in sorted_values]
    print("\nValues sorted from smallest to biggest:")
    for val in formatted_values:
        print(val)
        
    k2, p = normaltest(values)
    if p < 0.05:
        print("The given values do NOT represent a normal distribution.")
    else:
        print("The given values represent a normal distribution.")

    
    print(f"Total number of values: {len(values)}")
    print(f"Minimum value: {min(values):.2f}")
    print(f"Maximum value: {max(values):.2f}")
    print(f"Mean: {np.mean(values):.2f}")
    print(f"Standard deviation: {np.std(values):.2f}")
    print(f"Median: {np.median(values):.2f}")

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
    generate_statistics(values)

    show_histogram = input("Do you want a histogram (y/n)? ").strip().lower()
    if show_histogram == 'y':
        plt.hist(values, bins='auto', edgecolor='black')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.title('Histogram of Input Values')
        plt.show()

if __name__ == "__main__":
    main()
