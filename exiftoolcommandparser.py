import pandas as pd
import re


filenamePattern = 'FilenamePattern'
exiftoolCommand = 'exiftool -m'

class ExifToolCommandParser:
    def __init__(self, cmdFile, offset=0):
        self.pattern_kv = re.compile(r'-([a-zA-Z]+)="([^"]+)"')
        self.pattern_filename = re.compile(r'\*.*\.(jpg|TIF)', re.IGNORECASE)
        self.cmdFile = cmdFile
        self.df = self._read_commands()
        self.preprocess(offset=offset)


    # Function to parse a line of exiftool command
    def _parse_commands(self, line):
        # Patterns to match key-value pairs and filenames

        matches = self.pattern_kv.findall(line)
        parsed_data = {key: value for key, value in matches}
        
        # Parse the filename
        filename_match = self.pattern_filename.search(line)
        if filename_match:
            filename = filename_match.group()
            parsed_data[filenamePattern] = filename

        return parsed_data

    def _read_commands(self):
        try:

            with open(self.cmdFile, 'r') as file:
                lines = file.readlines()

            data = [self._parse_commands(line) for line in lines if line.strip()]

            return pd.DataFrame(data)

        except Exception as e:
            print(f"Error parsing file: {e.message}")
            return pd.DataFrame()


    def preprocess(self, offset=0):
        # Extract numeric value from FilenamePattern and store in PhotoID
        def extract_photo_id(filename, offset=0):
            numeric_match = re.search(r'_(\d+)\.(TIF|tif|JPG|jpg)', filename)
            if numeric_match:
                return str(int(numeric_match.group(1)) + offset).zfill(2)
            return None

        self.df['PhotoID'] = self.df[filenamePattern].apply(lambda x: extract_photo_id(x,offset=offset) if pd.notna(x) else None)
        self.df['PhotoID'].attrs = {'private': True}
        self.df[filenamePattern].attrs = {'private': True}

    def _save_commands(self, output_file):
        try:
            with open(output_file, 'w') as file:
                for index, row in self.df.iterrows():
                    command = exiftoolCommand
                    for col in self.df.columns:
                        if col != filenamePattern and pd.notna(row[col]):
                            if not self.df[col].attrs.get('private', False):
                                command += f' -{col}="{row[col]}"'
                    command += f' {row[filenamePattern]}'
                    file.write(command + '\n')
            print(f"Exiftool commands have been written to {output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")
