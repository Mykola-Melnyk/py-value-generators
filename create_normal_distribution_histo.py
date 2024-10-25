import numpy as np
import matplotlib.pyplot as plt
import pyperclip

def generate_normal_distribution():
    lower_value = float(input("Enter lower value: "))
    upper_value = float(input("Enter upper value: "))
    mean = float(input("Enter mean: "))
    std_dev = float(input("Enter standard deviation: "))
    num_values = int(input("Enter the number of values: "))
    num_digits = int(input("Enter the number of digits after comma: "))
    create_histogram = input("Create histogram (y / n): ").strip().lower()
    
    values = np.random.normal(loc=mean, scale=std_dev, size=num_values)
    
    # Clip values to be within the specified range
    values = np.clip(values, lower_value, upper_value)
    
    formatted_values = [f"{value:.{num_digits}f}".replace('.', ',') for value in values]
    
    output = "\n".join(formatted_values)
    pyperclip.copy(output)
    
    print("\nGenerated values (copied to clipboard):")
    print(output)
    
    if create_histogram == 'y':
        plt.hist([round(value) for value in values], bins=range(int(lower_value), int(upper_value) + 1), edgecolor='black')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Histogram of Generated Values')
        plt.show()

generate_normal_distribution()
