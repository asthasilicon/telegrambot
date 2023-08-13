import sqlite3
import datetime
import time

interval_seconds = 30  # Replace this with your desired interval in seconds

while True:
    # Connect to the SQLite database
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()

    # Get today's date
    today_date = datetime.date.today()

    # Construct and execute the SQL query
    cursor.execute("SELECT * FROM birthday_reminder WHERE date <> ?", (today_date,))

    # Fetch the results
    results = cursor.fetchall()

    # Print the results or perform any desired actions
    for row in results:
        row_id = row[0]
        cursor.execute("UPDATE birthday_reminder SET reminded = 0 WHERE id = ? ",(row_id,))
    db_connection.commit()
    # Close the database connection
    cursor.close()
    db_connection.close()
    
    
    
    print("Code executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))

    # Pause the execution for the specified interval
    time.sleep(interval_seconds)



