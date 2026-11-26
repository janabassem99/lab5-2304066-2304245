-- Lab 5 Part II | Jana Bassem 2304066 | Farida Mohamed 2304245
-- Fresh setup only. This resets ONLY the Lab 5 database, not Lab 2 or Lab 3.
DROP DATABASE IF EXISTS library_lab5_2304066;
CREATE DATABASE library_lab5_2304066 CHARACTER SET utf8mb4;
USE library_lab5_2304066;
CREATE TABLE AUTHOR (author_id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, country VARCHAR(50) NOT NULL);
CREATE TABLE PUBLISHER (publisher_id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, country VARCHAR(50) NOT NULL);
CREATE TABLE CATEGORY (category_id INT PRIMARY KEY, name VARCHAR(100) NOT NULL);
CREATE TABLE BOOK (
 book_id INT PRIMARY KEY, title VARCHAR(150) NOT NULL, price DECIMAL(10,2) NOT NULL,
 publish_year INT, author_id INT NOT NULL, publisher_id INT NOT NULL, category_id INT NOT NULL,
 FOREIGN KEY (author_id) REFERENCES AUTHOR(author_id) ON DELETE CASCADE,
 FOREIGN KEY (publisher_id) REFERENCES PUBLISHER(publisher_id),
 FOREIGN KEY (category_id) REFERENCES CATEGORY(category_id)
);
CREATE TABLE MEMBER (member_id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(150) NOT NULL, join_date DATE NOT NULL);
CREATE TABLE LOAN (
 loan_id INT PRIMARY KEY, book_id INT NOT NULL, member_id INT NOT NULL,
 loan_date DATE NOT NULL, return_date DATE,
 FOREIGN KEY (book_id) REFERENCES BOOK(book_id) ON DELETE CASCADE,
 FOREIGN KEY (member_id) REFERENCES MEMBER(member_id)
);

-- Lab 5: one review per member and book, with an enforced 1-5 rating.
CREATE TABLE REVIEW (
 review_id INT PRIMARY KEY,
 book_id INT NOT NULL,
 member_id INT NOT NULL,
 rating INT NOT NULL,
 review_date DATE NOT NULL,
 CONSTRAINT review_rating CHECK (rating BETWEEN 1 AND 5),
 CONSTRAINT review_once UNIQUE (book_id, member_id),
 FOREIGN KEY (book_id) REFERENCES BOOK(book_id) ON DELETE CASCADE,
 FOREIGN KEY (member_id) REFERENCES MEMBER(member_id)
);

-- BONUS: reuse this catalogue join in F2.1 and both F2.3 queries.
CREATE VIEW book_details AS
SELECT b.book_id, b.title, b.price, b.publish_year,
       b.author_id, a.name AS author, a.country AS author_country,
       b.publisher_id, p.name AS publisher, p.country AS publisher_country,
       b.category_id, c.name AS category
FROM BOOK b
JOIN AUTHOR a ON b.author_id = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
JOIN CATEGORY c ON b.category_id = c.category_id;
