# ExifTool Command Parser

## Overview

This project provides a Python script to parse ExifTool commands generated from [ExitNotes](https://github.com/tommi1hirvonen/ExifNotes) app and save the parsed data into Pandas dataframe for further transformations. The script extracts key-value pairs and filenames from each line of the input file.

## Features

- Parses ExifTool commands to extract key-value pairs.
- Extracts filenames matching the pattern `*0.jpg` or `*_0.TIF`.
- Outputs the parsed data into a CSV file using pandas.

## Requirements

- Python 3.x
- pandas
- argparse

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sVathis/exiffilm.git
    cd exiffielm
    ```

2. Install the required Python packages:
    ```sh
    pip install pandas
    ```

## Usage

1. Prepare a text file containing ExifTool commands, with each command on a new line.

2. Run the script with the input file as an argument:
    ```sh
    python exifilm.py input_file.txt
    ```

3. The script will print the parsed data as a pandas DataFrame.
