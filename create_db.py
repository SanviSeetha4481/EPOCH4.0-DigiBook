import sqlite3

def init_db(db_path="library.db"):
    try:
        # Use context manager so connection auto-closes
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()

            # Create table with constraints for data integrity
            cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER CHECK(year > 0),
                isbn TEXT UNIQUE
            )
            """)

            # Create indexes to speed up searches
            cur.execute("CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn)")

        # If no error — success!
        print("Database created successfully!")

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    init_db()
