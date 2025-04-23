import cv2
import sqlite3
from datetime import datetime
from qreader import QReader
from collections import Counter

# Сканер QR кодов
qreader = QReader()

# Подключение к БД
conn = sqlite3.connect("qrdata.db")
cursor = conn.cursor()

# Время для названия файлов и timestamp
time = datetime.now().strftime("%d-%m-%Y")

# конфигурация OpenCV 
cams = {"Город": "", "Кимры": ""}

# Основная логика
for city, url in cams.items():
    cam = cv2.VideoCapture(url) # CCTV камера

    ret, frame = cam.read() # Считываем изображение

    if ret:
        cv2.imwrite(f"imgs/{time}-{city}.png", frame) # Сохраняем фото в файл

    cam.release()

    image = cv2.cvtColor(cv2.imread(f"imgs/{time}-{city}.png"), cv2.COLOR_BGR2RGB)

    decoded_text = qreader.detect_and_decode(image=image)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            text TEXT,
            quantity INTEGER,
            timestamp TEXT
        )
    """)

    counts = Counter(decoded_text)

    for text, qty in counts.items():
        if text != None:
            cursor.execute("INSERT INTO qr_codes (city, text, quantity, timestamp) VALUES (?, ?, ?, ?)", (city, text, qty, time))

    conn.commit()

conn.close()