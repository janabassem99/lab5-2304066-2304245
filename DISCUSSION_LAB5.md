# Lab 5 discussion guide

Jana Bassem - 2304066 | Farida Mohamed - 2304245

## Start with the database

"My Lab 5 website continues the previous library. I added REVIEW so a member can rate a book. The library now has seven tables. I use complex SELECT queries for the new reports."

AUTHOR, PUBLISHER and CATEGORY each have a one-to-many relationship with BOOK. BOOK and MEMBER each have a one-to-many relationship with LOAN and REVIEW. A loan is one borrowing event. A review is one member's rating of a book.

REVIEW has five columns.
- review_id INT PRIMARY KEY identifies one review.
- book_id INT NOT NULL references BOOK.
- member_id INT NOT NULL references MEMBER.
- rating INT NOT NULL has CHECK(rating BETWEEN 1 AND 5).
- review_date DATE NOT NULL records the date.

UNIQUE(book_id, member_id) enforces one review from each member for each book. A member may review several books and a book may receive reviews from several members. A duplicate pair is rejected even if it uses a new review_id.

ON DELETE CASCADE on REVIEW.book_id deletes a book's reviews when the book is deleted. The existing author-to-book and book-to-loan cascades remain. A referenced member cannot be deleted under the restrictive foreign key. CHECK, UNIQUE and FOREIGN KEY are enforced by MySQL even when inserts bypass the website.

## F2.1 - Scalar subquery

A scalar subquery returns one value. SELECT AVG(price) FROM BOOK returns the whole library's average price. The outer SELECT keeps rows above that average, displays the average in each row and orders by price DESC.

Fresh seed has 10 books totalling 199.50, so average is 19.95. Five prices exceed it. The live database also contains imported books.

**Bonus** - this query reads book_details, so its catalogue joins are reused through the view.

## F2.2 - NOT EXISTS

For each book b, the subquery looks for a LOAN where l.book_id = b.book_id. NOT EXISTS is true only when there are no matching rows. The member version matches member_id instead.

This is correlated because it refers to the outer b or m. It expresses "there is no borrowing record". A loan whose return_date is filled still proves the book was borrowed.

Lab 4 used LEFT JOIN followed by WHERE l.loan_id IS NULL for the same question. The verification compares both result sets and confirms identical rows.

EXISTS tests the existence of rows. SELECT * inside it does not mean that all inner columns are displayed to the user.

## F2.3 - Correlated subqueries

A correlated subquery refers to an outer row. Here, b.category_id = d.category_id selects books in the current outer book's category.

For the most expensive book, compare d.price to MAX(price) from that category. Equal prices at the maximum all qualify. Ordering by book_id does not discard ties.

For above-category-average books, compare d.price with AVG(price) in the same category. The displayed category_average comes from a scalar subquery in SELECT. If a category has one book, that book equals its average and is excluded by the strict greater-than condition.

**Bonus** - both queries use book_details for category names and book fields.

## F2.4 - Derived table and EXISTS

A derived table is a SELECT in FROM with an alias. First, group every MEMBER with their LOAN rows and COUNT(l.loan_id). LEFT JOIN preserves a member with zero loans. COUNT(l.loan_id) ignores the NULL match and returns zero.

Then AVG(t.loan_count) computes the average of those per-member counts. Fresh seed gives counts 5, 3, 2, 2, 0. Their average is 2.40. HAVING retains the members with 5 and 3.

Counting only members found in LOAN would give 12 / 4 = 3.00 and change the result. The zero-loan member must count in the denominator.

For borrowed authors, EXISTS contains BOOK joined to LOAN and matches b.author_id to the outer author. The outer AUTHOR is selected once, even if the author has many books and many loans.

## F2.5 - Review reports

LEFT JOIN keeps books without reviews. COUNT(r.review_id) counts real review rows. AVG(r.rating) is NULL for no reviews. COALESCE(AVG(r.rating), 0) returns the first non-NULL value, giving zero in that case.

CASE evaluates conditions in order.
1. Zero reviews gives No review.
2. Average at least 4.5 gives Excellent.
3. Average at least 3.5 gives Good.
4. Otherwise gives Fair.

Use the raw average for classification. The page formats numeric display to two decimals. A display rounded up to 4.50 can still have a raw value below 4.5, so classification must use the actual average.

Fresh examples are Palace Walk 4.50 Excellent, Sugar Street 3.50 Good, The Map of Love 2.00 Fair and Animal Farm 0.00 No review.

The second query groups reviews by book. HAVING AVG(r.rating) > (SELECT AVG(rating) FROM REVIEW) keeps books above the average of all review rows. The nine seeded ratings total 33, so the global average is 33 / 9 = 3.6667.

