import sqlite3


class Database:
    def connect_to_db(self):
        """Open a sqlite3 connection and set `self.conn` and `self.cursor`.

        Uses a local file `app.db` so state persists between runs. This keeps
        the implementation simple and avoids external dependencies.
        """
        self.conn = sqlite3.connect("app.db")
        self.cursor = self.conn.cursor()
        print("Connected to the database.")

    def create_tabel(self):
        """Create a simple table if it doesn't exist.

        Note: the original code calls `create_tabel` (typo). Keep the name
        to remain compatible with existing calls.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def __enter__(self):
        self.connect_to_db()
        self.create_tabel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if hasattr(self, "conn") and self.conn:
                self.conn.close()
        except Exception:
            pass
        return False
    
with Database() as db:
    # Example operation: insert a sample item
    db.cursor.execute("INSERT INTO items (name) VALUES (?)", ("Sample Item",))
    db.conn.commit()