import sqlite3 

conn=sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE COURSE_LIST(
                            COURSE_SEMESTER TEXT NOT NULL PRIMARY KEY
                            );")
cursor.execute("CREATE TABLE PASSWORD(
                                ID INT NOT NULL PRIMARY KEY, 
                                PASSWORD TEXT NOT NULL, 
                                AUTHORITY TEXT NOT NULL CHECK(AUTHORITY == 'ADMIN' OR AUTHORITY == 'STUDENT' OR AUTHORITY == 'STAFF' OR AUTHORITY == 'GUEST'
                                ));")
cursor.execute("CREATE TABLE STUDENT_COURSE(
                        COURSE_SEMESTER TEXT NOT NULL,ID INT NOT NULL, 
                        FOREIGN KEY(COURSE_SEMESTER) REFERENCES COURSE_LIST(COURSE_SEMESTER),FOREIGN KEY(ID) REFERENCES PASSWORD(ID));")
cursor.execute("CREATE TABLE QUESTIONS_POOL(
                        NAME TEXT NOT NULL PRIMARY KEY,
                        COM TEXT NOT NULL, 
                        DESCRIPTION_TEXT TEXT NOT NULL, 
                        TEXT NOT NULL CHECK(TYPE == 'C' OR TYPE == 'MTC' OR TYPE == 'TEXT'),
                        Q_TEXT TEXT
                        );")
cursor.execute("CREATE TABLE OPTIONAL_QUESTIONS_POOL(
                        NAME TEXT NOT NULL PRIMARY KEY,
                        COM TEXT NOT NULL, 
                        DESCRIPTION_TEXT TEXT NOT NULL, 
                        TYPE TEXT NOT NULL CHECK(TYPE == 'C' OR TYPE == 'MTC' OR TYPE == 'TEXT'), 
                        Q_TEXT TEXT);")
cursor.execute("CREATE TABLE SURVEY(
                        NAME TEXT NOT NULL PRIMARY KEY, 
                        COURSE_SEMESTER TEXT NOT NULL, 
                        COM TEXT NOT NULL, 
                        DESCRIPTION_TEXT TEXT NOT NULL, 
                        Q_LIST TEXT NOT NULL, 
                        OQ_LIST TEXT, 
                        ANSWER TEXT, 
                        STATE TEXT NOT NULL CHECK(STATE == 'NOT_REVIEWED' OR STATE ==  'A_OPENED' OR STATE = 'A_CLOSED' OR STATE == 'NORMAL'),
                        T_START TEXT NOT NULL, 
                        T_END TEXT NOT NULL ,
                        ATTENDENCE_RECORD TEXT, 
                        FOREIGN KEY(COURSE_SEMESTER) REFERENCES COURSE_LIST(COURSE_SEMESTER));")
cursor.execute("CREATE TABLE PUBLIC_RESULT (
                        NAME TEXT PRIMARY KEY,
                        FOREIGN KEY(NAME) REFERENCES SURVEY(NAME));")

cursor.execute("CREATE TABLE GUEST (
                        ID INT NOT NULL PRIMARY KEY, 
                        PASSWORD TEXT NOT NULL,EMAIL TEXT, 
                        COURSE_SEMESTER TEXT NOT NULL);")
conn.commit()


