import sqlite3

class Database:
    #Creating the Database
    def __init__(self, db_name = "soma_planner.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        #Enabling the foreign keys
        self.cursor.execute("PRAGMA foreign_keys = ON")

        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL,
                            difficulty INTEGER NOT NULL
                            )  
                            """)
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS exams(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            subject_id INTEGER NOT NULL,
                            exam_date TEXT NOT NULL,
                            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
                            )
                            """)
        
        self.conn.commit()

    
    #Subject Methods ADD, VIEW, UPDATE, DELETE AND SEARCH    
    def add_subject(self, name, difficulty):
        self.cursor.execute("INSERT INTO subjects (name, difficulty) VALUES(?, ?)",
                           (name, difficulty)
                           )
        self.conn.commit()
    
    def get_subjects(self):
        self.cursor.execute("SELECT * FROM subjects ORDER BY name")

        return self.cursor.fetchall()
    
    def search_subject(self, keyword):
        self.cursor.execute("""SELECT * FROM subjects WHERE name LIKE ? """, ("%" + keyword + "%",))

        return self.cursor.fetchall()
    
    def update_subject(self, subject_id, name, difficulty):
        self.cursor.execute("""UPDATE subjects SET name = ?, difficulty = ?
                           WHERE id = ?""",
                           (name, difficulty, subject_id)
                           )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_subject(self, subject_id):
        self.cursor.execute(""" DELETE FROM subjects
                           WHERE id = ?""",
                           (subject_id,)
                           )
        self.conn.commit()
        
        return self.cursor.rowcount > 0
        
   
    #Exam Methods ADD, GET, UPDATE and DELETE exams
    def add_exam(self, subject_id, exam_date):
        self.cursor.execute("INSERT INTO exams(subject_id, exam_date) VALUES(?, ?)",
                           (subject_id, exam_date)
                           )
        self.conn.commit()
        
    def get_exams(self):
        self.cursor.execute("""SELECT exams.id, subjects.id, subjects.name, subjects.difficulty, exams.exam_date
                                FROM exams
                                JOIN subjects
                                ON exams.subject_id = subjects.id
                                ORDER BY exams.exam_date
                                  """)
        return self.cursor.fetchall()
    
    def update_exam(self, exam_id, subject_id, exam_date):
        self.cursor.execute("""UPDATE exams SET subject_id = ?, exam_date = ?
                           WHERE id = ?""",
                           (subject_id, exam_date, exam_id)
                           )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_exam(self, exam_id):
        self.cursor.execute("""DELETE FROM exams WHERE id = ? """,
                            (exam_id,)
                            )

        self.connection.commit()
        return self.cursor.rowcount > 0
    
    #Close Database
    def close(self):
        self.conn.close()
