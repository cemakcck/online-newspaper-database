# 📰 Online Newspaper Database – CMPE351 Project

A fully normalized relational database system simulating the backend of an online newspaper.  
This was developed as part of the CMPE351 (Database Systems) course at Istanbul Bilgi University.

---

## 📘 Overview

The system supports:

- **Users** who subscribe and read articles
- **Authors** who write articles
- **Articles** with categories and publication dates
- **Administrators** who manage the content
- **Comments** tied to articles
- All relationships and constraints defined in a normalized schema

---

## 🧠 Concepts Demonstrated

- ER Modeling
- Relational Schema Design
- Primary & Foreign Keys
- Cardinality Mapping
- Multi-valued Attribute Handling (Tel# separated from AUTHOR)
- CRUD Operations via SQL + Python interface (in notebook)
- Join queries & user-interactive menu system

---

## 📂 Files in This Repo

| File | Description |
|------|-------------|
| `Cem_Akcicek_Database_Project.ipynb` | Full Python notebook with SQLite setup and CRUD interface |
| `Online_Newspaper_Database_Report.pdf` | Report with ER diagram, schema, normalization, and constraints |
| `schema.sql` | SQL-only version of the schema (for instant database setup) |

---

## 🧪 How to Use This Project

### 🟢 Option 1 – Run the Notebook

1. Open `Cem_Akcicek_Database_Project.ipynb` in Google Colab or Jupyter
2. Run all cells
3. You’ll see:
   - Tables created and filled with demo data
   - A menu for CRUD operations
   - A JOIN query showing what users read

### 🟢 Option 2 – Use the SQL Schema Directly

1. Open a SQLite tool (like [DB Browser for SQLite](https://sqlitebrowser.org/) or VSCode with SQLite plugin)
2. Create a new SQLite database
3. Copy the contents of `schema.sql` and execute it
4. Your schema is now live — you can add data and test joins manually

---

## 📌 Notes

This database project focuses on data modeling and basic operations. Some entities/relationships described in the report (e.g., `Writes`, `Has`, `ManagedBy`) are part of the design but not implemented in the current code version.

---

## 👩‍💻 Author

Cem Akçiçek  
Student, Istanbul Bilgi University – Computer Engineering  
GitHub: [cemakcck](https://github.com/cemakcck)
