import sqlite3
c = sqlite3.connect(':memory:').cursor()
c.execute("SELECT '2026-07-27T08:00:00.000Z' > '2026-07-27 15:00:00'")
print("Comparison Result:", c.fetchone()[0])