This weights every individual review equally. Averaging each book's average would be a different calculation when books have different review counts. Books without reviews do not contribute invented zero ratings to the global average.

## F2.6 - Set operators

Both SELECT statements in a set operation must return the same number of compatible columns.

UNION joins author and publisher country lists and removes duplicate rows. ORDER BY comes at the end and sorts the combined result.

INTERSECT returns countries present in both lists. In the fresh data, Egypt, France and United Kingdom appear in both.

EXCEPT returns author countries missing from the publisher list. Spain is the fresh example. Reversing the two SELECTs asks a different question.

UNION ALL combines author and member names with a type column. It keeps separate people with identical names. The result sorts by name and type. We use native INTERSECT and EXCEPT, which need MySQL 8.0.31 or later. Jana's MySQL 8.4.11 supports them.

## BONUS - book_details view

Point to CREATE VIEW book_details at the end of problem2_DDL.sql. It saves the join of BOOK, AUTHOR, PUBLISHER and CATEGORY, with book fields and readable names.

Then point to FROM book_details d in F2.1 and both F2.3 queries. Those pages have an explicit bonus notice.

"A view stores a SELECT definition. When I query it, it reads the current data from its base tables. I reused the catalogue join in three report queries."

In DBeaver, expand Views and open book_details. Run SHOW CREATE VIEW book_details. The integration check updates a book inside a temporary transaction, queries the view and verifies that its price changes, then rolls the transaction back.

## Python functions to explain

create_app() in website/app.py registers the lab5 Blueprint at /lab5 alongside the old library and Lab 4 routes. DispatcherMiddleware mounts the Lab 2 app at /lab2 using its registration database.

report(page) in website/lab5.py accepts one of six known page names. PAGES maps that name to a heading and allowed query keys. Unknown names return 404. The query text comes from website/lab5_queries.py.

rows(sql, parameters) in website/lab4.py calls cursor.execute(sql, parameters), then fetchall(). database() in website/library.py opens a MySQL connection from .env and closes it afterwards. The returned dictionaries are rendered in lab5.html.

Lab 5 reports have fixed SELECT queries and take no free-text SQL input. The earlier search uses bound %s values. Entering a SQL command in its title field is treated as search data. A MySQL account that has DROP privileges can still drop a database by directly executing SQL in DBeaver.

The website and DBeaver are clients. MySQL stores the records. Both clients must use library_lab5_2304066 to view the same rows. DBeaver needs refresh after website edits and commit after manual edits if manual commit is enabled.

## Discussion walkthrough

1. Open the lab hub and select Lab 5. Show the same typography, colours and earlier lab links.
2. In DBeaver, show seven tables and the book_details view.
3. Open Above average and explain the scalar query and view bonus.
4. Open Never borrowed and compare its IDs with Lab 4 Loans.
5. Open Categories and explain why the inner query refers to d.category_id.
6. Open Active members and show the average plus qualifying members.
7. Open Reviews and explain all four CASE labels, zero reviews and the global average.
8. Open Countries and explain UNION, INTERSECT, EXCEPT and UNION ALL.
9. Show problem2_Queries.sql with labels F2.1-F2.6.
10. Explain the CHECK and UNIQUE rejections using the results from python check_lab5.py.

## Practice answers

Why a subquery here? I compare a book with an average computed from other rows.

Why is F2.3 correlated? The inner category filter refers to the current outer book's category_id.

Why NOT EXISTS? I need books or members with no matching loan at all.

Why LEFT JOIN for the average loan count? Every member must count, including members with zero loans.

Why COUNT(review_id) instead of COUNT(*)? An unmatched book still has one joined output row with NULL review fields.

Why COALESCE? It displays zero where AVG returns NULL for no reviews.

Why check No review first in CASE? It gives an unreviewed book its own label before applying rating thresholds.

Why HAVING? It filters groups after their average or count has been computed.

What happens if two books tie for maximum? Both appear.

Why UNIQUE on two columns? The member-book pair must be unique, while either column alone may repeat.

What does the view bonus save? Repeated catalogue join definitions in F2.1 and F2.3.

What is actually being tested? check_lab5.py creates a temporary database, runs the real SQL scripts, checks query results and constraints, exercises the pages and removes its temporary database.

## Data and submission scope

The local Lab 5 setup copied the existing Lab 4 records into library_lab5_2304066. It then added nine reviews and an author-country example. The source library database is a snapshot source, so future changes to Lab 4 do not automatically change Lab 5. The earlier library forms within this Lab 5 application all access Lab 5.

This work implements Part II. Part I COMPANY files require their own schema, seeds and answers.
