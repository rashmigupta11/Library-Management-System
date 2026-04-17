import sqlite3

# connect to database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# LIBRARY MEMBERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
)
""")

# BOOKS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    category TEXT,
    type TEXT,
    available INTEGER DEFAULT 1
)
""")

# ISSUE BOOKS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    actual_return TEXT,
    status TEXT DEFAULT 'Issued'
)
""")

# FINES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS fines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER,
    amount REAL,
    paid INTEGER DEFAULT 0
)
""")

# INSERT DEFAULT USERS (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('adm', 'adm', 'admin')")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('user', 'user', 'user')")
    print("Default users created.")

# save changes
conn.commit()

# close connection
conn.close()
print("Database and tables created successfully!")