import re
import requests
from typing import List, Tuple
import unittest
from unittest.mock import patch, Mock

class PhoneNumberExtractor:
    """Класс для извлечения и проверки телефонных номеров"""
    
    def __init__(self):
        # Регулярное выражение для российских номеров телефонов
        self.phone_pattern = re.compile(
            r'(?:\+7|8|7)?\s*[\(\-\s]*(\d{3})[\)\-\s]*\s*(\d{3})[\-\s]*(\d{2})[\-\s]*(\d{2})'
        )
        
        # Альтернативные форматы
        self.alternative_patterns = [
            # Формат +7 (XXX) XXX-XX-XX
            re.compile(r'\+7\s*\(\d{3}\)\s*\d{3}[\-\s]?\d{2}[\-\s]?\d{2}'),
            # Формат 8 (XXX) XXX-XX-XX
            re.compile(r'8\s*\(\d{3}\)\s*\d{3}[\-\s]?\d{2}[\-\s]?\d{2}'),
            # Формат XXX-XXX-XX-XX
            re.compile(r'\d{3}[\-\s]?\d{3}[\-\s]?\d{2}[\-\s]?\d{2}'),
        ]
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """Извлекает все телефонные номера из текста"""
        phones = []
        
        # Основной поиск
        matches = self.phone_pattern.findall(text)
        for match in matches:
            phone = f"+7 ({match[0]}) {match[1]}-{match[2]}-{match[3]}"
            phones.append(phone)
        
        # Дополнительный поиск по альтернативным паттернам
        for pattern in self.alternative_patterns:
            matches = pattern.findall(text)
            phones.extend(matches)
        
        # Удаление дубликатов и возврат
        return list(set(phones))
    
    def validate_phone_number(self, phone: str) -> bool:
        """Проверяет корректность телефонного номера"""
        # Очистка номера от лишних символов
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        # Проверка длины и формата
        if clean_phone.startswith('+7'):
            return len(clean_phone) == 12
        elif clean_phone.startswith('7'):
            return len(clean_phone) == 11
        elif clean_phone.startswith('8'):
            return len(clean_phone) == 11
        else:
            return len(clean_phone) == 10
    
    def get_phones_from_url(self, url: str) -> List[str]:
        """Получает телефонные номера с веб-страницы"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Извлекаем номера
            phones = self.extract_phone_numbers(response.text)
            
            # Фильтруем только валидные номера
            valid_phones = [phone for phone in phones if self.validate_phone_number(phone)]
            
            return valid_phones
            
        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return []