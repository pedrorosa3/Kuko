"""
Aplicações Distribuídas - Projeto 3 - kuko_client.py
Grupo: 40
Números de aluno: 60294 60270
"""


import sqlite3
from os.path import isfile
def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect('kuko.db')
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute("CREATE TABLE question(id_question INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answers TEXT NOT NULL, k INT NOT NULL);")
        cursor.execute("CREATE TABLE qset(id_qset INTEGER PRIMARY KEY AUTOINCREMENT, questions TEXT NOT NULL);")
        cursor.execute("CREATE TABLE quiz(id_quiz INTEGER PRIMARY KEY AUTOINCREMENT, id_qset INT,state VARCHAR(50), points TEXT, timestamp_p DATETIME, timestamp_e DATETIME, question_i INT, participants TEXT, FOREIGN KEY (id_qset) REFERENCES qset(id_qset));")
        cursor.execute("CREATE TABLE results(id_quiz INT , question_i INT , participant INT , answer INT, PRIMARY KEY (id_quiz, question_i, participant) ,FOREIGN KEY (id_quiz) REFERENCES quiz(id_quiz));")
        connection.commit()
        variasperguntas=[("What is the capital of France?","Paris;Berlim;London;Madrid",1),
        ("Who wrote 'Romeo and Juliet'","William;Jose;Antonio;Manel",1),
        ("What is the chemical symbol of silver","Au;Ag;Fe;Cu",1),
        ("What is the capital of Italy","Rome;Berlin;Paris;Madrid",1)]

        #variosqsets=[("1;2"),("2;3")]
        cursor.executemany('INSERT INTO question VALUES (NULL,?, ?, ?)', variasperguntas)
        connection.commit()


    return connection, cursor

        

			

if __name__ == '__main__':
    conn, cursor = connect_db('kuko.db')
    
    
    #cursor.execute('SELECT * FROM question') # Fazer query e obter todos
    #todos = cursor.fetchall() # os resultados
    #print ("Todos: ", todos)