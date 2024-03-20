import pandas as pd
import os

def xlsx_to_csv(input_folder, output_folder):
    # Check if output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    files = os.listdir(input_folder)

    #  looks through each file
    for file in files:
        if file.endswith('.xlsx'):
            # construct paths for input and output files
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.csv')

            # read excel convert to CSV
            df = pd.read_excel(input_path)

            # Save as CSV
            df.to_csv(output_path, index=False)
            print(f"{file} converted to CSV successfully.")

# Example usage:
input_folder = "input_folder"  # Specify the path to the folder containing .xlsx files
output_folder = "output_folder"  # Specify the path to the folder where .csv files will be saved
xlsx_to_csv(input_folder, output_folder)
