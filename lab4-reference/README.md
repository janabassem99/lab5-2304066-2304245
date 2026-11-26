# The Reading Room — Lab 4, Part II
**Jana Bassem — 2304066**  
**Farida Mohamed — 2304245**

An extension of our Lab 2 and Lab 3 Flask website, with the same simple interface. All F2.1–F2.6 features and the placeholder bonus are included. Part I is not included. The handout specifies a group of three; add your third teammate's details before submission.

## Start the website
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r website/requirements.txt
```
Copy website/.env.example to website/.env and enter your own MySQL credentials. Use DB_NAME=library_lab4_2304066 and LAB2_DB_NAME=registration. Never publish .env, session files or existing personal data.

On a **fresh machine only**, create and seed Lab 4:
```sh
mysql -u root -p < problem2_DDL.sql
mysql -u root -p < problem2_DML.sql
```
The DDL resets library_lab4_2304066. Do not rerun it on your working database if you want to keep your changes. It does not reset Lab 2 or Lab 3.

If you already have Lab 3 and Lab 4 does not exist, run `python prepare_local.py` instead of those two commands to preserve your old library rows. This refuses to overwrite an existing Lab 4 database. Jana's local database has already been prepared; just start the server.

For Lab 2, keep the existing registration database. On a new machine ONLY, use website/lab2/database/schema.sql to create it; that original script resets registration, so never run it over accounts/tasks you want to keep.

```sh
python website/app.py
```
Open http://127.0.0.1:5003/ . Lab 2 is /lab2/, original library forms are /library/, and Lab 4 is /lab4/. Lab 4 discussion notes are /lab4/discussion.

## DBeaver
Connect to the same host, port, user and password as website/.env (normally 127.0.0.1:3306). Refresh the connection and expand library_lab4_2304066 → Tables. The six tables are AUTHOR, PUBLISHER, CATEGORY, BOOK, MEMBER and LOAN. Open problem2_Queries.sql in an SQL editor and execute the script. It starts with USE library_lab4_2304066 and contains runnable sample values for the search.
Refresh table data after website changes. Commit DBeaver changes if manual commit is enabled, then refresh the website. Do not execute the reset DDL merely to refresh the display.

## Requirements
| Feature | URL | SQL |
|---|---|---|
| F2.1 Search + placeholder bonus | /lab4/search | LIKE, BETWEEN, WHERE, ORDER BY; parameter tuple |
| F2.2 Catalogue | /lab4/catalogue | JOIN four tables |
| F2.3 Reports | /lab4/reports | GROUP BY, HAVING, COUNT, AVG, SUM, MIN, MAX |
| F2.4 Loans | /lab4/loans | JOIN, LEFT JOIN, IS NULL |
| F2.5 Most borrowed | /lab4/popular | GROUP BY, ORDER BY, LIMIT |
| F2.6 Authors | /lab4/authors | LEFT JOIN counts and same-country JOIN |

The DML has 4 authors, 3 publishers, 3 categories, 10 books, 5 members and 12 loans, covering all required edge cases. Local imported Lab 3 records add to these counts. Imported books have unknown publisher/category labels and NULL years until you edit them. Images remain local files. The updated book form includes publisher, category and publication year.

## Files for submission
- problem2_DDL.sql: clean six-table schema with foreign keys and cascading deletes.
- problem2_DML.sql: repeatable demonstration seed for a fresh schema.
- problem2_Queries.sql: every F2 query, labelled, runnable in MySQL/DBeaver.
- website/: Flask site including earlier labs and new pages.
- DISCUSSION_LAB4.md: explanations, expected seed results and practice questions.
- README.md: setup instructions.

lab3-reference/ preserves the old Lab 3 SQL and README for reference, not Lab 4 setup. prepare_local.py imports existing records into a new database. check_lab4.py verifies the SQL and website against a disposable database, requiring CREATE/DROP DATABASE privileges. It never writes to the user's library or registration tables.

## Verification
```sh
python check_lab4.py
```
Checks cover seed counts, reports, all pages, combined search filters, injection-style search text, invalid inputs, book add/edit/delete and cascading deletion. Test data is isolated in lab4_verification_2304066 and removed afterwards.

## Discussion
Read DISCUSSION_LAB4.md or open /lab4/discussion. The source query definitions are website/lab4_queries.py; page handlers are website/lab4.py. MySQL stores data; DBeaver and Flask both access it. Lab 2 retains its own database and login session. DispatcherMiddleware routes /lab2 requests; Flask Blueprints handle the library and reports.
