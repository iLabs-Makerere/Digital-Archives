import os
import tornado.ioloop
import tornado.web
import psycopg2
import psycopg2.pool
from app import routes

if __name__ == "__main__":
	pool = psycopg2.pool.SimpleConnectionPool(1,50,host="localhost",database="archives",user="postgres", password="qwertyuiop")
	static_path = os.path.join(os.path.dirname(__file__), 'static')
	viewer_path = os.path.join(os.path.dirname(__file__), 'viewer')
	settings = {
		'static_path':static_path,
		'cookie_secret':'A082935459fjonp#@#',
		'login_url':'/login',
		'debug': True,
	}
	application = tornado.web.Application([
	    (r"/viewer/(.*)", tornado.web.StaticFileHandler, {"path": viewer_path, "default_filename": "index.html"}),
		(r"/", routes.index.Index),
		(r"/login", routes.users.Login),
		(r"/logout", routes.users.Logout),
		(r"/register", routes.users.Register),
		(r"/publish", routes.books.Publish),
		(r"/upload/(.*)", routes.books.Upload),
		(r"/book/(.*)", routes.books.Book),
		(r"/category/(.*)", routes.category.Category),
		(r"/search", routes.books.Search),
		(r"/manage", routes.manage.Home),
		(r"/manage/users", routes.manage.ManageUsers),
		(r"/manage/books", routes.manage.ManageBooks),
		(r"/manage/settings", routes.manage.ManageSettings),
		(r"/manage/categories", routes.manage.ManageCategories),
	],**settings)
	application.listen(8888)
	tornado.ioloop.IOLoop.current().start()