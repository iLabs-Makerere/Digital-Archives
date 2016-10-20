import tornado.web
import pprint
import bcrypt
from ..models.users import Users

class Login(tornado.web.RequestHandler):
	
	def get(self):
		self.render("../views/login.html")
		
	def post(self):
		email = self.get_argument("email")
		password = self.get_argument("password")

		if not password or not email:
			self.render("../views/login.html")
		else:
			users_model = Users()
			user = users_model.get_user(email)
			a = user[0][6]
			hashed = bcrypt.hashpw(a, bcrypt.gensalt())
			if bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed:
				self.set_secure_cookie("log_status", "Active")
				self.set_secure_cookie("username", user[0][1])
				self.set_secure_cookie("role", user[0][7])
				self.redirect('/')
			else:
				self.render("../views/login.html")

class Register(tornado.web.RequestHandler):
	def get(self):
		self.render("../views/register.html")
		
class Logout(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')