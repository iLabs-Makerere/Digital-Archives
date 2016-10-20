import tornado.web
#import pprint
from ..models.users import Users
from ..models.books import Books
from ..models.categories import Categories

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("username")
        if not user: return None
        return user

class Index(BaseHandler):
    def get(self):
        if not self.get_secure_cookie("log_status"):
            self.render("../views/index.html")
        else:
            books_model = Books()
            categories_model = Categories()
            books_total = books_model.count_books()
            categories = categories_model.get_categories('id','DESC',100, 0)
            page = 1
            try:
                page = self.get_argument("page")
            except Exception, e:
                page = 1
            offset = (int(page) - 1) * 10
            books = books_model.get_books('ID','DESC',10,offset)
            #pprint.pprint(books)
            prev_page = int(page)-1
            c = int(page)*10
            r = books_total - c
            next_page = 0
            if r>0:
                next_page = int(page) + 1
                
            else:
                next_page = 0
            self.render("../views/home.html", view = "browse", categories = categories,books = books, next_page = next_page, prev_page = prev_page)