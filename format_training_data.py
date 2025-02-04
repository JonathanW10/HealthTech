import csv
import re

def format_csv_input(input_file, output_file):
	with open(input_file, mode='r', newline='', encoding='utf-8', errors = 'replace') as infile:
		reader = csv.reader(infile)
		
		# Prepare the output data
		formatted_lines = []
		
		for row in reader:
			for cell in row:
				# Use regex to find text between the quotation marks
				matches = re.findall(r'{(.*?)}', cell)
					
				# If matches are found, format them as required
				if len(matches) > 1:
					for i in range(0, len(matches), 2):
						# Pair each question with its answer
						formatted_lines.append(f"- - {matches[i]}")
						if i + 1 < len(matches):
							formatted_lines.append(f"  - {matches[i + 1]}")
			
			# Write the formatted lines to the output file
			with open(output_file, mode='w', newline='', encoding='utf-8', errors='replace') as outfile:
				for line in formatted_lines:
					outfile.write(f"{line}\n")

# Example usage
input_file = 'health_training_data2.csv'  # Your input CSV file
output_file = 'formatted_health_training2.yml'  # Your desired output file
#format_csv_input(input_file, output_file)
