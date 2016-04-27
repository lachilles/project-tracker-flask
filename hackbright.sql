CREATE TABLE students (
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    github VARCHAR(30)
    );

INSERT INTO students VALUES('Jane','Hacker','jhacks');
INSERT INTO students VALUES('Sarah','Developer','sdevelops');


CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(30),
    description TEXT,
    max_grade INTEGER
    );

INSERT INTO projects VALUES(1,'Markov','Tweets generated from Markov chains',50);
INSERT INTO projects VALUES(2,'Blockly','Programmatic Logic Puzzle Game',10);


CREATE TABLE grades (
    student_github VARCHAR(30),
    project_title VARCHAR(30),
    grade INTEGER
    );

INSERT INTO grades VALUES('jhacks','Markov',10);
INSERT INTO grades VALUES('jhacks','Blockly',2);
INSERT INTO grades VALUES('sdevelops','Markov',50);
INSERT INTO grades VALUES('sdevelops','Blockly',100);
