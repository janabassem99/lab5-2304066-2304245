"""Create Lab 5 once, importing every Lab 4 row and then adding Lab 5 seed cases."""
from pathlib import Path
import os
import pymysql
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / 'website' / '.env')
TARGET = 'library_lab5_2304066'
SOURCE = 'library_lab4_2304066'
TABLES = ('AUTHOR', 'PUBLISHER', 'CATEGORY', 'BOOK', 'MEMBER', 'LOAN')


def statements(filename):
    text = '\n'.join(line for line in (ROOT / filename).read_text().splitlines()
                     if not line.lstrip().startswith('--'))
    return [statement.strip() for statement in text.split(';') if statement.strip()]


def main():
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'), port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'root'), password=os.getenv('DB_PASSWORD', ''),
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
    )
    with connection, connection.cursor() as cursor:
        cursor.execute('SELECT VERSION() AS version')
        print('MySQL', cursor.fetchone()['version'])
        cursor.execute('SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME=%s', (TARGET,))
        if cursor.fetchone():
            raise SystemExit('Lab 5 already exists. Start the website to continue using it.')
        cursor.execute('SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME=%s', (SOURCE,))
        existing = {}
        if cursor.fetchone():
            for table in TABLES:
                cursor.execute(f'SELECT * FROM {SOURCE}.{table}')
                existing[table] = cursor.fetchall()
            # The new reviews reference these existing Lab 4 demonstration IDs.
            for table, key, ids in [('BOOK', 'book_id', range(4001, 4007)),
                                     ('MEMBER', 'member_id', range(4001, 4005))]:
                if not set(ids).issubset({row[key] for row in existing[table]}):
                    raise SystemExit('Some Lab 4 demo books/members are missing. Review the new review seed IDs before importing.')
        for statement in statements('problem2_DDL.sql'):
            if not statement.upper().startswith('DROP DATABASE'):
                cursor.execute(statement)
        if existing:
            for table, records in existing.items():
                if records:
                    columns = list(records[0])
                    sql = (f"INSERT INTO {table} (" + ','.join(f'`{c}`' for c in columns)
                           + ') VALUES (' + ','.join(['%s'] * len(columns)) + ')')
                    cursor.executemany(sql, [tuple(row[c] for c in columns) for row in records])
            cursor.execute("SELECT country FROM AUTHOR WHERE country NOT IN (SELECT country FROM PUBLISHER)")
            if not cursor.fetchone():
                cursor.execute('SELECT COALESCE(MAX(author_id),0)+1 AS next_id FROM AUTHOR')
                new_id = cursor.fetchone()['next_id']
                cursor.execute('INSERT INTO AUTHOR VALUES (%s,%s,%s)',
                               (new_id, 'Demo Spanish Author', 'Spain'))
            # Read only the REVIEW insert from the fresh seed script.
            for statement in statements('problem2_DML.sql'):
                if statement.startswith('INSERT INTO REVIEW'):
                    cursor.execute(statement)
            print('Copied Lab 4 rows', {table: len(records) for table, records in existing.items()})
        else:
            for statement in statements('problem2_DML.sql'):
                cursor.execute(statement)
            print('Created the fresh seven-table demonstration dataset.')
        connection.commit()
        cursor.execute('SELECT COUNT(*) AS reviews FROM REVIEW')
        print('Lab 5 ready', cursor.fetchone())


if __name__ == '__main__':
    main()
