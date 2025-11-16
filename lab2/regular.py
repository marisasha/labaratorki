import re
import requests
from typing import List, Tuple
import unittest
from unittest.mock import patch, Mock

class PhoneNumberExtractor:
    """Класс для извлечения и проверки телефонных номеров"""
    
    def __init__(self):
        self.phone_pattern = re.compile(
            r'(?:\+7|8|7)?\s*[\(\-\s]*(\d{3})[\)\-\s]*\s*(\d{3})[\-\s]*(\d{2})[\-\s]*(\d{2})'
        )
        
        self.alternative_patterns = [

            re.compile(r'\+7\s*\(\d{3}\)\s*\d{3}[\-\s]?\d{2}[\-\s]?\d{2}'),

            re.compile(r'8\s*\(\d{3}\)\s*\d{3}[\-\s]?\d{2}[\-\s]?\d{2}'),

            re.compile(r'\d{3}[\-\s]?\d{3}[\-\s]?\d{2}[\-\s]?\d{2}'),
        ]
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """Извлекает все телефонные номера из текста"""
        phones = []
        
        matches = self.phone_pattern.findall(text)
        for match in matches:
            phone = f"+7 ({match[0]}) {match[1]}-{match[2]}-{match[3]}"
            phones.append(phone)
        
        for pattern in self.alternative_patterns:
            matches = pattern.findall(text)
            phones.extend(matches)
        
        return list(set(phones))
    
    def validate_phone_number(self, phone: str) -> bool:
        """Проверяет корректность телефонного номера"""
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        if clean_phone.startswith('+7'):
            return len(clean_phone) == 12
        elif clean_phone.startswith('7'):
            return len(clean_phone) == 11
        elif clean_phone.startswith('8'):
            return len(clean_phone) == 11
        else:
            return len(clean_phone) == 10
    
    def normalize_phone(self, phone: str) -> str:
        """Нормализует номер к стандартному формату"""
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        if clean_phone.startswith('+7'):
            return clean_phone
        elif clean_phone.startswith('7') and len(clean_phone) == 11:
            return '+' + clean_phone
        elif clean_phone.startswith('8') and len(clean_phone) == 11:
            return '+7' + clean_phone[1:]
        elif len(clean_phone) == 10:
            return '+7' + clean_phone
        else:
            return phone
    
    def get_phones_from_url(self, url: str) -> List[str]:
        """Получает телефонные номера с веб-страницы"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            

            phones = self.extract_phone_numbers(response.text)
            

            valid_phones = [phone for phone in phones if self.validate_phone_number(phone)]
            
            return valid_phones
            
        except Exception as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return []