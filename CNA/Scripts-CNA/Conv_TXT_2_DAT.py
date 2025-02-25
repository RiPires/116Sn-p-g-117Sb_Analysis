import os
import glob

def convert_txt_to_dat(filename):
    """Reads a .txt file with one column of numbers and writes a .dat file with two columns: index and value."""
    with open(filename, 'r') as infile:
        lines = infile.readlines()
    
    # Clean and convert lines to numbers
    numbers = [line.strip() for line in lines if line.strip()]
    
    # Create the output filename with .dat extension
    base_name, _ = os.path.splitext(filename)
    output_filename = base_name + ".dat"

    # Write to the new file
    with open(output_filename, 'w') as outfile:
        for index, value in enumerate(numbers, start=1):
            outfile.write(f"{index} {value}\n")

    print(f"Converted {filename} to {output_filename}")

# Convert all .txt files in the directory
txt_files = glob.glob("*.txt")  # List all .txt files in the directory

for txt_file in txt_files:
    convert_txt_to_dat(txt_file)

print("Conversion completed for all .txt files.")
