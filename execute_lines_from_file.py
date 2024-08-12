def extract_lines(input_file, output_file, num_lines):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for i, line in enumerate(infile):
            if i < num_lines:
                outfile.write(line)
            else:
                break

input_file = 'data.txt'
output_file = 'lines.txt'
num_lines = 3  # Укажите количество строк, которые хотите извлечь

extract_lines(input_file, output_file, num_lines)
