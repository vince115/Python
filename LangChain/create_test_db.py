import sqlite3

# 建立 SQLite 資料庫檔案 test.db
conn = sqlite3.connect("test.db")
c = conn.cursor()

# 建立 users 表
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TEXT
)
''')

# 建立 orders 表
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product TEXT,
    amount REAL,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# 插入測試用的使用者資料
c.executemany('INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)', [
    ("Alice", "alice@example.com", "2023-01-01"),
    ("Bob", "bob@example.com", "2023-02-01"),
    ("Charlie", "charlie@example.com", "2023-03-01"),
])

# 插入測試用的訂單資料
c.executemany('INSERT INTO orders (user_id, product, amount, created_at) VALUES (?, ?, ?, ?)', [
    (1, "Apple", 30, "2024-01-05"),
    (1, "Orange", 20, "2024-02-01"),
    (2, "Banana", 15, "2024-01-15"),
    (2, "Apple", 50, "2024-03-01"),
    (3, "Apple", 40, "2024-01-20"),
])

conn.commit()
conn.close()

print("✅ test.db 建立完成！")

