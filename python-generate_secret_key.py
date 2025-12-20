#!/usr/bin/env python
"""
Генератор SECRET_KEY для Django
Запуск: python python-generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print(f'\nВаш SECRET_KEY:\n{secret_key}\n')
    print('Добавьте его в переменные окружения на хостинге!')
