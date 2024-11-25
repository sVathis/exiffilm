import pandas as pd
import re
import shlex
import exiftool
import logging

logging.basicConfig(level=logging.DEBUG)

filenamePattern = 'FilenamePattern'
defaultParameters = '-m -progress -charset utf8 -LensType=MF'
defaultParametersList = shlex.split(defaultParameters)
exiftoolCommand = 'exiftool ' + defaultParameters


class ExifNotesCommandParser:
    def __init__(self, cmdFile, filmid, offset=0,):
        self.pattern_kv = re.compile(r'-([a-zA-Z]+)="([^"]+)"')
        self.pattern_filename = re.compile(r'\*.*\.(jpg|TIF)', re.IGNORECASE)
        self.filmid = filmid
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
                return str(int(numeric_match.group(1)) + offset).zfill(4)
            return None

        def extract_file_extension(filename):
            extension_match = re.search(r'\.(TIF|tif|JPG|jpg)$', filename)
            if extension_match:
                return extension_match.group(1)
            return None

        self.df['FileExtension'] = self.df[filenamePattern].apply(lambda x: extract_file_extension(x) if pd.notna(x) else None)
        self.df['PhotoID'] = self.df[filenamePattern].apply(lambda x: extract_photo_id(x,offset=offset) if pd.notna(x) else None)
        self.df['Filename'] = self.filmid + self.df['PhotoID'] 

        # Remove the string "Nikon" from the "Lens" column if it exists
        if 'Lens' in self.df.columns:
            self.df['Lens'] = self.df['Lens'].str.replace('Nikon ', '', regex=False)

        # Rename 'ImageDescription' column to 'Title'
        if 'ImageDescription' in self.df.columns:
            self.df.rename(columns={'ImageDescription': 'Title'}, inplace=True)

        self.df[filenamePattern].attrs = {'private': True}
        self.df['PhotoID'].attrs = {'private': True}
        self.df['FileExtension'].attrs = {'private': True}        
        self.df['Filename'].attrs = {'private': True}

    def save_commands(self, output_file):
        try:
            with open(output_file, 'w') as file:
                for index, row in self.df.iterrows():
                    command = exiftoolCommand
                    for col in self.df.columns:
                        if  pd.notna(row[col]):
                            if not self.df[col].attrs.get('private', False):
                                command += f' -{col}="{row[col]}"'
                    command += f' {row["Filename"]}.xmp'
                    file.write(command + '\n')
            print(f"Exiftool commands have been written to {output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def get_row_as_command_list(self, index):
        row = self.df.iloc[index]
        row_list = []
        for col in self.df.columns:
            if pd.notna(row[col]):
                if not self.df[col].attrs.get('private', False):
                    row_list.append(f'-{col}={row[col]}')
        row_list.append(row['Filename'])
        return row_list

    def run_command(self, index=0):
        row_list = self.get_row_as_command_list(index=index)
        params =  defaultParametersList + row_list
        print(params)
        # with exiftool.ExifTool() as et:
        #     et.execute(*params)
        with exiftool.ExifToolHelper(logger=logging.getLogger(__name__)) as et:
                #et.execute(*params)
                pass

        
    def __str__(self):
        return self.df.to_string()
    
    def __repr__(self):
        return self.df.to_string()
    
