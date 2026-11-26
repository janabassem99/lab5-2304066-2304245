-- Lab 5 discussion | Jana Bassem 2304066 | Farida Mohamed 2304245
-- Run these statements in DBeaver against your prepared Lab 5 database.
USE library_lab5_2304066;
SELECT VERSION() AS mysql_version, DATABASE() AS current_database;
SHOW FULL TABLES;
SELECT * FROM REVIEW ORDER BY review_id;
SHOW CREATE TABLE REVIEW;
-- BONUS: inspect the saved catalogue join.
SHOW CREATE VIEW book_details;
SELECT * FROM book_details ORDER BY book_id;
-- F2.1 bonus: reuse the view.
SELECT title, price, (SELECT AVG(price) FROM BOOK) AS library_average
FROM book_details
WHERE price > (SELECT AVG(price) FROM BOOK)
ORDER BY price DESC, book_id;
-- Use check_lab5.py for constraint rejection and cascade tests in an isolated database.
