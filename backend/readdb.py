import sqlite3

def read_logs():
    # Connect to SQLite database
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    
    # Query all log entries
    c.execute("SELECT * FROM logs")
    rows = c.fetchall()
    
    # Print or process the retrieved data
    for row in rows:
        print(row)
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    read_logs()
