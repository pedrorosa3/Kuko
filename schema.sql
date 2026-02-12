PRAGMA foreign_keys = ON;
CREATE TABLE question(

    id_question INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answers TEXT NOT NULL,
    k INT NOT NULL

);

CREATE TABLE qset(
    id_qset INTEGER PRIMARY KEY AUTOINCREMENT,
    questions TEXT NOT NULL
);

CREATE TABLE quiz(
    id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
    id_qset INT,
    state VARCHAR(50),
    points TEXT,
    timestamp_p DATETIME,
    timestamp_e DATETIME,
    question_i INT,
    participants TEXT,
    FOREIGN KEY (id_qset) REFERENCES qset(id_qset)
);

CREATE TABLE results(
    id_quiz INT,
    question_i INT,
    participant INT,
    answer INT,
    PRIMARY KEY (id_quiz,question_i,participant),
    FOREIGN KEY (id_quiz) REFERENCES quiz(id_quiz)
);

INSERT INTO question (question,answers,k) VALUES
        ("What is the capital of France?","Paris;Berlim;London;Madrid",1),
        ("Who wrote 'Romeo and Juliet'","William;Jose;Antonio;Manel",1),
        ("What is the chemical symbol of silver","Au;Ag;Fe;Cu",1),
        ("What is the capital of Italy","Rome;Berlin;Paris;Madrid",1);


