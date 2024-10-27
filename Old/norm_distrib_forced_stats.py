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
        hist = input("Do you want to create a histogram? (yes/no): ").strip().lower()
        
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
        
        # Format values
        values = np.round(values, digits)
        df = pd.DataFrame(values, columns=['Values'])

        # Copy to clipboard
        df.to_clipboard(index=False, header=False, sep=',')

        # Output formatted values
        print("Formatted Values:")
        print(df.to_csv(index=False, header=False, sep=','))
        print(f"Total number of values: {len(values)}")
        print(f"Minimum value: {min(values):.2f}")
        print(f"Maximum value: {max(values):.2f}")
        print(f"Mean: {np.mean(values):.2f}")
        print(f"Standard deviation: {np.std(values):.2f}")
        print(f"Median: {np.median(values):.2f}")
        # Generate histogram if needed
        if hist == 'yes':
            rounded_values = np.round(values)
            plt.hist(rounded_values, bins=int(upper-lower), edgecolor='black')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('Histogram of Generated Values')
            plt.show()
    
    except Exception as e:
        print(f"An error occurred: {e}")

generate_normal_distribution()
