import tornado.web
import psycopg2
import psycopg2.extensions

class Categories():

    def get_categories(self, sort_column='ID', sort_order='DESC', limit=10, offset=0):
        conn = psycopg2.connect(host="localhost", database="archives", user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM categories ORDER BY %s %s LIMIT %s OFFSET %s" % (sort_column, sort_order, limit, offset))
        categories = curr.fetchall()
        return categories

    def count_categories(self):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM categories")
        categories = curr.rowcount
        return categories

    def add_categories(self, category):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("INSERT INTO categories(category) VALUES (%s) RETURNING id", (category,))
        category = curr.fetchone()
        conn.commit()
        return category[0]