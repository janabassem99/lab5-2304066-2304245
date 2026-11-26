"""Lab 5 SELECT queries, with the book_details view bonus in F2.1 and F2.3."""

QUERIES = {
    # F2.1 BONUS: use the saved catalogue join.
    'above_average': """
SELECT d.title, d.price, (SELECT AVG(price) FROM BOOK) AS library_average
FROM book_details d
WHERE d.price > (SELECT AVG(price) FROM BOOK)
ORDER BY d.price DESC, d.book_id
""",
    # F2.2(a)
    'never_books': """
SELECT b.book_id, b.title
FROM BOOK b
WHERE NOT EXISTS (SELECT * FROM LOAN l WHERE l.book_id = b.book_id)
ORDER BY b.book_id
""",
    # F2.2(b)
    'never_members': """
SELECT m.member_id, m.name, m.email
FROM MEMBER m
WHERE NOT EXISTS (SELECT * FROM LOAN l WHERE l.member_id = m.member_id)
ORDER BY m.member_id
""",
    # F2.3(a) BONUS: the view supplies the category name. Keep all tied maxima.
    'category_best': """
SELECT d.category, d.title, d.price
FROM book_details d
WHERE d.price = (
    SELECT MAX(b.price) FROM BOOK b WHERE b.category_id = d.category_id
)
ORDER BY d.category, d.book_id
""",
    # F2.3(b) BONUS: compare each row with its own category average.
    'category_above': """
SELECT d.category, d.title, d.price,
       (SELECT AVG(b.price) FROM BOOK b WHERE b.category_id = d.category_id) AS category_average
FROM book_details d
WHERE d.price > (
    SELECT AVG(b.price) FROM BOOK b WHERE b.category_id = d.category_id
)
ORDER BY d.category, d.price DESC, d.book_id
""",
    # F2.4(a): left join includes members with zero loans before averaging.
    'loan_average': """
SELECT AVG(t.loan_count) AS average_loans_per_member
FROM (
    SELECT m.member_id, COUNT(l.loan_id) AS loan_count
    FROM MEMBER m LEFT JOIN LOAN l ON l.member_id = m.member_id
    GROUP BY m.member_id
) t
""",
    'active_members': """
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
ORDER BY loans DESC, m.member_id
""",
    # F2.4(b)
    'borrowed_authors': """
SELECT a.author_id, a.name
FROM AUTHOR a
WHERE EXISTS (
    SELECT * FROM BOOK b JOIN LOAN l ON l.book_id = b.book_id
    WHERE b.author_id = a.author_id
)
ORDER BY a.author_id
""",
    # F2.5(a): test the zero-review case before the numeric thresholds.
    'reviews': """
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
ORDER BY b.book_id
""",
    # F2.5(b): average of individual ratings, including every review.
    'reviews_above': """
SELECT b.book_id, b.title, AVG(r.rating) AS average_rating,
       (SELECT AVG(rating) FROM REVIEW) AS overall_average
FROM BOOK b JOIN REVIEW r ON r.book_id = b.book_id
GROUP BY b.book_id, b.title
HAVING AVG(r.rating) > (SELECT AVG(rating) FROM REVIEW)
ORDER BY average_rating DESC, b.book_id
""",
    # F2.6(a)
    'countries': """
SELECT country FROM AUTHOR
UNION
SELECT country FROM PUBLISHER
ORDER BY country
""",
    # F2.6(b): native MySQL INTERSECT, version 8.0.31+.
    'both_countries': """
SELECT country FROM AUTHOR
INTERSECT
SELECT country FROM PUBLISHER
ORDER BY country
""",
    # F2.6(c)
    'author_countries': """
SELECT country FROM AUTHOR
EXCEPT
SELECT country FROM PUBLISHER
ORDER BY country
""",
    # F2.6(d): preserve different people who happen to share a name.
    'people': """
SELECT name, 'Author' AS type FROM AUTHOR
UNION ALL
SELECT name, 'Member' AS type FROM MEMBER
ORDER BY name, type
""",
}

PAGES = {
    'above-average': ('Beyond the average.', 'Books priced above the library average.',
                      [('Above the library average', 'above_average')], True),
    'never-borrowed': ('Waiting for a reader.', 'Books and members with no borrowing history.',
                       [('Never-borrowed books', 'never_books'), ('Members with no loans', 'never_members')], False),
    'categories': ('The best of each category.', 'Compare prices within each category.',
                   [('Most expensive books in each category', 'category_best'),
                    ('Above their category average', 'category_above')], True),
    'active-members': ('Our active readers.', 'Loan counts include every member, including those with zero loans.',
                       [('Average loans per member', 'loan_average'), ('Members above that average', 'active_members'),
                        ('Authors whose books were borrowed', 'borrowed_authors')], False),
    'reviews': ('What readers think.', 'Every book, its average rating and reader verdict.',
                [('All books and ratings', 'reviews'), ('Rated above the overall average', 'reviews_above')], False),
    'countries': ('Countries and people.', 'Explore the people and places behind the library.',
                  [('Author and publisher countries', 'countries'), ('Countries in both', 'both_countries'),
                   ('Author countries without publishers', 'author_countries'), ('Authors and members', 'people')], False),
}
