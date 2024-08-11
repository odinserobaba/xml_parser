    pattern = rf'({key_escaped}=")(.*?)(")'
                replacement = rf'\1{value}\3'  # Строка замены с использованием групп

                # Попробуем заменить, используя безопасный подход
                try:
                    # Заменяем только если ключ присутствует
                    if re.search(pattern, updated_line):
                        updated_line = re.sub(pattern, replacement, updated_line)
                except re.error as e:
                    logging.error(f"Regex error while replacing '{key}': {e}")
