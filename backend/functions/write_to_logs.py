import sqlite3
import time

def write_to_logs(address, username, pfp_url, new_pfp_url):
    now = str(time.time())
    
    # Connect to SQLite database
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 date TEXT, 
                 custody_address TEXT,
                 username TEXT,
                 pfp_url TEXT,
                 new_pfp_url TEXT)''')
    
    # Check if the username already exists
    c.execute("SELECT * FROM logs WHERE username=?", (username,))
    existing_entry = c.fetchone()
    
    if existing_entry:
        # Update existing entry
        c.execute('''UPDATE logs 
                     SET date=?, custody_address=?, pfp_url=?, new_pfp_url=?
                     WHERE username=?''', (now, address, pfp_url, new_pfp_url, username))
    else:
        # Insert new entry
        c.execute('''INSERT INTO logs (date, custody_address, username, pfp_url, new_pfp_url) 
                     VALUES (?, ?, ?, ?, ?)''', (now, address, username, pfp_url, new_pfp_url))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
