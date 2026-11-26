"""Check Lab 5 SQL and routes in a uniquely named disposable MySQL database."""
from decimal import Decimal
from pathlib import Path
import sys
import tempfile
import uuid

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'website'))
import pymysql
from app import create_app
from lab5_queries import QUERIES
from lab4_queries import QUERIES as LAB4

TARGET = 'lab5_verify_' + uuid.uuid4().hex[:12]
with tempfile.TemporaryDirectory() as uploads:
    app = create_app({'TESTING': True, 'DB_NAME': TARGET, 'UPLOAD_FOLDER': uploads})
    config = app.config
    connection = pymysql.connect(
        host=config['DB_HOST'], port=config['DB_PORT'], user=config['DB_USER'],
        password=config['DB_PASSWORD'], charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    with connection, connection.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE {TARGET}')
        try:
            for filename in ['problem2_DDL.sql', 'problem2_DML.sql', 'problem2_Queries.sql']:
                sql = '\n'.join(line for line in (ROOT / filename).read_text().splitlines()
                                if not line.lstrip().startswith('--'))
                sql = sql.replace('library_lab5_2304066', TARGET)
                for statement in sql.split(';'):
                    if statement.strip() and not statement.strip().upper().startswith(('DROP DATABASE', 'CREATE DATABASE')):
                        cursor.execute(statement)
            connection.commit()

            def result(key):
                cursor.execute(QUERIES[key])
                return list(cursor.fetchall())

            for table, count in [('AUTHOR', 5), ('PUBLISHER', 3), ('CATEGORY', 3),
                                 ('BOOK', 10), ('MEMBER', 5), ('LOAN', 12), ('REVIEW', 9)]:
                cursor.execute(f'SELECT COUNT(*) AS n FROM {table}')
                assert cursor.fetchone()['n'] == count, table
            assert len(result('above_average')) == 5
            assert all(row['library_average'] == Decimal('19.950000') for row in result('above_average'))
            assert len(result('category_best')) == 3
            assert len(result('category_above')) == 5
            assert result('loan_average')[0]['average_loans_per_member'] == Decimal('2.4000')
            assert [row['member_id'] for row in result('active_members')] == [4001, 4002]
            assert len(result('borrowed_authors')) == 2
            reviews = result('reviews')
            assert [row['rating_label'] for row in reviews[:6]] == ['Excellent', 'Excellent', 'Good', 'Fair', 'Good', 'Fair']
            assert all(row['average_rating'] == 0 and row['rating_label'] == 'No review' for row in reviews[6:])
            assert {row['book_id'] for row in result('reviews_above')} == {4001, 4002, 4005}
            assert [row['country'] for row in result('author_countries')] == ['Spain']
            assert len(result('countries')) == 4 and len(result('both_countries')) == 3
            assert len(result('people')) == 10
            for new, old in [('never_books', 'no_books'), ('never_members', 'no_members')]:
                expected = result(new)
                cursor.execute(LAB4[old])
                assert expected == list(cursor.fetchall()), new

            # Rejections must be enforced in MySQL as well as any UI.
            for values, expected_code in [
                ((9991, 4007, 4001, 0, '2026-11-10'), 3819),
                ((9992, 4007, 4001, 6, '2026-11-10'), 3819),
                ((9993, 4001, 4001, 4, '2026-11-10'), 1062),
                ((9994, 999999, 4001, 4, '2026-11-10'), 1452),
                ((9995, 4007, 999999, 4, '2026-11-10'), 1452),
            ]:
                try:
                    cursor.execute('INSERT INTO REVIEW VALUES (%s,%s,%s,%s,%s)', values)
                except pymysql.MySQLError as error:
                    assert error.args[0] == expected_code, error
                else:
                    raise AssertionError('Invalid review was accepted')

            # Correlated MAX preserves ties. A view reads current table data.
            cursor.execute('UPDATE BOOK SET price=30 WHERE book_id=4001')
            assert len(result('category_best')) == 3
            cursor.execute('UPDATE BOOK SET price=25 WHERE book_id=4001')
            assert len(result('category_best')) == 4  # Fiction has a 25.00 tie.
            cursor.execute('SELECT price FROM book_details WHERE book_id=4001')
            assert cursor.fetchone()['price'] == Decimal('25.00')
            connection.rollback()

            # Book cascade removes both review and loan rows; author cascade reaches reviews.
            cursor.execute('DELETE FROM AUTHOR WHERE author_id=4001')
            for table in ['BOOK', 'LOAN', 'REVIEW']:
                column = 'author_id' if table == 'BOOK' else 'book_id'
                condition = '=4001' if table == 'BOOK' else ' IN (4001,4002,4003)'
                cursor.execute(f'SELECT COUNT(*) AS n FROM {table} WHERE {column}{condition}')
                assert cursor.fetchone()['n'] == 0
            connection.rollback()

            client = app.test_client()
            routes = ['/', '/lab5/', '/lab5/above-average', '/lab5/never-borrowed',
                      '/lab5/categories', '/lab5/active-members', '/lab5/reviews',
                      '/lab5/countries', '/lab5/discussion', '/library/',
                      '/lab4/', '/lab4/reports', '/lab4/loans', '/lab4/authors', '/lab2/']
            for route in routes:
                response = client.get(route, follow_redirects=True)
                assert response.status_code == 200, (route, response.status_code)
            for page in ['above-average', 'categories']:
                assert b'Bonus implemented' in client.get('/lab5/' + page).data
            assert client.get('/lab5/unknown').status_code == 404
            for keyword in ["' OR 1=1 --", "'; SELECT 1; #"]:
                response = client.get('/lab4/search', query_string={'keyword': keyword})
                assert response.status_code == 200 and b'No matching records' in response.data
            print('PASS: all scripts, 7 tables, 9 reviews, 14 queries, Lab 4 equivalence,')
            print('CHECK/UNIQUE/FK rejections, cascade, ties, live view, 15 routes, bonus labels and injection checks.')
        finally:
            cursor.execute(f'DROP DATABASE {TARGET}')
