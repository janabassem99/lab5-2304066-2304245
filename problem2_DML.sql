-- Deterministic demonstration data; IDs 4001+ are separate from the old library.
USE library_lab5_2304066;
INSERT INTO AUTHOR VALUES
(4001,'Naguib Mahfouz','Egypt'),(4002,'Ahdaf Soueif','Egypt'),
(4003,'George Orwell','United Kingdom'),(4004,'Demo Author Without Books','France');
INSERT INTO PUBLISHER VALUES (4001,'Nile Press','Egypt'),(4002,'London Books','United Kingdom'),(4003,'Paris Editions','France');
INSERT INTO CATEGORY VALUES (4001,'Fiction'),(4002,'History'),(4003,'Essays');
INSERT INTO BOOK VALUES
(4001,'Palace Walk',18.50,1956,4001,4001,4001),
(4002,'Palace of Desire',22.00,1957,4001,4001,4001),
(4003,'Sugar Street',19.00,1957,4001,4001,4001),
(4004,'The Map of Love',25.00,1999,4002,4002,4001),
(4005,'In the Eye of the Sun',16.00,1992,4002,4002,4001),
(4006,'Cairo: My City',14.00,2012,4002,4001,4002),
(4007,'Nineteen Eighty-Four',20.00,1949,4003,4002,4001),
(4008,'Animal Farm',12.00,1945,4003,4002,4001),
(4009,'Homage to Catalonia',23.00,1938,4003,4002,4002),
(4010,'Collected Essays',30.00,1961,4003,4003,4003);
INSERT INTO MEMBER VALUES
(4001,'Demo Reader A','reader.a@example.com','2026-09-01'),
(4002,'Demo Reader B','reader.b@example.com','2026-09-02'),
(4003,'Demo Reader C','reader.c@example.com','2026-09-03'),
(4004,'Demo Reader D','reader.d@example.com','2026-09-04'),
(4005,'Demo Reader Without Loans','reader.e@example.com','2026-09-05');
INSERT INTO LOAN VALUES
(4001,4001,4001,'2026-09-01','2026-09-05'),
(4002,4001,4002,'2026-09-06','2026-09-10'),
(4003,4001,4003,'2026-09-11','2026-09-15'),
(4004,4001,4001,'2026-10-01',NULL),
(4005,4002,4001,'2026-09-01','2026-09-05'),
(4006,4002,4002,'2026-09-06','2026-09-10'),
(4007,4002,4004,'2026-10-02',NULL),
(4008,4003,4001,'2026-09-01','2026-09-05'),
(4009,4003,4002,'2026-10-03',NULL),
(4010,4004,4001,'2026-09-01','2026-09-05'),
(4011,4005,4003,'2026-10-04',NULL),
(4012,4006,4004,'2026-09-01','2026-09-05');

-- An author-only country is required for EXCEPT.
INSERT INTO AUTHOR VALUES (5001,'Demo Spanish Author','Spain');
-- Nine reviews cover every CASE label, different ratings and unreviewed books.
INSERT INTO REVIEW VALUES
(5001,4001,4001,5,'2026-11-01'),
(5002,4001,4002,4,'2026-11-02'),
(5003,4002,4001,5,'2026-11-03'),
(5004,4002,4002,5,'2026-11-04'),
(5005,4003,4001,3,'2026-11-05'),
(5006,4003,4002,4,'2026-11-06'),
(5007,4004,4001,2,'2026-11-07'),
(5008,4005,4003,4,'2026-11-08'),
(5009,4006,4004,1,'2026-11-09');
