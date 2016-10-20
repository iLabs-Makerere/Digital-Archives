import psycopg2
import psycopg2.extensions

class Users():
    
    def get_user(self,email):
        conn = psycopg2.connect(host="localhost",database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curr.fetchall()
        return user
        
    def get_users(self, limit = 10, offset = 0):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM users LIMIT %s OFFSET %s", (limit,offset))
        users = curr.fetchall()
        return users
        
    def count_users(self):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("SELECT * FROM users")
        users = curr.rowcount
        return users
        
    def delete_users(self,email):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("DELETE FROM users WHERE email=%s",(email,))
        conn.commit()
        return
    def edit_user(self,first_name, last_name, newemail, affiliation, identity, gender, password, role, email):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("UPDATE users SET first_name = %s, last_name= %s, email= %s, affiliation= %s, identity= %s," +
        "gender= %s, password= %s, role= %s WHERE email = %s",(first_name, last_name, newemail, affiliation, identity, gender, password, role, email))
        conn.commit()
        return
    def add_user(self,first_name, last_name, newemail, affiliation, identity, gender, password, role, email):
        conn = psycopg2.connect(host="localhost", database="archives",user="postgres", password="qwertyuiop")
        curr = conn.cursor()
        curr.execute("INSERT INTO users(first_name, last_name, email, affiliation, identity, gender, password, role) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id", (first_name, last_name, newemail, affiliation, identity, gender, password, role, email))
        user = curr.fetchone()
        conn.commit()
        return book[0]