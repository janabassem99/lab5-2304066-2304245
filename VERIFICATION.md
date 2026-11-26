# Lab 5 verification

Run python check_lab5.py to verify the new SQL and website using a disposable database.

Passed on MySQL 8.4.11:
- DDL, DML and every query script execute successfully.
- Seven tables and the book_details view exist.
- Nine seed reviews and every requested data case are present.
- Fourteen report SELECTs return the expected seed results.
- NOT EXISTS reports equal the earlier LEFT JOIN reports.
- CHECK rejects ratings 0 and 6. UNIQUE rejects duplicate book/member pairs.
- Foreign keys reject missing books and members.
- Author deletion cascades through books to loans and reviews.
- Tied category maxima appear, and the view reads updated base table values.
- Fifteen page requests, earlier labs, invalid routes and bonus labels behave correctly.
- Lab 4 search treats injection-style inputs as data.

Local preparation copied 7 authors, 4 publishers, 4 categories, 14 books, 5 members and 12 loans from Lab 4 before adding the Lab 5 examples. The local report totals include those copied rows.
