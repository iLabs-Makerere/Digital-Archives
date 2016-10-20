import tornado.web
import tornado.ioloop
import tornado
import pprint
import os, uuid
from ..models.users import Users
from ..models.books import Books
from ..models.categories import Categories

__UPLOADS__ = "static/files/"

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("username")
        if not user: return None
        return user

class Publish(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        categories_model = Categories()
        categories = categories_model.get_categories('id', 'DESC', 100, 0)
        self.render("../views/publish.html", view = "browse", categories=categories)

    def post(self):
        if not self.current_user:
            self.redirect("/login")
            return
        title = self.get_argument("title")
        author = self.get_argument("author")
        year = self.get_argument("year")
        isbn = self.get_argument("isbn")
        publisher = self.get_argument("publisher")
        category = self.get_argument("category")
        excerpt = self.get_argument("excerpt")
        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(fileinfo['body'])
        publish_model = Books()
        book = publish_model.add_book(title, excerpt, author, publisher, year, isbn, cname, category)
        self.redirect("/")

class Upload(BaseHandler):

    def get(self,book):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("../views/upload.html", view ="browse")

    def post(self):
        if not self.current_user:
            self.redirect("/login")
            return
        book = self.get_argument("book")

class Book(BaseHandler):

    def get(self,book):
        if not self.current_user:
            self.redirect("/login")
            return
        books_model = Books()
        book = books_model.get_book(book)
        print book
        self.render("../views/book.html", view = "reader", book=book)

class Search(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        search = self.get_argument("search")
        search_model = Books()
        books = search_model.search_book(search)
        #return book
        self.render("../views/search.html", view = "browse", books=books)
		