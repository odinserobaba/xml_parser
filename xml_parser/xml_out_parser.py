import re
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("replace.log"),
    logging.StreamHandler()
])

def load_replacements(replacements_file):
    replacements = {}
    with open(replacements_file, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Извлекаем ключи и значения из строки
                attributes = eval(line.strip())  # Используйте eval с осторожностью
                print(attributes)
                replacements.update(attributes)
            except Exception as e:
                logging.error(f"Error parsing line: {line.strip()} Exception: {e}")
    return replacements

def replace_values(input_file, output_file, replacements):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        updated_line = line.strip()

        # Заменяем значения на основе словаря replacements
        for key, value in replacements.items():
            print(f"Replacing '{key}' with '{value}'")

            # Убедитесь, что ключ не содержит специальных символов
            key_escaped = re.escape(key)
            print(key_escaped)
            # Создаем шаблон для замены
            
            pattern = rf'({key_escaped}=")(.*?)(")'
            replacement = rf'\1{value}\3'  # Строка замены с использованием групп

            # Попробуем заменить, используя безопасный подход
            try:
                # Заменяем только если ключ присутствует
                if re.search(pattern, updated_line):
                    updated_line = re.sub(pattern, replacement, updated_line)
            except re.error as e:
                logging.error(f"Regex error while replacing '{key}': {e}")

        updated_lines.append(updated_line)

    # Запись обновленных строк в выходной файл
    with open(output_file, 'w', encoding='utf-8') as file:
        for updated_line in updated_lines:
            file.write(updated_line + '\n')

    logging.info(f'Replacement complete. Updated {len(updated_lines)} lines.')

# Задайте пути к входному файлу, файлу замен и выходному файлу
input_file_path = 'output_parser.txt' # Исходный файл
replacements_file_path = 'data1.txt'   # Файл с заменами
output_file_path = 'updated_data.txt'  # Файл для записи обновленных данных

# Запуск процесса замены
replacements = load_replacements(replacements_file_path)
replace_values(input_file_path, output_file_path, replacements)
