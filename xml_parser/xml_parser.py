import re
import logging
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("process.log"),
    logging.StreamHandler()
])

def extract_attributes(line):
    # Регулярное выражение для поиска атрибутов в формате name="value"
    pattern = r'(\w+)="([^"]+)"'
    
    # Словарь для хранения найденных атрибутов
    attributes = {}
    
    # Находим все совпадения в строке
    matches = re.findall(pattern, line)
    
    for match in matches:
        key, value = match
        attributes[key] = value
    
    return attributes

def process_file(input_file, output_file):
    results = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_lines = len(lines)  # Общее количество строк
    logging.info(f'Total lines to process: {total_lines}')

    # Обработка файла с отображением прогресса
    for line in tqdm(lines, desc="Processing lines", total=total_lines):
        # Удаляем пробелы в начале и в конце строки
        line = line.strip()

        # Пропускаем пустые строки
        if not line:
            logging.warning('Encountered an empty line.')
            continue

        attributes = extract_attributes(line)

        if attributes:
            results.append(attributes)
        else:
            logging.warning(f'Missing required fields in line: {line}')

    # Запись результатов в выходной файл
    with open(output_file, 'w', encoding='utf-8') as file:
        for record in results:
            file.write(str(record) + '\n')

    logging.info(f'Processing complete. Extracted {len(results)} records.')

# Задайте пути к входному и выходному файлам
input_file_path = 'data1.txt'
output_file_path = 'output_parser.txt'

# Запуск процесса
process_file(input_file_path, output_file_path)
