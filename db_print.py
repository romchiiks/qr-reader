import sqlite3


def select_db():
    result_list = []
    conn = sqlite3.connect('qrdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM qr_codes')
    result = cursor.fetchall()
    conn.close()
    for row in result:
        result_list.append(f"ID: {row[0]} CITY: {row[1]} TEXT: {row[2]} QUANTITY: {row[3]} TIME: {row[4]}")

    return result_list 

def clear_db():
    conn = sqlite3.connect('qrdata.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS qr_codes')
    conn.commit()
    conn.close()
    return "Cleared DB"

while True:
    choose = input("\n1. Check\n2. Clear\n3. Exit\n")
    if choose == '1':
        try:
            rows = select_db()
            for row in rows:
                print(row)
        except sqlite3.OperationalError:
            print("No entries")
    elif choose == '2':
        print(clear_db())
    elif choose == '3':
        break