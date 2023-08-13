import sqlite3

conn = sqlite3.connect('birthday_reminder.db')
cursor = conn.cursor()

# Create the birthday table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS birthdays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL
    
    )
''')

conn.commit()
conn.close()
