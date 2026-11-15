# Online Newspaper Database

A normalized relational database for an online newspaper: authors write articles, administrators manage them, users subscribe, read and comment. Built on SQLite, with a small Python interface for creating, reading, updating and deleting records.

Developed for CMPE351 (Database Systems) at Istanbul Bilgi University. The design (ER diagram, relational schema, normalization) is in `Online_Newspaper_Database_Report.pdf`.

## Schema

`schema.sql` implements the report's relational schema:

| Table | Purpose |
|-------|---------|
| `AUTHOR`, `AUTHOR_TEL` | Authors; phone numbers split out as a multi-valued attribute |
| `ARTICLE` | Articles with category and publication date |
| `ADMINISTRATOR` | Administrators (passwords stored as hashes) |
| `USER`, `SUBSCRIPTION_OWNS` | Readers and their subscriptions |
| `Writes`, `ManagedBy`, `ReadBy` | Author–article, article–admin and user–article relationships |
| `COMMENT`, `Has` | Comments and the articles they belong to |

Primary and foreign keys are declared and enforced. Deleting a user also removes their reads and subscription (`ON DELETE CASCADE`).

## Use it

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Interactive menu:** `python newspaper.py`. It creates `online_newspaper.db` with sample data on the first run, then lets you list users and articles, add an article, change a category, delete a user, and run the join that shows who read what.

**Notebook:** open `walkthrough.ipynb` in Jupyter from this folder, or in Google Colab. It builds the database in memory and runs the main queries.

**Plain SQL:** run `schema.sql` in any SQLite tool, for example `sqlite3 news.db < schema.sql`.

## Tests

```bash
pytest
```

The tests check the schema file, that sample data is only added once, the CRUD operations, foreign key enforcement, the join queries, and that the menu copes with bad input.

## Author

Cem Akçiçek, with Ece Doğa Gül. Istanbul Bilgi University, Computer Engineering.
