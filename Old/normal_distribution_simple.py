import numpy as np

def generate_normal_distribution():
    lower_value = float(input("Enter lower value: "))
    upper_value = float(input("Enter upper value: "))
    mean = float(input("Enter mean: "))
    std_dev = float(input("Enter standard deviation: "))
    num_values = int(input("Enter the number of values: "))
    num_digits = int(input("Enter the number of digits after comma: "))
    
    values = np.random.normal(loc=mean, scale=std_dev, size=num_values)
    
    # Clip values to be within the specified range
    values = np.clip(values, lower_value, upper_value)
    
    formatted_values = [f"{value:.{num_digits}f}".replace('.', ',') for value in values]
    
    print("\nGenerated values:")
    for val in formatted_values:
        print(val)

generate_normal_distribution()
