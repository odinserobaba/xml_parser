import re
import pandas as pd
import logging
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='processing_log.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлу
file_path = 'lines.txt'

# Регулярные выражения для извлечения данных
pattern_inn = re.compile(r'ИННЮЛ="(.*?)"')
pattern_kpp = re.compile(r'КПП="(.*?)"')
pattern_kod_pok = re.compile(r'КодПок="(.*?)"')
pattern_prizn_stav = re.compile(r'ПризнСтав="(.*?)"')
pattern_nal_baza = re.compile(r'НалБаза="(.*?)"')
pattern_sum_akciz = re.compile(r'СумАкциз="(.*?)"')
pattern_period = re.compile(r'Период="(.*?)"')
# Инициализация пустого списка для хранения записей
records = []

# Открываем файл и считываем все строки для подсчета
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()

# Обработка файла построчно с tqdm
for line in tqdm(lines, desc="Processing lines", total=len(lines)):
    # Удаляем возможные пробелы и переходы на новую строку
    line = line.strip()
    if not line:
        continue  # Пропускаем пустые строки

    try:
        # Поиск данных в строке с помощью регулярных выражений
        inn = pattern_inn.search(line)
        kpp = pattern_kpp.search(line)

        if inn and kpp:
            inn = inn.group(1)
            kpp = kpp.group(1)

            # Обрабатываем операционные коды
            kod_pok_matches = pattern_kod_pok.findall(line)
            prizn_stav_matches = pattern_prizn_stav.findall(line)
            nal_baza_matches = pattern_nal_baza.findall(line)
            sum_akciz_matches = pattern_sum_akciz.findall(line)
            period = pattern_period.findall(line)
            # prizn_srok = pattern_kod_srok_upl.findall(line)
            if kod_pok_matches:
                for period,kod_pok, prizn_stav, nal_baza, sum_akciz in zip(
                        period,
                        kod_pok_matches,
                        prizn_stav_matches,
                        nal_baza_matches,
                        sum_akciz_matches):
                    records.append({
                        'ИННЮЛ': inn,
                        'КПП': kpp,
                        'КодПок': kod_pok,
                        'Период': period,
                        'ПризнСтав': prizn_stav,
                        'НалБаза': float(nal_baza) if nal_baza else 0.0,
                        'СумАкциз': float(sum_akciz) if sum_akciz else 0.0,
                    })
            else:
                logging.warning(f"No KodPok found in line: {line}")
        else:
            logging.warning(f"Missing required fields in line: {line}")
    except Exception as e:
        logging.error(f"Error processing line: {line}\nException: {e}")

# Создаем DataFrame из записей
df = pd.DataFrame(records)

# Проверяем, были ли добавлены записи
if df.empty:
    logging.info("No records were created. Please check the input data and structure.")
    print("No records were created. Please check the input data and structure.")
else:
    logging.info("Records successfully created.")
    print("Records successfully created.")
    print(df.head())

    # Агрегируем данные по ИННЮЛ, КПП, КодПок, ПризнСтав
    aggregated_df = df.groupby(['ИННЮЛ', 'КПП', 'КодПок', 'Период','ПризнСтав']).agg({'НалБаза': 'size', 'СумАкциз': 'sum'}).reset_index()
    aggregated_df['Сумма НалБаза + СумАкциз'] = aggregated_df['НалБаза'] + aggregated_df['СумАкциз']

    # Выводим агрегированные данные
    print(aggregated_df.head())

    # Сохраняем подробные данные и агрегированные данные в файлы
    df.to_csv('output_detailed.csv', index=False)
    aggregated_df.to_csv('output_aggregated.csv', index=False)

    # Сохранение файла с суммами по признакам ИННЮЛ, КПП, КодПок, ПризнСтав
    grouped_sum_df = df.groupby(['ИННЮЛ', 'КПП','КодПок','Период', 'ПризнСтав']).agg({'НалБаза': 'size','СумАкциз': 'sum'}).reset_index()
    grouped_sum_df.to_csv('grouped_sum_output.csv', index=False)
    logging.info("Processing completed successfully.")
