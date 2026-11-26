-- Lab 5 Part II | Jana Bassem 2304066 | Farida Mohamed 2304245
-- MySQL 8.0.31+ required for native INTERSECT and EXCEPT.
USE library_lab5_2304066;

-- F2.1 BONUS - book_details view
SELECT d.title, d.price, (SELECT AVG(price) FROM BOOK) AS library_average
FROM book_details d
WHERE d.price > (SELECT AVG(price) FROM BOOK)
ORDER BY d.price DESC, d.book_id;

-- F2.2(a)
SELECT b.book_id, b.title
FROM BOOK b
WHERE NOT EXISTS (SELECT * FROM LOAN l WHERE l.book_id = b.book_id)
ORDER BY b.book_id;

-- F2.2(b)
SELECT m.member_id, m.name, m.email
FROM MEMBER m
WHERE NOT EXISTS (SELECT * FROM LOAN l WHERE l.member_id = m.member_id)
ORDER BY m.member_id;

-- F2.3(a) BONUS - book_details view
SELECT d.category, d.title, d.price
FROM book_details d
WHERE d.price = (
    SELECT MAX(b.price) FROM BOOK b WHERE b.category_id = d.category_id
)
ORDER BY d.category, d.book_id;

-- F2.3(b) BONUS - book_details view
SELECT d.category, d.title, d.price,
       (SELECT AVG(b.price) FROM BOOK b WHERE b.category_id = d.category_id) AS category_average
FROM book_details d
WHERE d.price > (
    SELECT AVG(b.price) FROM BOOK b WHERE b.category_id = d.category_id
)
ORDER BY d.category, d.price DESC, d.book_id;

-- F2.4(a) - overall average
SELECT AVG(t.loan_count) AS average_loans_per_member
FROM (
    SELECT m.member_id, COUNT(l.loan_id) AS loan_count
    FROM MEMBER m LEFT JOIN LOAN l ON l.member_id = m.member_id
    GROUP BY m.member_id
) t;

-- F2.4(a) - members above average
SELECT m.member_id, m.name, COUNT(l.loan_id) AS loans
FROM MEMBER m LEFT JOIN LOAN l ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
HAVING COUNT(l.loan_id) > (
    SELECT AVG(t.loan_count)
    FROM (
        SELECT m2.member_id, COUNT(l2.loan_id) AS loan_count
        FROM MEMBER m2 LEFT JOIN LOAN l2 ON l2.member_id = m2.member_id
        GROUP BY m2.member_id
    ) t
)
ORDER BY loans DESC, m.member_id;

-- F2.4(b)
SELECT a.author_id, a.name
FROM AUTHOR a
WHERE EXISTS (
    SELECT * FROM BOOK b JOIN LOAN l ON l.book_id = b.book_id
    WHERE b.author_id = a.author_id
)
ORDER BY a.author_id;

-- F2.5(a)
SELECT b.book_id, b.title, COUNT(r.review_id) AS review_count,
       COALESCE(AVG(r.rating), 0) AS average_rating,
       CASE
           WHEN COUNT(r.review_id) = 0 THEN 'No review'
           WHEN AVG(r.rating) >= 4.5 THEN 'Excellent'
           WHEN AVG(r.rating) >= 3.5 THEN 'Good'
           ELSE 'Fair'
       END AS rating_label
FROM BOOK b LEFT JOIN REVIEW r ON r.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY b.book_id;

-- F2.5(b)
SELECT b.book_id, b.title, AVG(r.rating) AS average_rating,
       (SELECT AVG(rating) FROM REVIEW) AS overall_average
FROM BOOK b JOIN REVIEW r ON r.book_id = b.book_id
GROUP BY b.book_id, b.title
HAVING AVG(r.rating) > (SELECT AVG(rating) FROM REVIEW)
ORDER BY average_rating DESC, b.book_id;

-- F2.6(a)
SELECT country FROM AUTHOR
UNION
SELECT country FROM PUBLISHER
ORDER BY country;

-- F2.6(b)
SELECT country FROM AUTHOR
INTERSECT
SELECT country FROM PUBLISHER
ORDER BY country;

-- F2.6(c)
SELECT country FROM AUTHOR
EXCEPT
SELECT country FROM PUBLISHER
ORDER BY country;

-- F2.6(d)
SELECT name, 'Author' AS type FROM AUTHOR
UNION ALL
SELECT name, 'Member' AS type FROM MEMBER
ORDER BY name, type;
