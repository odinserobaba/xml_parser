import os
import re
import logging
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='processing_log.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлу
file_path = 'data.txt'

# Создание папки для выходных файлов
output_dir = 'out'
os.makedirs(output_dir, exist_ok=True)

# Файлы для записи данных
files = {
    'sum_nal_pu_kbk': os.path.join(output_dir, 'sum_nal_pu_kbk.csv'),
    'oper_ptrfkod': os.path.join(output_dir, 'oper_ptrfkod.csv'),
    'aktsiz_pu': os.path.join(output_dir, 'aktsiz_pu.csv'),
    'common_params': os.path.join(output_dir, 'common_params.csv'),
}

# Регулярные выражения для извлечения данных
pattern_inn = re.compile(r'ИННЮЛ="(.*?)"')
pattern_kpp = re.compile(r'КПП="(.*?)"')
pattern_kod_pok = re.compile(r'<ОперПТРФКод КодПок="(.*?)" ПризнСтав="(.*?)" НалБаза="(.*?)" СумАкциз="(.*?)" />')
pattern_privn_srok_upl = re.compile(r'<СумНалПУ_КБК ПривнСрокУпл="(.*?)" АкцизПУ="(.*?)" />')
pattern_aktsiz_pu = re.compile(r'<АкцизПУ КодПок="(.*?)" СумАкциз="(.*?)" />')
pattern_period = re.compile(r'Период="(.*?)"')

# Заголовки для CSV файлов
with open(files['sum_nal_pu_kbk'], 'w', encoding='utf-8') as f:
    f.write('ИННЮЛ,КПП,ПривнСрокУпл,АкцизПУ,Период\n')

with open(files['oper_ptrfkod'], 'w', encoding='utf-8') as f:
    f.write('ИННЮЛ,КПП,КодПок,ПризнСтав,НалБаза,СумАкциз,Период\n')

with open(files['aktsiz_pu'], 'w', encoding='utf-8') as f:
    f.write('ИННЮЛ,КПП,КодПок,СумАкциз,Период\n')

with open(files['common_params'], 'w', encoding='utf-8') as f:
    f.write('ИННЮЛ,КПП,Параметр,Значение\n')

# Обработка файла построчно с tqdm
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    for line in tqdm(file, desc="Processing lines"):
        line = line.strip()
        if not line:
            continue  # Пропускаем пустые строки

        try:
            # Поиск данных в строке с помощью регулярных выражений
            inn = pattern_inn.search(line)
            kpp = pattern_kpp.search(line)
            period = pattern_period.search(line)

            oper_ptrfkod_matches = pattern_kod_pok.findall(line)
            privn_srok_upl_matches = pattern_privn_srok_upl.findall(line)
            aktsiz_pu_matches = pattern_aktsiz_pu.findall(line)
            
            if inn and kpp:
                inn = inn.group(1)
                kpp = kpp.group(1)
                period = period.group(1) if period else ''

                # Запись данных из <СумНалПУ_КБК
                with open(files['sum_nal_pu_kbk'], 'a', encoding='utf-8') as f:
                    for privn_srok_upl, aktsiz_pu in privn_srok_upl_matches:
                        f.write(f'{inn},{kpp},{privn_srok_upl},{aktsiz_pu},{period}\n')

                # Запись данных из <ОперПТРФКод
                with open(files['oper_ptrfkod'], 'a', encoding='utf-8') as f:
                    for kod_pok, prizn_stav, nal_baza, sum_akciz in oper_ptrfkod_matches:
                        f.write(f'{inn},{kpp},{kod_pok},{prizn_stav},{nal_baza},{sum_akciz},{period}\n')

                # Запись данных из <АкцизПУ
                with open(files['aktsiz_pu'], 'a', encoding='utf-8') as f:
                    for kod_pok, sum_akciz in aktsiz_pu_matches:
                        f.write(f'{inn},{kpp},{kod_pok},{sum_akciz},{period}\n')

                # # Общие записи вида "что-то"="что-то"
                # with open(files['common_params'], 'a', encoding='utf-8') as f:
                #     common_matches = re.findall(r'(\w+)="([^"]*)"', line)
                #     for match in common_matches:
                #         f.write(f'{inn},{kpp},{match[0]},{match[1]}\n')
            else:
                logging.warning(f"Missing required fields in line: {line}")
        except Exception as e:
            logging.error(f"Error processing line: {line}\nException: {e}")

logging.info("Processing completed successfully.")
print("Processing completed successfully.")
