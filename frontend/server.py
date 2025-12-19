#!/usr/bin/env python3
"""
Простой HTTP сервер для тестирования фронтенда GGame
Запуск: python server.py
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # CORS headers для API запросов
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    """Запуск сервера"""
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print("🚀 GGame Frontend Server запущен!")
        print(f"📱 Откройте в браузере: http://localhost:{PORT}")
        print(f"📁 Папка: {DIRECTORY}")
        print("❌ Для остановки нажмите Ctrl+C")

        # Автоматически открыть в браузере
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except:
            pass  # Игнорируем ошибки открытия браузера

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Сервер остановлен")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
