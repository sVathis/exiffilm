import pandas as pd
import re


filenamePattern = 'FilenamePattern'
exiftoolCommand = 'exiftool -m'

class ExifToolCommandParser:
    def __init__(self, cmdFile):
        self.pattern_kv = re.compile(r'-([a-zA-Z]+)="([^"]+)"')
        self.pattern_filename = re.compile(r'\*.*\.(jpg|TIF)', re.IGNORECASE)
        self.cmdFile = cmdFile
        self.df = self._read_file()


    # Function to parse a line of exiftool command
    def _parse_exiftool_commands(self, line):
        # Patterns to match key-value pairs and filenames

        matches = self.pattern_kv.findall(line)
        parsed_data = {key: value for key, value in matches}
        
        # Parse the filename
        filename_match = self.pattern_filename.search(line)
        if filename_match:
            parsed_data[filenamePattern] = filename_match.group()

        return parsed_data

    def _read_file(self):
        try:

            with open(self.cmdFile, 'r') as file:
                lines = file.readlines()

            data = [self._parse_exiftool_commands(line) for line in lines if line.strip()]

            return pd.DataFrame(data)

        except Exception as e:
            print(f"Error parsing file: {e}")
            return pd.DataFrame()
        
    def _save_file(self, output_file):
        try:
            with open(output_file, 'w') as file:
                for index, row in self.df.iterrows():
                    command = exiftoolCommand
                    for col in self.df.columns:
                        if col != filenamePattern and pd.notna(row[col]):
                            command += f' -{col}="{row[col]}"'
                    command += f' {row[filenamePattern]}'
                    file.write(command + '\n')
            print(f"Exiftool commands have been written to {output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")
