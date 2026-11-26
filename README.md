# The Reading Room - Lab 5, Part II

**Jana Bassem - 2304066**  
**Farida Mohamed - 2304245**

The same Flask library website continues Labs 2, 3 and 4, with seven library tables and six new Lab 5 pages. MySQL 8.0.31 or later is required for INTERSECT and EXCEPT. Jana's installed MySQL is 8.4.11.

## Start the website

Open lab5-2304066.code-workspace in VS Code to load this project folder. On a new machine, create the Python environment and install the dependencies.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r website/requirements.txt
```

Copy website/.env.example to website/.env. Enter your own MySQL password and keep DB_NAME=library_lab5_2304066. Keep LAB2_DB_NAME=registration for the earlier task application.

If Lab 4 exists on your machine and Lab 5 has not been created, preserve its current data by running this once.

```sh
python prepare_local.py
```

The helper copies all six Lab 4 tables into the new Lab 5 database and adds the review data and required country example. It refuses to overwrite an existing Lab 5 database. The source data is read as a one-time snapshot. Images are in website/static/uploads and should stay with your local project.

On a fresh machine with no earlier library to copy, run the supplied SQL files instead.

```sh
mysql -u root -p < problem2_DDL.sql
mysql -u root -p < problem2_DML.sql
```

**The DDL drops and recreates the Lab 5 database. Use it for fresh setup. Use problem2_Queries.sql to demonstrate queries against existing data.** Lab 5 has already been prepared on Jana's Mac.

Start the server and keep its terminal open.

```sh
python website/app.py
```

Open http://127.0.0.1:5003/ and choose Lab 5. Its six report pages start at /lab5/. Earlier pages are /lab2/, /library/ and /lab4/. A local server must be running for these addresses to open. On a new machine, Lab 2 also needs its own existing registration database, or its fresh schema in website/lab2/database/schema.sql.

## DBeaver

Open the existing local MySQL connection. Refresh the database list and select library_lab5_2304066. Expand Tables to see AUTHOR, PUBLISHER, CATEGORY, BOOK, MEMBER, LOAN and REVIEW. Expand Views to see book_details.

Open problem2_Queries.sql and run the statements. This SELECT script includes USE library_lab5_2304066. It contains every Lab 5 query, labelled F2.1-F2.6.

```sql
SELECT VERSION();
SELECT DATABASE();
SELECT * FROM REVIEW;
SELECT * FROM book_details;
SHOW CREATE VIEW book_details;
```

Refresh a data tab after website changes. Commit DBeaver edits when manual commit is enabled. Flask and DBeaver both access the same MySQL schema.

## Part II coverage

| Requirement | Page | SQL used |
|---|---|---|
| F2.1 Above average | /lab5/above-average | Scalar AVG subquery and the bonus view |
| F2.2 Never borrowed | /lab5/never-borrowed | Correlated NOT EXISTS for books and members |
| F2.3 Best of category | /lab5/categories | Correlated MAX and AVG subqueries, both using the bonus view |
| F2.4 Active members | /lab5/active-members | Derived table of loan counts including zero, HAVING, EXISTS |
| F2.5 Reviews | /lab5/reviews | LEFT JOIN, COUNT, AVG, CASE, COALESCE, HAVING with overall AVG |
| F2.6 Countries and people | /lab5/countries | UNION, INTERSECT, EXCEPT and typed UNION ALL |
| Discussion | /lab5/discussion | Explanations and bonus demonstration |

F2.2 returns the same book/member IDs as the Lab 4 LEFT JOIN reports, verified by check_lab5.py. F2.3 keeps every book tied at a category's maximum price. F2.4 includes zero-loan members in the denominator. F2.5 compares each book's average with the average of all individual ratings.

## Bonus completed - book_details view

**The full Lab 5 bonus is implemented.**

- problem2_DDL.sql creates book_details by joining BOOK, AUTHOR, PUBLISHER and CATEGORY.
- F2.1 reads FROM book_details d.
- Both F2.3 queries read FROM book_details d.
- The F2.1 and F2.3 website pages display a visible bonus notice.
- DISCUSSION_LAB5.md and /lab5/discussion explain how to demonstrate the view.

The view stores a SELECT definition. Its next SELECT reflects changes committed to the underlying tables. The earlier Lab 4 placeholder bonus is retained in its search form.

## REVIEW constraints

REVIEW has review_id as primary key. book_id references BOOK with ON DELETE CASCADE. member_id references MEMBER. rating is NOT NULL and CHECK(rating BETWEEN 1 AND 5). UNIQUE(book_id, member_id) prevents the same member reviewing the same book twice.

Deleting an author cascades to their books, then to their books' reviews and loans. Deleting a member with loans or reviews is restricted. Deleting referenced publishers and categories is restricted.

## Demonstration data and expected fresh results

The fresh DML inserts 5 authors, 3 publishers, 3 categories, 10 books, 5 members, 12 loans and 9 reviews.

- The library average price is 19.95. Five books are above it.
- Spain has an author and no publisher.
- Palace Walk has ratings 5 and 4, an average of 4.50 and the Excellent label.
- Sugar Street has ratings 3 and 4, an average of 3.50 and the Good label.
- The Map of Love averages 2.00 and is Fair. Animal Farm has zero reviews, an average displayed as 0 and No review.
- The average of all 9 ratings is 3.6667. Palace Walk, Palace of Desire and In the Eye of the Sun exceed it.
- Average loans per member is 12 / 5 = 2.40. Demo Reader A has 5 and Demo Reader B has 3.
- Four books were never borrowed and one member has no loans.
- A one-book category returns that book as its maximum and returns no books above its category average.

Jana's local Lab 5 database also includes all imported Lab 4 data, so live totals and averages can differ from the fresh seed results.

## Files and discussion

- problem2_DDL.sql, problem2_DML.sql and problem2_Queries.sql are the required Part II scripts.
- website/lab5_queries.py contains the same report SQL.
- website/lab5.py maps the page names to the queries. rows() in website/lab4.py executes them.
- DISCUSSION_LAB5.md explains each query, the constraints, the Python flow and practice answers.
- lab4-reference/ and lab3-reference/ preserve earlier SQL and notes.
- prepare_local.py performs the one-time copy. check_lab5.py verifies the new work.

This project covers the requested **Part II**. Part I COMPANY scripts and answers are separate handout deliverables.

## Verification

```sh
python check_lab5.py
```

The check creates a uniquely named temporary database and removes it afterwards. It needs CREATE and DROP privileges for that test database. It verifies all scripts, seven tables, fourteen queries, expected seed results, Lab 4 equivalence, invalid/duplicate/orphan review rejection, cascades, tied prices, live view data, earlier routes, bonus notices and search injection inputs. It never drops or writes your working library databases.

Passwords, .env, session files, virtual environments and personal image uploads are excluded from a shareable project. Use the sample .env.example to configure another machine.
