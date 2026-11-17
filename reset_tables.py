from db import DatabaseManager
db = DatabaseManager()
def reset_tables():
    db.cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type ="table"
    AND name NOT LIKE "sqlite_%"
""")
    for (row,) in (db.cursor.fetchall()):
        db.cursor.execute(f""" 
    DROP TABLE {row}
""")

reset_tables()
