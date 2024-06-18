import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('events.db')
c = conn.cursor()

# Fetch all events
c.execute('SELECT * FROM events')
rows = c.fetchall()

# Convert to a pandas DataFrame
df = pd.DataFrame(rows, columns=['id', 'start', 'end', 'summary'])
print(df)

# Close the connection
conn.close()
