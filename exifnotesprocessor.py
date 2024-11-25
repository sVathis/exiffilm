import argparse
from exifnotescommandparser import ExifNotesCommandParser

def main():
    parser = argparse.ArgumentParser(description='Process a file with ExifToolCommandParser and save commands to a .sh file.')
    parser.add_argument('filename', help='The input filename')
    parser.add_argument('number', type=int, help='A number to create the output filename with .sh extension')
    args = parser.parse_args()

    parser = ExifNotesCommandParser(args.filename, str(args.number))
    output_file = f"{args.number}.sh"
    parser.save_commands(output_file)

if __name__ == "__main__":
    main()