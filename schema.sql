-- Online Newspaper Database (CMPE351): relational schema for SQLite.
-- Follows the relational schema in Online_Newspaper_Database_Report.pdf.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS AUTHOR (
    Author_ID   INTEGER PRIMARY KEY,
    Name        TEXT NOT NULL,
    Birth_Date  TEXT,
    Sex         TEXT CHECK (Sex IN ('M', 'F')),
    Email       TEXT NOT NULL UNIQUE
);

-- Multi-valued attribute Tel# moved into its own relation.
CREATE TABLE IF NOT EXISTS AUTHOR_TEL (
    Author_ID   INTEGER NOT NULL REFERENCES AUTHOR (Author_ID) ON DELETE CASCADE,
    Tel         TEXT NOT NULL,
    PRIMARY KEY (Author_ID, Tel)
);

CREATE TABLE IF NOT EXISTS ARTICLE (
    Article_ID        INTEGER PRIMARY KEY,
    Title             TEXT NOT NULL,
    Category          TEXT NOT NULL,
    Publication_Date  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ADMINISTRATOR (
    Admin_ID       INTEGER PRIMARY KEY,
    Password_Hash  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS USER (
    User_ID              INTEGER PRIMARY KEY,
    Subscription_Status  TEXT NOT NULL,
    Email                TEXT NOT NULL UNIQUE,
    Sex                  TEXT CHECK (Sex IN ('M', 'F'))
);

-- SUBSCRIPTION merged with the Owns relationship (each subscription belongs to one user).
CREATE TABLE IF NOT EXISTS SUBSCRIPTION_OWNS (
    Sub_ID    INTEGER PRIMARY KEY,
    User_ID   INTEGER NOT NULL REFERENCES USER (User_ID) ON DELETE CASCADE,
    Sub_Type  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Writes (
    Author_ID   INTEGER NOT NULL REFERENCES AUTHOR (Author_ID) ON DELETE CASCADE,
    Article_ID  INTEGER NOT NULL REFERENCES ARTICLE (Article_ID) ON DELETE CASCADE,
    PRIMARY KEY (Author_ID, Article_ID)
);

CREATE TABLE IF NOT EXISTS ManagedBy (
    Article_ID  INTEGER NOT NULL REFERENCES ARTICLE (Article_ID) ON DELETE CASCADE,
    Admin_ID    INTEGER NOT NULL REFERENCES ADMINISTRATOR (Admin_ID) ON DELETE CASCADE,
    PRIMARY KEY (Article_ID, Admin_ID)
);

CREATE TABLE IF NOT EXISTS ReadBy (
    User_ID     INTEGER NOT NULL REFERENCES USER (User_ID) ON DELETE CASCADE,
    Article_ID  INTEGER NOT NULL REFERENCES ARTICLE (Article_ID) ON DELETE CASCADE,
    PRIMARY KEY (User_ID, Article_ID)
);

CREATE TABLE IF NOT EXISTS COMMENT (
    Comment_ID  INTEGER PRIMARY KEY,
    User_ID     INTEGER REFERENCES USER (User_ID) ON DELETE SET NULL,
    Body        TEXT NOT NULL,
    Created_At  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Has (
    Article_ID  INTEGER NOT NULL REFERENCES ARTICLE (Article_ID) ON DELETE CASCADE,
    Comment_ID  INTEGER NOT NULL REFERENCES COMMENT (Comment_ID) ON DELETE CASCADE,
    PRIMARY KEY (Article_ID, Comment_ID)
);
