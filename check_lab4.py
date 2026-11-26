"""Integration checks use a disposable database; never mutate the real library."""
from pathlib import Path
import sys, re
sys.path.insert(0,str(Path(__file__).parent/'website'))
from app import create_app
from lab4_queries import QUERIES
import pymysql
root=Path(__file__).parent
app=create_app({'TESTING':True,'DB_NAME':'lab4_verification_2304066','UPLOAD_FOLDER':'/tmp/lab4-test-uploads'})
c=pymysql.connect(host=app.config['DB_HOST'],port=app.config['DB_PORT'],user=app.config['DB_USER'],password=app.config['DB_PASSWORD'],cursorclass=pymysql.cursors.DictCursor)
with c,c.cursor() as q:
 q.execute('CREATE DATABASE IF NOT EXISTS lab4_verification_2304066')
 try:
  for file in ['problem2_DDL.sql','problem2_DML.sql','problem2_Queries.sql']:
   sql='\n'.join(x for x in (root/'lab4-reference'/file).read_text().splitlines() if not x.strip().startswith('--')).replace('library_lab4_2304066','lab4_verification_2304066')
   for statement in sql.split(';'):
    if statement.strip(): q.execute(statement)
  c.commit()
  for table,total in [('AUTHOR',4),('PUBLISHER',3),('CATEGORY',3),('BOOK',10),('MEMBER',5),('LOAN',12)]:
   q.execute('SELECT COUNT(*) AS n FROM '+table); assert q.fetchone()['n']==total
  q.execute(QUERIES['prices']); assert float(q.fetchone()['total_price'])==199.5
  q.execute(QUERIES['top_books']); assert [r['loans'] for r in q.fetchall()]==[4,3,2]
  q.execute(QUERIES['top_member']); assert q.fetchone()['member_id']==4001
  q.execute(QUERIES['authors']); assert q.fetchall()[-1]['books']==0
  q.execute(QUERIES['active_loans']); assert len(q.fetchall())==4
  client=app.test_client()
  for route in ['/','/library/','/library/books/add','/library/books/4001/edit','/lab4/','/lab4/catalogue','/lab4/reports','/lab4/loans','/lab4/popular','/lab4/authors','/lab4/discussion','/lab2/']:
   response=client.get(route); assert response.status_code in [200,302],(route,response.status_code)
  r=client.get('/lab4/search?keyword=Palace&minimum=15&maximum=20&category=4001'); assert b'Palace Walk' in r.data and b'Palace of Desire' not in r.data
  r=client.get('/lab4/search',query_string={'keyword':"' OR 1=1 --"}); assert b'No matching records' in r.data
  for args in [{'minimum':'30','maximum':'10'},{'minimum':'NaN'},{'category':'bad'}]:
   r=client.get('/lab4/search',query_string=args); assert r.status_code==200 and b'role="alert"' in r.data
  with client.session_transaction() as session: session['library_csrf']='test'
  data=dict(csrf_token='test',book_id=9999,title='Test Book',price='17.50',author_id=4001,publisher_id=4001,category_id=4001,publish_year=2026)
  assert client.post('/library/books/add',data=data).status_code==302
  data['title']='Updated Book'; assert client.post('/library/books/9999/edit',data=data).status_code==302
  c.commit(); q.execute('SELECT title FROM BOOK WHERE book_id=9999'); assert q.fetchone()['title']=='Updated Book'
  assert client.post('/library/books/9999/delete',data={'csrf_token':'test'}).status_code==302
  c.commit()
  # Check both levels of cascade without touching the user's database.
  q.execute('DELETE FROM AUTHOR WHERE author_id=4001')
  q.execute('SELECT COUNT(*) AS n FROM BOOK WHERE author_id=4001'); assert q.fetchone()['n']==0
  q.execute('SELECT COUNT(*) AS n FROM LOAN WHERE book_id IN (4001,4002,4003)'); assert q.fetchone()['n']==0
  c.rollback()
  print('PASS: SQL scripts, 6 seed counts, aggregate results, 13 routes, combined filters, injection input, invalid inputs, book add/edit/delete and author-book-loan cascade.')
 finally:
  q.execute('DROP DATABASE IF EXISTS lab4_verification_2304066')
