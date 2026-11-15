import sqlite3

import pytest

import newspaper as np_


@pytest.fixture
def conn(tmp_path):
    c = np_.connect(tmp_path / "news.db")
    np_.create_schema(c)
    np_.seed(c)
    yield c
    c.close()


def count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_schema_file_is_plain_sql_with_every_table():
    conn = sqlite3.connect(":memory:")
    conn.executescript(np_.SCHEMA_FILE.read_text(encoding="utf-8"))
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert tables == {
        "AUTHOR", "AUTHOR_TEL", "ARTICLE", "ADMINISTRATOR", "USER", "SUBSCRIPTION_OWNS",
        "Writes", "ManagedBy", "ReadBy", "COMMENT", "Has",
    }


def test_seeding_twice_adds_nothing(conn):
    before = {t: count(conn, t) for t in ("AUTHOR", "ARTICLE", "USER", "ReadBy")}
    np_.seed(conn)
    assert {t: count(conn, t) for t in before} == before
    assert before["ARTICLE"] == 5


def test_add_article(conn):
    article_id = np_.add_article(conn, "Test title", "Teknoloji", "2025-01-01")
    assert conn.execute("SELECT Title FROM ARTICLE WHERE Article_ID = ?", (article_id,)).fetchone()[0] == "Test title"


def test_add_article_rejects_bad_date(conn):
    with pytest.raises(ValueError):
        np_.add_article(conn, "Title", "Category", "01/01/2025")


def test_update_category_reports_missing_article(conn):
    assert np_.update_article_category(conn, 1, "Spor") is True
    assert np_.update_article_category(conn, 999, "Spor") is False


def test_deleting_a_user_removes_their_reads_and_subscription(conn):
    assert np_.delete_user(conn, 1) is True
    assert conn.execute("SELECT COUNT(*) FROM ReadBy WHERE User_ID = 1").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM SUBSCRIPTION_OWNS WHERE User_ID = 1").fetchone()[0] == 0
    assert np_.delete_user(conn, 1) is False


def test_foreign_keys_are_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO ReadBy (User_ID, Article_ID) VALUES (999, 1)")


def test_reads_join(conn):
    rows = np_.articles_read_by_users(conn)
    assert ("ali.kurt@example.com", "Yapay Zeka ve Gelecek", "Teknoloji") in rows


def test_articles_with_authors(conn):
    rows = np_.articles_with_authors(conn)
    assert len(rows) == 5
    assert all(author for _, author in rows)


def test_menu_survives_bad_input(conn, monkeypatch, capsys):
    answers = iter(["9", "4", "abc", "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))
    np_.menu(conn)
    out = capsys.readouterr().out
    assert "Please enter a number between 1 and 7" in out
    assert "Please enter a whole number" in out
