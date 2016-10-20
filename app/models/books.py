import tornado.web
import psycopg2
import psycopg2.extensions



class Books():
    
    def add_book(self,title, excerpt, author, publisher, year, isbn, ufile, category):
        conn = psycopg2.connect(host="localhost",database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("INSERT INTO books(title, excerpt, author, publisher, published_date, isbn, file, category) VALUES (%s,%s,%s,%s,%s,%s,%s, %s) RETURNING id", (title, excerpt, author, publisher, year, isbn, ufile, category))
        book = curr.fetchone()
        conn.commit()
        return book[0]
        
    def get_books(self, sort_column = 'ID', sort_order = 'DESC', limit = 10, offset = 0):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM books ORDER BY %s %s LIMIT %s OFFSET %s"% (sort_column,sort_order,limit,offset))
        books = curr.fetchall()
        return books
        
    def get_book(self, book):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM books WHERE id = %s", (book,))
        book = curr.fetchone()
        return book
        
    def search_book(self, search):
        search = search.lower()
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM books WHERE LOWER(title) LIKE '%%' || %s || '%%' OR LOWER(author) LIKE '%%' || %s || '%%'", (search, search,))
        books = curr.fetchall()
        return books
        
    def count_books(self):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM books")
        books = curr.rowcount
        return books
        
    def delete_books(self,id):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("DELETE FROM books WHERE id=%s",(id,))
        conn.commit()
        return
    def edit_book(self,title, excerpt,author, publisher, published_date, isbn, id):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("UPDATE books SET title = %s, excerpt= %s, author= %s, publisher= %s, published_date= %s," +
        "isbn= %s WHERE id = %s",(title, excerpt, author, publisher,published_date, isbn, id,))
        conn.commit()
        return

    def get_category_books(self, sort_column = 'ID', sort_order = 'DESC', limit = 10, offset = 0, category=False):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM books WHERE category=%s ORDER BY %s %s LIMIT %s OFFSET %s"% (category, sort_column,sort_order,limit,offset))
        books = curr.fetchall()
        return books