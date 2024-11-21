import re
import pandas as pd
import argparse

# Define the regex pattern to parse exiftool commands
pattern = re.compile(r'-([a-zA-Z]+)="([^"]+)"')

# Patterns to match key-value pairs and filenames
pattern_kv = re.compile(r'-([a-zA-Z]+)="([^"]+)"')
pattern_filename = re.compile(r'\*.*\.(jpg|TIF)', re.IGNORECASE)

# Function to parse a line of exiftool command
def parse_exiftool_command(line):
    matches = pattern_kv.findall(line)
    parsed_data = {key: value for key, value in matches}
    
    # Parse the filename
    filename_match = pattern_filename.search(line)
    if filename_match:
        parsed_data['Filename'] = filename_match.group()
    
    return parsed_data

# Set up argument parser
parser = argparse.ArgumentParser(description='Parse exiftool commands from a file and save to a CSV.')
parser.add_argument('input_file', help='Path to the input file')
#parser.add_argument('output_file', help='Path to the output CSV file')
args = parser.parse_args()

# Read the input file
with open(args.input_file, 'r') as file:
    lines = file.readlines()

# Parse each line and collect the data, disregarding empty lines
data = [parse_exiftool_command(line) for line in lines if line.strip()]

# Create a pandas DataFrame
df = pd.DataFrame(data)

print(df)

# Generate the output file with exiftool commands
output_file = 'output_exiftool_commands.txt'
with open(output_file, 'w') as file:
    for index, row in df.iterrows():
        command = 'exiftool -m'
        for col in df.columns:
            if col != 'Filename' and pd.notna(row[col]):
                command += f' -{col}="{row[col]}"'
        command += f' {row["Filename"]}'
        file.write(command + '\n')

print(f"Exiftool commands have been written to {output_file}")

# Save the DataFrame to a CSV file
#df.to_csv(args.output_file, index=False)

#print("Data has been parsed and saved to", args.output_file)