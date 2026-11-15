"""Online Newspaper Database: SQLite schema, sample data and a small CRUD menu.

Run `python newspaper.py` for the interactive menu. The database file is created next to this
script (online_newspaper.db) and the sample data is only added the first time.
"""

import hashlib
import sqlite3
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
SCHEMA_FILE = HERE / "schema.sql"
DEFAULT_DB = HERE / "online_newspaper.db"

AUTHORS = [
    ("Ahmet Yılmaz", "1970-03-12", "M", "ahmet.yilmaz@example.com"),
    ("Ayşe Demir", "1985-07-23", "F", "ayse.demir@example.com"),
    ("Mehmet Kaya", "1990-02-14", "M", "mehmet.kaya@example.com"),
    ("Fatma Çelik", "1995-11-05", "F", "fatma.celik@example.com"),
    ("Emre Şahin", "1988-09-30", "M", "emre.sahin@example.com"),
]
AUTHOR_TELS = [(1, "+90 212 555 0101"), (1, "+90 532 555 0101"), (2, "+90 216 555 0102")]
ARTICLES = [
    ("Yapay Zeka ve Gelecek", "Teknoloji", "2024-01-01"),
    ("Sağlıklı Beslenme İpuçları", "Yaşam", "2024-01-15"),
    ("Türk Tarihinde Dönüm Noktaları", "Tarih", "2024-02-10"),
    ("Girişimcilik ve Yenilik", "İş Dünyası", "2024-02-25"),
    ("Doğal Yaşamın Korunması", "Çevre", "2024-03-05"),
]
USERS = [
    ("Aktif", "ali.kurt@example.com", "M"),
    ("Pasif", "zeynep.ak@example.com", "F"),
    ("Aktif", "murat.can@example.com", "M"),
    ("Pasif", "selin.tas@example.com", "F"),
    ("Aktif", "burak.uzun@example.com", "M"),
]
SUBSCRIPTIONS = [(1, "Yıllık"), (3, "Aylık"), (5, "Öğrenci")]
WRITES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
READS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (1, 3)]
COMMENTS = [(1, "Harika bir yazı, teşekkürler!"), (3, "Kaynakları da paylaşır mısınız?")]
HAS = [(1, 1), (3, 2)]


def connect(path=DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))


def seed(conn: sqlite3.Connection) -> None:
    """Add the sample data, but only into an empty database."""
    if conn.execute("SELECT COUNT(*) FROM ARTICLE").fetchone()[0]:
        return
    with conn:
        conn.executemany("INSERT INTO AUTHOR (Name, Birth_Date, Sex, Email) VALUES (?, ?, ?, ?)", AUTHORS)
        conn.executemany("INSERT INTO AUTHOR_TEL (Author_ID, Tel) VALUES (?, ?)", AUTHOR_TELS)
        conn.executemany("INSERT INTO ARTICLE (Title, Category, Publication_Date) VALUES (?, ?, ?)", ARTICLES)
        conn.executemany("INSERT INTO USER (Subscription_Status, Email, Sex) VALUES (?, ?, ?)", USERS)
        conn.executemany("INSERT INTO SUBSCRIPTION_OWNS (User_ID, Sub_Type) VALUES (?, ?)", SUBSCRIPTIONS)
        conn.execute(
            "INSERT INTO ADMINISTRATOR (Password_Hash) VALUES (?)",
            (hashlib.sha256(b"sample-admin-password").hexdigest(),),
        )
        conn.executemany("INSERT INTO Writes (Author_ID, Article_ID) VALUES (?, ?)", WRITES)
        conn.executemany("INSERT INTO ManagedBy (Article_ID, Admin_ID) VALUES (?, 1)", [(i,) for i in range(1, 6)])
        conn.executemany("INSERT INTO ReadBy (User_ID, Article_ID) VALUES (?, ?)", READS)
        conn.executemany("INSERT INTO COMMENT (User_ID, Body) VALUES (?, ?)", COMMENTS)
        conn.executemany("INSERT INTO Has (Article_ID, Comment_ID) VALUES (?, ?)", HAS)


