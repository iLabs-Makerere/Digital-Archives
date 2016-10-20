import tornado.web
import tornado.ioloop
import tornado
import pprint
import os, uuid
import bcrypt
from ..models.users import Users
from ..models.books import Books
from ..models.categories import Categories

__UPLOADS__ = "static/files/"

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("username")
        role = self.get_secure_cookie("role")

        if role == "admin":
            if not user: return None
            return user
        else:
            self.redirect("/")
            return

class Home(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("../views/manage/index.html")

class ManageBooks(BaseHandler):
    def get(self):
        books_model = Books()
        books_total = books_model.count_books()
        page = 1
        try:
            page = self.get_argument("page")
        except Exception, e:
            page = 1
        offset = (int(page) - 1) * 10
        books = books_model.get_books('ID','DESC',10,offset)
        prev_page = int(page)-1
        c = int(page)*10
        r = books_total - c
        next_page = 0
        if r>0:
            next_page = int(page) + 1
        else:
            next_page = 0
        self.render("../views/manage/books.html", books = books, next_page = next_page, prev_page = prev_page)

    def post(self):
        action = self.get_argument("action")

        if action =="view":
            idNo = self.get_argument("book")
            self.redirect("/book/"+idNo)
        if action == "delete":
            idNo = self.get_argument("book")
            books_model = Books()
            books_model.delete_books(idNo)
            self.redirect("/manage/books")
        if action =="edit":
            idNo = self.get_argument("book")
            books_model = Books()
            categories_model = Categories()
            categories = categories_model.get_categories('id', 'DESC', 100, 0)
            book = books_model.get_book(idNo)
            self.render("../views/edit_book.html", book=book, view = "browse", categories=categories)
        elif action=="update":
            idNo = self.get_argument("book")
            title = self.get_argument("title")
            excerpt = self.get_argument("excerpt")
            author =self.get_argument("author")
            publisher = self.get_argument("publisher")
            published_date = self.get_argument("year")
            isbn = self.get_argument("isbn")
            books_model = Books()
            #book = books_model.get_book(book)
            #title, excerpt, author, publisher, published_date, isbn, ufile
            books_model.edit_book(title, excerpt, author, publisher, published_date, isbn, idNo)
            self.redirect("/manage/books")
        else:
            self.redirect("/manage/books")

class ManageUsers(BaseHandler):
    def get(self):
        users_model = Users()
        users_total = users_model.count_users()
        page = 1
        try:
            page = self.get_argument("page")
        except Exception, e:
            page = 1
            offset = (int(page) - 1) * 10
            users = users_model.get_users(10,offset)
            prev_page = int(page)-1
            c = int(page)*10
            r = users_total - c
            next_page = 0
            if r>0:
                next_page = int(page) + 1
            else:
                next_page = 0
                self.render("../views/manage/users.html", users = users, next_page = next_page, prev_page = prev_page)
    
    def post(self):
        action = self.get_argument("action")
        email = self.get_argument("user")


        if action=="view":
            users_model = Users()
            users = users_model.get_users()
            self.render("../views/view_users.html", users=users)
        elif action=="delete":
            users_model = Users()
            users_model.delete_users(email)
            self.redirect("/manage/users")
        elif action=="edit":
            users_model = Users()
            user = users_model.get_user(email)
            self.render("../views/edit_user.html", user=user, view = "browse")
        elif action=="update":
            first_name = self.get_argument("first_name") 
            last_name = self.get_argument("last_name") 
            newemail=self.get_argument("newemail") 
            affiliation = self.get_argument("affiliation") 
            identity = self.get_argument("identity") 
            gender = self.get_argument("gender") 
            password = self.get_argument("newpassword")
            if not password:
                password = self.get_argument("oldpassword")
            else:
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                role = self.get_argument("role")
                users_model = Users()
                user = users_model.get_user(email)
                users_model.edit_user(first_name, last_name, newemail, affiliation, identity, gender, password, role, email)
                self.redirect("/manage/users")
        else:
            users_model = Users()
            user = users_model.add_user(user)
            self.render("../views/add_user.html", user=user, view = "browse")

class ManageSettings(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("../views/manage/settings.html")

    def post(self):
        action = self.get_argument("action")

class ManageCategories(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        categories_model = Categories()
        categories_total = categories_model.count_categories()
        page = 1
        try:
            page = self.get_argument("page")
        except Exception, e:
            page = 1
            offset = (int(page) - 1) * 10
            categories = categories_model.get_categories('id', 'DESC',10, offset)
            prev_page = int(page) - 1
            c = int(page) * 10
            r = categories_total - c
            next_page = 0
            if r > 0:
                next_page = int(page) + 1
            else:
                next_page = 0
                self.render("../views/manage/categories.html", categories=categories, next_page=next_page, prev_page=prev_page)

    def post(self):
        action = self.get_argument("action")

        if action == "add":
            category = self.get_argument("category")
            categories_model = Categories()
            category = categories_model.add_categories(category)
            self.redirect("/manage/categories")
