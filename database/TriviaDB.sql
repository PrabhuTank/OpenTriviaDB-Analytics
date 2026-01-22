-- Use the created database
USE triviadb;

-- Create the 'Types' table
CREATE TABLE IF NOT EXISTS Types (
    ID_type INT AUTO_INCREMENT PRIMARY KEY,
    Type_name VARCHAR(30) NOT NULL,
	Type_slug VARCHAR(30) NOT NULL
);

-- Create the 'Levels' table
CREATE TABLE IF NOT EXISTS Levels (
    ID_level INT AUTO_INCREMENT PRIMARY KEY,
    Level_name VARCHAR(15) NOT NULL
);

-- Create the 'Categories' table
CREATE TABLE IF NOT EXISTS Categories (
    ID_category INT AUTO_INCREMENT PRIMARY KEY,
    Category_name VARCHAR(100) NOT NULL
);

-- Create the 'Questions' table
CREATE TABLE IF NOT EXISTS Questions (
    ID_question INT AUTO_INCREMENT PRIMARY KEY,
    Question_text TEXT NOT NULL,
	ID_type INT,
    ID_level INT,
    ID_category INT,
	FOREIGN KEY (ID_type) REFERENCES Types(ID_type),
    FOREIGN KEY (ID_level) REFERENCES Levels(ID_level),
    FOREIGN KEY (ID_category) REFERENCES Categories(ID_category)
);

-- Create the 'Answers' table
CREATE TABLE IF NOT EXISTS Answers (
    ID_answer INT AUTO_INCREMENT PRIMARY KEY,
    Answer_sentence TEXT NOT NULL,
    Correct ENUM('Yes', 'No') NOT NULL,
    ID_question INT,
    FOREIGN KEY (ID_question) REFERENCES Questions(ID_question) ON DELETE CASCADE
);

-- Insert sample data into 'Types' table
INSERT INTO Types (type_name, type_slug) VALUES 
('Multiple Choice','multiple'), 
('True / False','boolean');

-- Insert sample data into 'Levels' table
INSERT INTO Levels (level_name) VALUES 
('Easy'),
('Medium'),
('Hard');

-- Insert sample data into 'Categories' table
INSERT INTO Categories (category_name) VALUES 
("General Knowledge"),("Entertainment: Books"),("Entertainment: Film"),("Entertainment: Music"),("Entertainment: Musicals &amp; Theatres"),
("Entertainment: Television"),("Entertainment: Video Games"),("Entertainment: Board Games"),("Science &amp; Nature"),("Science: Computers"),
("Science: Mathematics"),("Mythology"),("Sports"),("Geography"),("History"),("Politics"),("Art"),("Celebrities"),("Animals"),("Vehicles"),
("Entertainment: Comics"),("Science: Gadgets"),("Entertainment: Japanese Anime &amp; Manga"),("Entertainment: Cartoon &amp; Animations");