def add_article(conn, title: str, category: str, publication_date: str) -> int:
    date.fromisoformat(publication_date)  # raises ValueError unless YYYY-MM-DD
    if not title.strip() or not category.strip():
        raise ValueError("Title and category are required.")
    with conn:
        cur = conn.execute(
            "INSERT INTO ARTICLE (Title, Category, Publication_Date) VALUES (?, ?, ?)",
            (title.strip(), category.strip(), publication_date),
        )
    return cur.lastrowid


def update_article_category(conn, article_id: int, category: str) -> bool:
    with conn:
        cur = conn.execute("UPDATE ARTICLE SET Category = ? WHERE Article_ID = ?", (category.strip(), article_id))
    return cur.rowcount == 1


def delete_user(conn, user_id: int) -> bool:
    """Deletes a user; their reads and subscription go with them (ON DELETE CASCADE)."""
    with conn:
        cur = conn.execute("DELETE FROM USER WHERE User_ID = ?", (user_id,))
    return cur.rowcount == 1


def articles_read_by_users(conn) -> list:
    return conn.execute(
        """
        SELECT USER.Email, ARTICLE.Title, ARTICLE.Category
        FROM ReadBy
        JOIN USER ON ReadBy.User_ID = USER.User_ID
        JOIN ARTICLE ON ReadBy.Article_ID = ARTICLE.Article_ID
        ORDER BY USER.User_ID, ARTICLE.Article_ID
        """
    ).fetchall()


def articles_with_authors(conn) -> list:
    return conn.execute(
        """
        SELECT ARTICLE.Title, group_concat(AUTHOR.Name, ', ')
        FROM ARTICLE
        JOIN Writes ON Writes.Article_ID = ARTICLE.Article_ID
        JOIN AUTHOR ON AUTHOR.Author_ID = Writes.Author_ID
        GROUP BY ARTICLE.Article_ID
        ORDER BY ARTICLE.Article_ID
        """
    ).fetchall()


def print_rows(headers, rows) -> None:
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)] if rows else [len(h) for h in headers]
    print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    for row in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(row, widths)))


def print_table(conn, table: str) -> None:
    cur = conn.execute(f"SELECT * FROM {table}")
    print(f"\n{table}")
    print_rows([d[0] for d in cur.description], cur.fetchall())


def ask_int(prompt: str):
    raw = input(prompt).strip()
    if raw.isdigit():
        return int(raw)
    print("Please enter a whole number.")
    return None


MENU = """
Choose an operation:
1. Show users
2. Show articles
3. Add an article
4. Delete a user
5. Change an article's category
6. Show who read what (JOIN)
7. Exit"""


def menu(conn) -> None:
    while True:
        print(MENU)
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            print_table(conn, "USER")
        elif choice == "2":
            print_table(conn, "ARTICLE")
        elif choice == "3":
            title = input("Title: ")
            category = input("Category: ")
            published = input("Publication date (YYYY-MM-DD): ")
            try:
                print(f"Added article {add_article(conn, title, category, published)}.")
            except ValueError:
                print("Please give a title, a category and a date like 2025-01-31.")
        elif choice == "4":
            user_id = ask_int("ID of the user to delete: ")
            if user_id is not None:
                print("User deleted." if delete_user(conn, user_id) else f"No user with ID {user_id}.")
        elif choice == "5":
            article_id = ask_int("ID of the article: ")
            if article_id is not None:
                category = input("New category: ")
                found = update_article_category(conn, article_id, category)
                print("Category updated." if found else f"No article with ID {article_id}.")
        elif choice == "6":
            print("\nArticles read by users")
            print_rows(["User", "Article", "Category"], articles_read_by_users(conn))
        elif choice == "7":
            print("Goodbye!")
            return
        else:
            print("Please enter a number between 1 and 7.")


def main() -> None:
    conn = connect()
    create_schema(conn)
    seed(conn)
    try:
        menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
