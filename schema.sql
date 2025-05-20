{\rtf1\ansi\ansicpg1254\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 CREATE TABLE IF NOT EXISTS AUTHOR (\
    Author_ID INTEGER PRIMARY KEY,\
    Name TEXT,\
    Birth_Date TEXT,\
    Sex TEXT,\
    Email TEXT\
);\
\
CREATE TABLE IF NOT EXISTS AUTHOR_TEL (\
    Author_ID INTEGER,\
    Tel TEXT,\
    FOREIGN KEY (Author_ID) REFERENCES AUTHOR (Author_ID)\
);\
\
CREATE TABLE IF NOT EXISTS ARTICLE (\
    Article_ID INTEGER PRIMARY KEY,\
    Title TEXT,\
    Category TEXT,\
    Publication_Date TEXT\
);\
\
CREATE TABLE IF NOT EXISTS USER (\
    User_ID INTEGER PRIMARY KEY,\
    Subscription_Status TEXT,\
    Email TEXT,\
    Sex TEXT\
);\
\
CREATE TABLE IF NOT EXISTS ReadBy (\
    User_ID INTEGER,\
    Article_ID INTEGER,\
    FOREIGN KEY (User_ID) REFERENCES USER (User_ID),\
    FOREIGN KEY (Article_ID) REFERENCES ARTICLE (Article_ID)\
);\
}