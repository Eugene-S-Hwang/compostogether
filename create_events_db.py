import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('events.db')
c = conn.cursor()

# Create events table
c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start TEXT NOT NULL,
        end TEXT NOT NULL,
        summary TEXT NOT NULL
    )
''')

# Insert sample data
events = [
    ('2024-06-17T09:00:00', '2024-06-17T10:00:00', 'Event 1'),
    ('2024-06-18T14:00:00', '2024-06-18T15:00:00', 'Event 2'),
    ('2024-06-19T11:00:00', '2024-06-19T12:00:00', 'Event 3'),
    ('2024-06-20T08:00:00', '2024-06-20T09:00:00', 'Event 4'),
    ('2024-06-21T13:00:00', '2024-06-21T14:00:00', 'Event 5')
]

c.executemany('INSERT INTO events (start, end, summary) VALUES (?, ?, ?)', events)
conn.commit()

# Close the connection
conn.close()

print("Database and table created, and sample data inserted successfully.")
